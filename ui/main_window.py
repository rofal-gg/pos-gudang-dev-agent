from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

COLOR = {
    "primary": "#6366f1",
    "primary_hover": "#4f46e5",
    "primary_light": "#e0e7ff",
    "bg_main": "#f8fafc",
    "bg_card": "#ffffff",
    "bg_sidebar": "#1e1b4b",
    "text_dark": "#1e293b",
    "text_muted": "#64748b",
    "text_sidebar": "#c7d2fe",
    "border": "#e2e8f0",
    "success_bg": "#dcfce7",
    "success_text": "#166534",
    "warning_bg": "#fef3c7",
    "warning_text": "#92400e",
    "danger_bg": "#fee2e2",
    "danger_text": "#991b1b",
    "node_default": "#6366f1",
    "node_new": "#f59e0b",
    "node_found": "#10b981",
    "node_line": "#94a3b8",
    "node_text": "#ffffff",
}

MAIN_STYLE = f"""
QMainWindow {{
    background: {COLOR["bg_main"]};
}}
QWidget#sidebar {{
    background: {COLOR["bg_sidebar"]};
    min-width: 220px;
    max-width: 220px;
}}
QPushButton#navBtn {{
    text-align: left;
    color: {COLOR["text_sidebar"]};
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    background: transparent;
}}
QPushButton#navBtn:hover {{
    background: rgba(99, 102, 241, 0.3);
    color: white;
}}
QPushButton#navBtn[active="true"] {{
    background: {COLOR["primary"]};
    color: white;
}}
QTableWidget {{
    background: white;
    border: 1px solid {COLOR["border"]};
    border-radius: 8px;
    gridline-color: {COLOR["border"]};
    font-size: 13px;
}}
QTableWidget::item:selected {{
    background: {COLOR["primary_light"]};
}}
QHeaderView::section {{
    background: {COLOR["bg_main"]};
    color: {COLOR["text_muted"]};
    font-weight: bold;
    padding: 8px;
    border: none;
    border-bottom: 1px solid {COLOR["border"]};
}}
QLineEdit, QSpinBox, QDateEdit, QComboBox {{
    border: 1px solid {COLOR["border"]};
    border-radius: 6px;
    padding: 6px 10px;
    background: white;
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {COLOR["primary"]};
}}
QPushButton#primaryBtn {{
    background: {COLOR["primary"]};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton#primaryBtn:hover {{
    background: {COLOR["primary_hover"]};
}}
QPushButton#dangerBtn {{
    background: {COLOR["danger_bg"]};
    color: {COLOR["danger_text"]};
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
}}
QLabel#avlBadge {{
    background: {COLOR["success_bg"]};
    color: {COLOR["success_text"]};
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: bold;
}}
QFrame#card {{
    background: white;
    border: 1px solid {COLOR["border"]};
    border-radius: 10px;
}}
"""


class MainWindow(QMainWindow):
    def __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack):
        super().__init__()
        self.avl_by_id = avl_by_id
        self.avl_by_name = avl_by_name
        self.alert_queue = alert_queue
        self.action_stack = action_stack
        self.current_user = None
        self._nav_entries = []

        self.setWindowTitle("Sistem POS & Manajemen Gudang")
        self.setMinimumSize(1200, 700)

        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(MAIN_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        logo = QLabel("POS & Gudang")
        logo.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold; padding: 20px;"
        )
        sidebar_layout.addWidget(logo)

        subtitle = QLabel("Struktur Data")
        subtitle.setStyleSheet(
            f"color: {COLOR['text_sidebar']}; font-size: 11px; "
            "opacity: 0.7; padding: 0 20px 16px;"
        )
        sidebar_layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(
            f"background: {COLOR['text_sidebar']}; max-height: 1px; margin: 0 16px;"
        )
        sidebar_layout.addWidget(separator)

        self.nav_widget = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(8, 12, 8, 8)
        self.nav_layout.setSpacing(4)
        sidebar_layout.addWidget(self.nav_widget)

        sidebar_layout.addStretch()

        logout_btn = QPushButton("Keluar")
        logout_btn.setObjectName("navBtn")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)

        self.stack = QStackedWidget()
        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.stack, 1)

        self.sidebar.hide()
        self.show_login()

    def _clear_stack(self) -> None:
        while self.stack.count():
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

    def _clear_nav_buttons(self) -> None:
        self._nav_entries.clear()
        while self.nav_layout.count():
            item = self.nav_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _set_nav_active(self, page_widget: QWidget) -> None:
        for btn, page in self._nav_entries:
            active = page is page_widget
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def show_login(self) -> None:
        from ui.login_page import LoginPage

        self.sidebar.hide()
        self._clear_nav_buttons()
        self._clear_stack()

        login_page = LoginPage(self)
        self.stack.addWidget(login_page)
        self.stack.setCurrentWidget(login_page)

    def show_main_ui(self, user: dict) -> None:
        from ui.avl_visual_widget import AVLVisualWidget
        from ui.dashboard_page import DashboardPage
        from ui.gudang_page import GudangPage
        from ui.kasir_page import KasirPage

        self.current_user = user
        self.sidebar.show()
        self._clear_nav_buttons()
        self._clear_stack()

        shared = (
            self.avl_by_id,
            self.avl_by_name,
            self.alert_queue,
            self.action_stack,
            user,
        )
        kasir_page = KasirPage(*shared, main_window=self)
        gudang_page = GudangPage(*shared, main_window=self)
        dashboard_page = DashboardPage(*shared)
        avl_page = AVLVisualWidget(*shared)

        self.gudang_page = gudang_page
        self.avl_visual_page = avl_page

        for page in (kasir_page, gudang_page, dashboard_page, avl_page):
            self.stack.addWidget(page)

        role = user.get("role", "")
        if role == "kasir":
            nav_items = [
                ("Kasir", kasir_page),
                ("Visualisasi AVL", avl_page),
            ]
        else:
            nav_items = [
                ("Gudang", gudang_page),
                ("Dashboard", dashboard_page),
                ("Visualisasi AVL", avl_page),
            ]

        for label, page in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, p=page: self.navigate(p))
            self.nav_layout.addWidget(btn)
            self._nav_entries.append((btn, page))

        if nav_items:
            self.navigate(nav_items[0][1])

    def navigate(self, page_widget: QWidget) -> None:
        self.stack.setCurrentWidget(page_widget)
        self._set_nav_active(page_widget)

    def logout(self) -> None:
        self.current_user = None
        self._clear_nav_buttons()
        self._clear_stack()
        self.show_login()

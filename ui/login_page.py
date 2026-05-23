import database

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.main_window import COLOR


class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(380)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(16)

        title = QLabel("Selamat Datang")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        card_layout.addWidget(title)

        subtitle = QLabel("Sistem POS & Manajemen Gudang")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"font-size: 13px; color: {COLOR['text_muted']};")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(16)

        card_layout.addWidget(QLabel("Username"))
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Masukkan username")
        card_layout.addWidget(self.input_username)

        card_layout.addWidget(QLabel("Password"))
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Masukkan password")
        self.input_password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.input_password)

        card_layout.addSpacing(8)

        self.lbl_error = QLabel()
        self.lbl_error.setAlignment(Qt.AlignCenter)
        self.lbl_error.setStyleSheet(f"color: {COLOR['danger_text']}; font-size: 13px;")
        self.lbl_error.hide()
        card_layout.addWidget(self.lbl_error)

        self.btn_login = QPushButton("Masuk")
        self.btn_login.setObjectName("primaryBtn")
        self.btn_login.setFixedHeight(42)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.btn_login)

        note = QLabel("Demo: admin/admin123  atau  kasir1/kasir123")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
        card_layout.addWidget(note)

        outer.addWidget(card)

        self.btn_login.clicked.connect(self.do_login)
        self.input_username.returnPressed.connect(self.do_login)
        self.input_password.returnPressed.connect(self.do_login)

    def do_login(self) -> None:
        username = self.input_username.text().strip()
        password = self.input_password.text()
        if not username or not password:
            self.lbl_error.setText("Username dan password tidak boleh kosong")
            self.lbl_error.show()
            return

        user = database.verify_login(username, password)
        if user:
            self.lbl_error.hide()
            self.main_window.show_main_ui(user)
        else:
            self.lbl_error.setText("❌ Username atau password salah")
            self.lbl_error.show()
            self.input_password.clear()
            self.input_password.setFocus()

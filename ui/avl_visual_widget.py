from datetime import datetime

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.main_window import COLOR


def _count_nodes(node: dict | None) -> int:
    if node is None:
        return 0
    return 1 + _count_nodes(node.get("left")) + _count_nodes(node.get("right"))


def _tree_height(node: dict | None) -> int:
    if node is None:
        return 0
    return 1 + max(_tree_height(node.get("left")), _tree_height(node.get("right")))


def _find_balance_factor(node: dict | None, key) -> int | None:
    if node is None:
        return None
    if node["key"] == key:
        return node["balance_factor"]
    left = _find_balance_factor(node.get("left"), key)
    if left is not None:
        return left
    return _find_balance_factor(node.get("right"), key)


class AVLCanvas(QWidget):
    def __init__(self, visual_widget: "AVLVisualWidget"):
        super().__init__(visual_widget)
        self._visual_widget = visual_widget
        self.snapshot = None
        self.highlight_key = None
        self.highlight_color = "#f59e0b"
        self.found_key = None
        self.node_radius = 28
        self.level_height = 90
        self._positions: dict = {}
        self.setMouseTracking(True)
        self.setMinimumHeight(500)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.snapshot is None:
            painter.setPen(QColor(COLOR["text_muted"]))
            font = QFont()
            font.setPointSize(14)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "Pohon AVL kosong")
            return

        canvas_width = max(self.width(), 400)
        self._positions = {}
        self._calculate_positions(self.snapshot, 0, canvas_width, 50)
        self._draw_edges(painter, self.snapshot)
        self._draw_nodes(painter, self.snapshot)

        max_y = max((y for _, y in self._positions.values()), default=50)
        min_h = max_y + self.node_radius + 40
        if self.minimumHeight() < min_h:
            self.setMinimumHeight(min_h)

    def _calculate_positions(self, node, x_left: int, x_right: int, y: int) -> None:
        if node is None:
            return
        x_center = (x_left + x_right) // 2
        self._positions[node["key"]] = (x_center, y)
        mid = (x_left + x_right) // 2
        self._calculate_positions(node.get("left"), x_left, mid, y + self.level_height)
        self._calculate_positions(node.get("right"), mid, x_right, y + self.level_height)

    def _draw_edges(self, painter: QPainter, node) -> None:
        if node is None:
            return
        px, py = self._positions[node["key"]]
        pen = QPen(QColor(COLOR["node_line"]))
        pen.setWidth(2)
        painter.setPen(pen)
        for child in (node.get("left"), node.get("right")):
            if child:
                cx, cy = self._positions[child["key"]]
                painter.drawLine(px, py + self.node_radius, cx, cy - self.node_radius)
                self._draw_edges(painter, child)

    def _draw_nodes(self, painter: QPainter, node) -> None:
        if node is None:
            return
        self._draw_nodes(painter, node.get("left"))
        self._draw_nodes(painter, node.get("right"))
        x, y = self._positions[node["key"]]
        r = self.node_radius

        if node["key"] == self.highlight_key:
            color = QColor(self.highlight_color)
        elif node["key"] == self.found_key:
            color = QColor(COLOR["node_found"])
        else:
            color = QColor(COLOR["node_default"])

        painter.setBrush(color)
        painter.setPen(QPen(color.darker(120), 2))
        painter.drawEllipse(x - r, y - r, r * 2, r * 2)

        painter.setPen(QColor(COLOR["node_text"]))
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        key_text = str(node["key"])
        if len(key_text) > 8:
            key_text = key_text[:6] + "…"
        painter.drawText(x - r, y - r, r * 2, r * 2, Qt.AlignCenter, key_text)

        painter.setPen(QColor(COLOR["text_muted"]))
        font2 = QFont()
        font2.setPointSize(8)
        painter.setFont(font2)
        bf_text = f"bf:{node['balance_factor']}"
        painter.drawText(x - 20, y + r + 2, 40, 16, Qt.AlignCenter, bf_text)

    def mousePressEvent(self, event) -> None:
        click_x, click_y = event.x(), event.y()
        for key, (nx, ny) in self._positions.items():
            dist = ((click_x - nx) ** 2 + (click_y - ny) ** 2) ** 0.5
            if dist <= self.node_radius:
                self._visual_widget.show_node_info(key)
                break


class AVLVisualWidget(QWidget):
    def __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user):
        super().__init__()
        self.avl_by_id = avl_by_id
        self.avl_by_name = avl_by_name
        self.alert_queue = alert_queue
        self.action_stack = action_stack
        self.user = user

        self.current_tree = avl_by_id
        self.highlight_key = None
        self.highlight_color = "#f59e0b"
        self.found_key = None

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("Visualisasi AVL Tree")
        title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        header.addWidget(title)
        header.addStretch()

        self.radio_by_id = QRadioButton("🔢 by ID (Integer)")
        self.radio_by_id.setChecked(True)
        self.radio_by_name = QRadioButton("🔤 by Nama (String)")
        tree_group = QButtonGroup(self)
        tree_group.addButton(self.radio_by_id)
        tree_group.addButton(self.radio_by_name)
        header.addWidget(self.radio_by_id)
        header.addWidget(self.radio_by_name)

        btn_refresh = QPushButton("Refresh")
        btn_refresh.setObjectName("primaryBtn")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.refresh)
        header.addWidget(btn_refresh)
        layout.addLayout(header)

        info_bar = QHBoxLayout()
        info_bar.setSpacing(12)
        self.lbl_total = self._make_info_card("Total Node", "0")
        self.lbl_height = self._make_info_card("Height Pohon", "0")
        self.lbl_updated = self._make_info_card("Last Updated", "—")
        info_bar.addWidget(self._card_wrap(self.lbl_total, "Total Node"))
        info_bar.addWidget(self._card_wrap(self.lbl_height, "Height Pohon"))
        info_bar.addWidget(self._card_wrap(self.lbl_updated, "Last Updated"))
        layout.addLayout(info_bar)

        self.canvas = AVLCanvas(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(self.canvas)
        scroll.setMinimumHeight(520)
        layout.addWidget(scroll, 1)

        legend = QHBoxLayout()
        legend.setSpacing(20)
        for dot_color, label in (
            (COLOR["node_default"], "Node default"),
            ("#f59e0b", "Node baru diinsert"),
            (COLOR["node_found"], "Node ditemukan (search)"),
        ):
            row = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {dot_color}; font-size: 16px;")
            row.addWidget(dot)
            lbl = QLabel(label)
            lbl.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
            row.addWidget(lbl)
            legend.addLayout(row)
        legend.addStretch()
        layout.addLayout(legend)

        info_box = QLabel(
            "Angka dalam node = key barang | bf = balance factor (-1/0/1 = seimbang)\n"
            "Node kuning = baru diinsert | Node hijau = hasil pencarian terakhir"
        )
        info_box.setStyleSheet(
            f"font-size: 12px; font-style: italic; color: {COLOR['text_muted']};"
        )
        info_box.setWordWrap(True)
        layout.addWidget(info_box)

        self.radio_by_id.toggled.connect(self._on_tree_toggle)
        self.radio_by_name.toggled.connect(self._on_tree_toggle)

    def _make_info_card(self, _title: str, value: str) -> QLabel:
        lbl = QLabel(value)
        lbl.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLOR['primary']};"
        )
        lbl.setAlignment(Qt.AlignCenter)
        return lbl

    def _card_wrap(self, value_lbl: QLabel, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 12)
        t = QLabel(title)
        t.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
        t.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(t)
        card_layout.addWidget(value_lbl)
        return card

    def _on_tree_toggle(self) -> None:
        if self.radio_by_id.isChecked():
            self.current_tree = self.avl_by_id
        else:
            self.current_tree = self.avl_by_name
        self.refresh()

    def refresh(self) -> None:
        snapshot = self.current_tree.to_snapshot()
        self.canvas.snapshot = snapshot
        self.canvas.highlight_key = self.highlight_key
        self.canvas.highlight_color = self.highlight_color
        self.canvas.found_key = self.found_key

        total = _count_nodes(snapshot)
        height = _tree_height(snapshot)
        self.lbl_total.setText(str(total))
        self.lbl_height.setText(str(height))
        self.lbl_updated.setText(datetime.now().strftime("%H:%M:%S"))

        levels = max(height, 1)
        min_w = max(400, total * 70)
        min_h = max(500, levels * self.canvas.level_height + 120)
        self.canvas.setMinimumSize(min_w, min_h)
        self.canvas.update()

    def highlight_new_node(self, key) -> None:
        self.radio_by_id.setChecked(True)
        self.current_tree = self.avl_by_id
        self.highlight_key = key
        self.highlight_color = "#f59e0b"
        self.found_key = None
        self.refresh()
        QTimer.singleShot(2000, self.clear_highlight)

    def highlight_found_node(self, key) -> None:
        if isinstance(key, int):
            self.radio_by_id.setChecked(True)
            self.current_tree = self.avl_by_id
        else:
            self.radio_by_name.setChecked(True)
            self.current_tree = self.avl_by_name
        self.found_key = key
        self.highlight_key = None
        self.refresh()
        QTimer.singleShot(2000, self.clear_found)

    def clear_highlight(self) -> None:
        self.highlight_key = None
        self.canvas.highlight_key = None
        self.canvas.update()

    def clear_found(self) -> None:
        self.found_key = None
        self.canvas.found_key = None
        self.canvas.update()

    def show_node_info(self, key) -> None:
        data = self.current_tree.search(key)
        if data is None and not isinstance(key, str):
            data = self.current_tree.search(str(key))
        if data is None:
            QMessageBox.information(self, "Node", f"Key {key} tidak ditemukan di pohon.")
            return

        snapshot = self.current_tree.to_snapshot()
        bf = _find_balance_factor(snapshot, key)
        bf_str = str(bf) if bf is not None else "—"
        harga = data.get("harga_satuan", 0)
        harga_fmt = f"Rp {int(harga):,}".replace(",", ".")

        QMessageBox.information(
            self,
            "Info Node AVL",
            f"<b>Key:</b> {key}<br>"
            f"<b>Nama Barang:</b> {data.get('nama_barang', '—')}<br>"
            f"<b>Harga Satuan:</b> {harga_fmt}<br>"
            f"<b>Balance Factor:</b> {bf_str}",
        )

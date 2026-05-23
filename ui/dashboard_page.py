from datetime import date, datetime

import database

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.main_window import COLOR


def _tipe_label(tipe: str) -> str:
    labels = {
        "tambah_barang": "Tambah Barang",
        "tambah_batch": "Tambah Batch",
        "checkout": "Checkout",
    }
    return labels.get(tipe, tipe)


def _sisa_hari(tgl_expired: str) -> int:
    exp = datetime.strptime(tgl_expired, "%Y-%m-%d").date()
    return (exp - date.today()).days


class DashboardPage(QWidget):
    def __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user):
        super().__init__()
        self.avl_by_id = avl_by_id
        self.avl_by_name = avl_by_name
        self.alert_queue = alert_queue
        self.action_stack = action_stack
        self.user = user
        self._build_ui()
        self.load_all()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        header.addWidget(title)
        header.addStretch()

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_all)
        header.addWidget(btn_refresh)
        layout.addLayout(header)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.lbl_expiry_count = QLabel("0")
        cards_row.addWidget(
            self._make_summary_card(
                "⚠ Expiry Alert",
                self.lbl_expiry_count,
                COLOR["danger_text"],
            )
        )

        self.lbl_stok_count = QLabel("0")
        cards_row.addWidget(
            self._make_summary_card(
                "📉 Stok Tipis",
                self.lbl_stok_count,
                COLOR["warning_text"],
            )
        )

        self.lbl_log_count = QLabel("0")
        cards_row.addWidget(
            self._make_summary_card(
                "📋 Total Aksi",
                self.lbl_log_count,
                COLOR["primary"],
            )
        )
        layout.addLayout(cards_row)

        heap_card = QFrame()
        heap_card.setObjectName("card")
        heap_layout = QVBoxLayout(heap_card)
        heap_layout.setContentsMargins(20, 16, 20, 16)
        heap_layout.setSpacing(12)

        heap_title = QLabel("🔺 Min-Heap Priority Queue — Expiry Terdekat")
        heap_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        heap_layout.addWidget(heap_title)

        heap_note = QLabel(
            "Data diurutkan menggunakan Min-Heap (Python heapq), bukan SQL ORDER BY. "
            "Insert O(log n) | Peek O(1) | Kompleksitas ruang O(n)"
        )
        heap_note.setWordWrap(True)
        heap_note.setStyleSheet(
            f"font-size: 12px; font-style: italic; color: {COLOR['text_muted']};"
        )
        heap_layout.addWidget(heap_note)

        self.tbl_heap = QTableWidget(0, 5)
        self.tbl_heap.setHorizontalHeaderLabels(
            ["Rank", "Nama Barang", "Tgl Expired", "Sisa Hari", "Stok"]
        )
        self._setup_table(self.tbl_heap)
        heap_layout.addWidget(self.tbl_heap)
        layout.addWidget(heap_card)

        stok_card = QFrame()
        stok_card.setObjectName("card")
        stok_layout = QVBoxLayout(stok_card)
        stok_layout.setContentsMargins(20, 16, 20, 16)
        stok_layout.setSpacing(12)

        stok_title = QLabel("📉 Barang Stok Tipis (≤ 10 unit)")
        stok_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        stok_layout.addWidget(stok_title)

        self.tbl_stok = QTableWidget(0, 3)
        self.tbl_stok.setHorizontalHeaderLabels(
            ["ID", "Nama Barang", "Sisa Stok Total"]
        )
        self._setup_table(self.tbl_stok)
        stok_layout.addWidget(self.tbl_stok)
        layout.addWidget(stok_card)

        log_card = QFrame()
        log_card.setObjectName("card")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(20, 16, 20, 16)
        log_layout.setSpacing(12)

        log_title = QLabel("📋 Log Aksi — Stack ADT")
        log_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        log_layout.addWidget(log_title)

        log_note = QLabel(
            "Setiap aksi dicatat ke Stack (LIFO). Undo tersedia di halaman Gudang."
        )
        log_note.setWordWrap(True)
        log_note.setStyleSheet(
            f"font-size: 12px; font-style: italic; color: {COLOR['text_muted']};"
        )
        log_layout.addWidget(log_note)

        self.tbl_log = QTableWidget(0, 3)
        self.tbl_log.setHorizontalHeaderLabels(["Waktu", "Tipe Aksi", "Status"])
        self._setup_table(self.tbl_log)
        log_layout.addWidget(self.tbl_log)
        layout.addWidget(log_card)

    def _make_summary_card(
        self, title_text: str, count_label: QLabel, count_color: str
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(8)

        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
        card_layout.addWidget(title_lbl)

        count_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        count_label.setStyleSheet(
            f"font-size: 28px; font-weight: bold; color: {count_color};"
        )
        card_layout.addWidget(count_label)
        return card

    def _setup_table(self, table: QTableWidget) -> None:
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.verticalHeader().setVisible(False)
        hdr = table.horizontalHeader()
        hdr.setStretchLastSection(True)

    def load_all(self) -> None:
        alerts = database.get_alerts()
        expiry_soon = alerts["expiry_soon"]
        stok_tipis = alerts["stok_tipis"]
        log_rows = database.get_action_log()

        self.lbl_expiry_count.setText(str(len(expiry_soon)))
        self.lbl_stok_count.setText(str(len(stok_tipis)))
        self.lbl_log_count.setText(str(len(log_rows)))

        self._load_heap_table()
        self._load_stok_table(stok_tipis)
        self._load_log_table(log_rows)

    def _load_heap_table(self) -> None:
        items = self.alert_queue.get_top_n(10)
        self.tbl_heap.setRowCount(len(items))

        for i, item in enumerate(items):
            sisa = _sisa_hari(item["tgl_expired"])

            rank_item = QTableWidgetItem(str(i + 1))
            rank_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_heap.setItem(i, 0, rank_item)

            self.tbl_heap.setItem(i, 1, QTableWidgetItem(item["nama_barang"]))
            self.tbl_heap.setItem(i, 2, QTableWidgetItem(item["tgl_expired"]))

            sisa_item = QTableWidgetItem(str(sisa))
            sisa_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_heap.setItem(i, 3, sisa_item)

            stok_item = QTableWidgetItem(str(item["jumlah_stok"]))
            stok_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_heap.setItem(i, 4, stok_item)

            if sisa <= 3:
                bg = QColor(COLOR["danger_bg"])
            elif sisa <= 7:
                bg = QColor(COLOR["warning_bg"])
            else:
                bg = None

            if bg is not None:
                for col in range(5):
                    cell = self.tbl_heap.item(i, col)
                    if cell:
                        cell.setBackground(bg)

        hdr = self.tbl_heap.horizontalHeader()
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)

    def _load_stok_table(self, rows: list[dict]) -> None:
        self.tbl_stok.setRowCount(len(rows))
        warning_bg = QColor(COLOR["warning_bg"])

        for i, row in enumerate(rows):
            id_item = QTableWidgetItem(str(row["id_barang"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_stok.setItem(i, 0, id_item)

            self.tbl_stok.setItem(i, 1, QTableWidgetItem(row["nama_barang"]))

            stok_item = QTableWidgetItem(str(row["sisa_stok_total"]))
            stok_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_stok.setItem(i, 2, stok_item)

            for col in range(3):
                cell = self.tbl_stok.item(i, col)
                if cell:
                    cell.setBackground(warning_bg)

        hdr = self.tbl_stok.horizontalHeader()
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)

    def _load_log_table(self, rows: list[dict]) -> None:
        self.tbl_log.setRowCount(len(rows))

        for i, row in enumerate(rows):
            self.tbl_log.setItem(i, 0, QTableWidgetItem(row["tgl_waktu"]))
            self.tbl_log.setItem(i, 1, QTableWidgetItem(_tipe_label(row["tipe_aksi"])))

            undone = bool(row.get("sudah_undo", 0))
            status_text = "Di-undo" if undone else "Aktif"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)

            if undone:
                status_item.setBackground(QColor(COLOR["danger_bg"]))
                status_item.setForeground(QColor(COLOR["danger_text"]))
            else:
                status_item.setBackground(QColor(COLOR["success_bg"]))
                status_item.setForeground(QColor(COLOR["success_text"]))

            self.tbl_log.setItem(i, 2, status_item)

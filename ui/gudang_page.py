import database

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.main_window import COLOR


def _format_rp(value: int) -> str:
    return f"Rp {value:,}".replace(",", ".")


def _tipe_label(tipe: str) -> str:
    labels = {
        "tambah_barang": "Tambah Barang",
        "tambah_batch": "Tambah Batch",
        "checkout": "Checkout",
    }
    return labels.get(tipe, tipe)


class GudangPage(QWidget):
    def __init__(
        self, avl_by_id, avl_by_name, alert_queue, action_stack, user, main_window=None
    ):
        super().__init__()
        self.avl_by_id = avl_by_id
        self.avl_by_name = avl_by_name
        self.alert_queue = alert_queue
        self.action_stack = action_stack
        self.user = user
        self.main_window = main_window
        self._build_ui()
        self.load_inventory()
        self.load_log()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Manajemen Gudang")
        title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        layout.addWidget(title)

        admin_lbl = QLabel(f"Admin: {self.user['username']}")
        admin_lbl.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
        layout.addWidget(admin_lbl)

        inv_card = QFrame()
        inv_card.setObjectName("card")
        inv_layout = QVBoxLayout(inv_card)
        inv_layout.setContentsMargins(20, 16, 20, 16)
        inv_layout.setSpacing(12)

        inv_header = QHBoxLayout()
        inv_title = QLabel("📦 Katalog & Stok Barang")
        inv_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        inv_header.addWidget(inv_title)
        inv_header.addStretch()

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_inventory)
        inv_header.addWidget(btn_refresh)
        inv_layout.addLayout(inv_header)

        self.tbl_inventory = QTableWidget(0, 5)
        self.tbl_inventory.setHorizontalHeaderLabels(
            ["ID", "Nama Barang", "Harga Satuan", "Stok Total", "Status"]
        )
        self.tbl_inventory.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_inventory.setAlternatingRowColors(True)
        self.tbl_inventory.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_inventory.verticalHeader().setVisible(False)
        inv_hdr = self.tbl_inventory.horizontalHeader()
        inv_hdr.setStretchLastSection(True)
        inv_hdr.setSectionResizeMode(1, QHeaderView.Stretch)
        inv_layout.addWidget(self.tbl_inventory)
        layout.addWidget(inv_card)

        forms_row = QHBoxLayout()
        forms_row.setSpacing(16)

        barang_card = QFrame()
        barang_card.setObjectName("card")
        barang_layout = QVBoxLayout(barang_card)
        barang_layout.setContentsMargins(20, 16, 20, 16)
        barang_layout.setSpacing(12)

        barang_title = QLabel("➕ Tambah Barang Baru")
        barang_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        barang_layout.addWidget(barang_title)

        barang_form = QFormLayout()
        barang_form.setSpacing(10)

        self.spin_id = QSpinBox()
        self.spin_id.setRange(1, 99999)
        self.spin_id.setValue(1)
        barang_form.addRow("ID Barang:", self.spin_id)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama barang...")
        barang_form.addRow("Nama Barang:", self.input_nama)

        self.spin_harga = QSpinBox()
        self.spin_harga.setRange(1, 9999999)
        self.spin_harga.setPrefix("Rp ")
        self.spin_harga.setValue(1000)
        barang_form.addRow("Harga Satuan:", self.spin_harga)
        barang_layout.addLayout(barang_form)

        btn_tambah_barang = QPushButton("Tambah Barang")
        btn_tambah_barang.setObjectName("primaryBtn")
        btn_tambah_barang.setCursor(Qt.PointingHandCursor)
        btn_tambah_barang.clicked.connect(self.do_tambah_barang)
        barang_layout.addWidget(btn_tambah_barang)

        self.lbl_barang_msg = QLabel()
        self.lbl_barang_msg.setWordWrap(True)
        self.lbl_barang_msg.hide()
        barang_layout.addWidget(self.lbl_barang_msg)

        forms_row.addWidget(barang_card, 1)

        batch_card = QFrame()
        batch_card.setObjectName("card")
        batch_layout = QVBoxLayout(batch_card)
        batch_layout.setContentsMargins(20, 16, 20, 16)
        batch_layout.setSpacing(12)

        batch_title = QLabel("📥 Tambah Batch Stok")
        batch_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        batch_layout.addWidget(batch_title)

        batch_form = QFormLayout()
        batch_form.setSpacing(10)

        self.combo_barang = QComboBox()
        batch_form.addRow("Barang:", self.combo_barang)

        self.spin_stok = QSpinBox()
        self.spin_stok.setRange(1, 99999)
        self.spin_stok.setValue(10)
        batch_form.addRow("Jumlah Stok:", self.spin_stok)

        today = QDate.currentDate()
        self.date_masuk = QDateEdit()
        self.date_masuk.setCalendarPopup(True)
        self.date_masuk.setDisplayFormat("yyyy-MM-dd")
        self.date_masuk.setDate(today)
        batch_form.addRow("Tgl Masuk:", self.date_masuk)

        self.date_expired = QDateEdit()
        self.date_expired.setCalendarPopup(True)
        self.date_expired.setDisplayFormat("yyyy-MM-dd")
        self.date_expired.setDate(today.addDays(30))
        batch_form.addRow("Tgl Expired:", self.date_expired)
        batch_layout.addLayout(batch_form)

        btn_tambah_batch = QPushButton("Tambah Batch")
        btn_tambah_batch.setObjectName("primaryBtn")
        btn_tambah_batch.setCursor(Qt.PointingHandCursor)
        btn_tambah_batch.clicked.connect(self.do_tambah_batch)
        batch_layout.addWidget(btn_tambah_batch)

        self.lbl_batch_msg = QLabel()
        self.lbl_batch_msg.setWordWrap(True)
        self.lbl_batch_msg.hide()
        batch_layout.addWidget(self.lbl_batch_msg)

        forms_row.addWidget(batch_card, 1)
        layout.addLayout(forms_row)

        log_card = QFrame()
        log_card.setObjectName("card")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(20, 16, 20, 16)
        log_layout.setSpacing(12)

        log_header = QHBoxLayout()
        log_title = QLabel("📋 Riwayat Aksi (Stack ADT)")
        log_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        log_header.addWidget(log_title)
        log_header.addStretch()

        btn_undo = QPushButton("↩ Undo Aksi Terakhir")
        btn_undo.setObjectName("dangerBtn")
        btn_undo.setCursor(Qt.PointingHandCursor)
        btn_undo.clicked.connect(self.do_undo)
        log_header.addWidget(btn_undo)
        log_layout.addLayout(log_header)

        self.tbl_log = QTableWidget(0, 3)
        self.tbl_log.setHorizontalHeaderLabels(["Waktu", "Tipe Aksi", "Status"])
        self.tbl_log.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_log.setAlternatingRowColors(True)
        self.tbl_log.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_log.verticalHeader().setVisible(False)
        log_hdr = self.tbl_log.horizontalHeader()
        log_hdr.setStretchLastSection(True)
        log_hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        log_hdr.setSectionResizeMode(1, QHeaderView.Stretch)
        log_layout.addWidget(self.tbl_log)
        layout.addWidget(log_card, 1)

    def _show_msg(self, label: QLabel, text: str, *, success: bool) -> None:
        if success:
            label.setStyleSheet(
                f"color: {COLOR['success_text']}; font-size: 13px; "
                f"background: {COLOR['success_bg']}; padding: 8px; border-radius: 6px;"
            )
        else:
            label.setStyleSheet(
                f"color: {COLOR['danger_text']}; font-size: 13px; "
                f"background: {COLOR['danger_bg']}; padding: 8px; border-radius: 6px;"
            )
        label.setText(text)
        label.show()

    def load_inventory(self) -> None:
        rows = database.get_inventory()
        self.tbl_inventory.setRowCount(0)
        self.tbl_inventory.setRowCount(len(rows))

        self.combo_barang.blockSignals(True)
        self.combo_barang.clear()

        for i, row in enumerate(rows):
            stok = int(row["sisa_stok_total"])
            tipis = stok <= 10

            id_item = QTableWidgetItem(str(row["id_barang"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_inventory.setItem(i, 0, id_item)

            self.tbl_inventory.setItem(i, 1, QTableWidgetItem(row["nama_barang"]))

            harga_item = QTableWidgetItem(_format_rp(int(row["harga_satuan"])))
            harga_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_inventory.setItem(i, 2, harga_item)

            stok_item = QTableWidgetItem(str(stok))
            stok_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_inventory.setItem(i, 3, stok_item)

            status_text = "⚠ Tipis" if tipis else "✓ Aman"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            if tipis:
                status_item.setForeground(Qt.darkRed)
            else:
                status_item.setForeground(Qt.darkGreen)
            self.tbl_inventory.setItem(i, 4, status_item)

            if tipis:
                danger = QColor(COLOR["danger_bg"])
                for col in range(5):
                    cell = self.tbl_inventory.item(i, col)
                    if cell:
                        cell.setBackground(danger)

            label = f"{row['id_barang']} — {row['nama_barang']}"
            self.combo_barang.addItem(label, row["id_barang"])

        self.combo_barang.blockSignals(False)

    def load_log(self) -> None:
        rows = database.get_action_log()
        self.tbl_log.setRowCount(len(rows))

        for i, row in enumerate(rows):
            waktu_item = QTableWidgetItem(row["tgl_waktu"])
            self.tbl_log.setItem(i, 0, waktu_item)

            tipe_item = QTableWidgetItem(_tipe_label(row["tipe_aksi"]))
            self.tbl_log.setItem(i, 1, tipe_item)

            undone = bool(row.get("sudah_undo", 0))
            status_text = "Di-undo" if undone else "Aktif"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            if undone:
                status_item.setForeground(QColor(COLOR["danger_text"]))
            else:
                status_item.setForeground(QColor(COLOR["success_text"]))
            self.tbl_log.setItem(i, 2, status_item)

    def do_tambah_barang(self) -> None:
        id_b = self.spin_id.value()
        nama = self.input_nama.text().strip()
        harga = self.spin_harga.value()

        if not nama:
            self._show_msg(self.lbl_barang_msg, "Nama barang tidak boleh kosong.", success=False)
            return

        if not database.insert_barang(id_b, nama, harga):
            self._show_msg(
                self.lbl_barang_msg,
                f"ID {id_b} sudah ada. Gunakan ID lain.",
                success=False,
            )
            return

        row_data = database.get_barang_by_id(id_b)
        self.avl_by_id.insert(id_b, row_data)
        self.avl_by_name.insert(nama.strip().lower(), row_data)
        self.action_stack.push("tambah_barang", row_data)
        database.insert_action_log("tambah_barang", row_data)

        self.load_inventory()
        self.load_log()

        self._show_msg(
            self.lbl_barang_msg,
            f"Barang '{nama}' (ID {id_b}) berhasil ditambahkan.",
            success=True,
        )

        if self.main_window is not None and hasattr(self.main_window, "avl_visual_page"):
            self.main_window.avl_visual_page.highlight_new_node(id_b)

        self.spin_id.setValue(1)
        self.input_nama.clear()
        self.spin_harga.setValue(1000)

    def do_tambah_batch(self) -> None:
        if self.combo_barang.count() == 0:
            self._show_msg(
                self.lbl_batch_msg,
                "Tidak ada barang. Tambah barang terlebih dahulu.",
                success=False,
            )
            return

        id_barang = self.combo_barang.currentData()
        jumlah = self.spin_stok.value()
        tgl_masuk = self.date_masuk.date().toString("yyyy-MM-dd")
        tgl_expired = self.date_expired.date().toString("yyyy-MM-dd")

        if tgl_expired <= tgl_masuk:
            self._show_msg(
                self.lbl_batch_msg,
                "Tanggal expired harus setelah tanggal masuk.",
                success=False,
            )
            return

        barang = database.get_barang_by_id(id_barang)
        if not barang:
            self._show_msg(self.lbl_batch_msg, "Barang tidak ditemukan.", success=False)
            return

        nama_barang = barang["nama_barang"]
        id_batch = database.insert_batch(id_barang, jumlah, tgl_masuk, tgl_expired)
        self.alert_queue.push(tgl_expired, id_batch, nama_barang, jumlah)
        self.action_stack.push("tambah_batch", {"id_batch": id_batch})
        database.insert_action_log("tambah_batch", {"id_batch": id_batch})

        self.load_inventory()
        self.load_log()

        self._show_msg(
            self.lbl_batch_msg,
            f"Batch stok +{jumlah} untuk '{nama_barang}' berhasil ditambahkan.",
            success=True,
        )
        self.spin_stok.setValue(10)
        today = QDate.currentDate()
        self.date_masuk.setDate(today)
        self.date_expired.setDate(today.addDays(30))

    def _mark_latest_log_undo(self, tipe: str) -> None:
        for row in database.get_action_log():
            if row["tipe_aksi"] == tipe:
                database.mark_undo(row["id_log"])
                return

    def do_undo(self) -> None:
        action = self.action_stack.pop()
        if action is None:
            QMessageBox.information(
                self,
                "Undo",
                "Tidak ada aksi yang bisa di-undo.",
            )
            return

        tipe = action["tipe"]
        payload = action["payload"]

        try:
            if tipe == "tambah_barang":
                database.delete_barang(payload["id_barang"])
                self.avl_by_id.delete(payload["id_barang"])
                self.avl_by_name.delete(payload["nama_barang"].strip().lower())
            elif tipe == "tambah_batch":
                database.delete_batch(payload["id_batch"])
                batches = database.get_all_batch_aktif()
                self.alert_queue.rebuild(batches)
            else:
                QMessageBox.warning(
                    self,
                    "Undo",
                    f"Tipe aksi '{tipe}' tidak didukung untuk undo di halaman ini.",
                )
                self.action_stack.push(tipe, payload)
                return
        except KeyError:
            self.action_stack.push(tipe, payload)
            QMessageBox.critical(
                self,
                "Undo Gagal",
                "Data tidak ditemukan di AVL Tree. Undo dibatalkan.",
            )
            return

        self._mark_latest_log_undo(tipe)
        self.load_inventory()
        self.load_log()
        QMessageBox.information(
            self,
            "Undo Berhasil",
            f"Aksi '{_tipe_label(tipe)}' berhasil di-undo.",
        )

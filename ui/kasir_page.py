import time
from datetime import datetime

import database

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
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


class KasirPage(QWidget):
    def __init__(
        self, avl_by_id, avl_by_name, alert_queue, action_stack, user, main_window=None
    ):
        super().__init__()
        self.keranjang: list[dict] = []
        self.current_user = user
        self.avl_by_id = avl_by_id
        self.avl_by_name = avl_by_name
        self.alert_queue = alert_queue
        self.action_stack = action_stack
        self.main_window = main_window
        self.current_result = None

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Kasir — Point of Sale")
        title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        layout.addWidget(title)

        user_lbl = QLabel(f"Login sebagai: {self.current_user['username']}")
        user_lbl.setStyleSheet(f"font-size: 12px; color: {COLOR['text_muted']};")
        layout.addWidget(user_lbl)

        search_card = QFrame()
        search_card.setObjectName("card")
        search_layout = QVBoxLayout(search_card)
        search_layout.setContentsMargins(20, 16, 20, 16)
        search_layout.setSpacing(12)

        search_title = QLabel("🔍 Cari Barang (AVL Tree)")
        search_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        search_layout.addWidget(search_title)

        search_row = QHBoxLayout()
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("ID barang atau nama...")
        search_row.addWidget(self.input_search, 1)

        btn_cari = QPushButton("Cari")
        btn_cari.setObjectName("primaryBtn")
        btn_cari.setCursor(Qt.PointingHandCursor)
        btn_cari.clicked.connect(self.do_search)
        search_row.addWidget(btn_cari)
        search_layout.addLayout(search_row)

        self.lbl_avl_badge = QLabel()
        self.lbl_avl_badge.setObjectName("avlBadge")
        self.lbl_avl_badge.hide()
        search_layout.addWidget(self.lbl_avl_badge)

        self.lbl_search_result = QLabel()
        self.lbl_search_result.setStyleSheet(f"font-size: 13px; color: {COLOR['text_dark']};")
        self.lbl_search_result.hide()
        search_layout.addWidget(self.lbl_search_result)

        self.btn_add_to_cart = QPushButton("➕ Tambah ke Keranjang")
        self.btn_add_to_cart.setObjectName("primaryBtn")
        self.btn_add_to_cart.setCursor(Qt.PointingHandCursor)
        self.btn_add_to_cart.clicked.connect(self.add_to_cart)
        self.btn_add_to_cart.hide()
        search_layout.addWidget(self.btn_add_to_cart)

        layout.addWidget(search_card)

        cart_card = QFrame()
        cart_card.setObjectName("card")
        cart_layout = QVBoxLayout(cart_card)
        cart_layout.setContentsMargins(20, 16, 20, 16)
        cart_layout.setSpacing(12)

        cart_title = QLabel("🛒 Keranjang Belanja")
        cart_title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        cart_layout.addWidget(cart_title)

        self.tbl_keranjang = QTableWidget(0, 6)
        self.tbl_keranjang.setHorizontalHeaderLabels(
            ["No", "Nama Barang", "Harga Satuan", "Qty", "Subtotal", "Hapus"]
        )
        self.tbl_keranjang.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_keranjang.setAlternatingRowColors(True)
        self.tbl_keranjang.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_keranjang.verticalHeader().setVisible(False)
        hdr = self.tbl_keranjang.horizontalHeader()
        hdr.setStretchLastSection(True)
        hdr.resizeSection(0, 40)
        hdr.resizeSection(2, 120)
        hdr.resizeSection(3, 80)
        hdr.resizeSection(4, 120)
        hdr.resizeSection(5, 70)
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)
        cart_layout.addWidget(self.tbl_keranjang)
        layout.addWidget(cart_card, 1)

        total_bar = QHBoxLayout()
        total_lbl = QLabel("Total Pembayaran:")
        total_lbl.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {COLOR['text_dark']};"
        )
        total_bar.addWidget(total_lbl)

        self.lbl_total = QLabel(_format_rp(0))
        self.lbl_total.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {COLOR['primary']};"
        )
        total_bar.addWidget(self.lbl_total)
        total_bar.addStretch()

        self.btn_checkout = QPushButton("💳 Proses Bayar")
        self.btn_checkout.setObjectName("primaryBtn")
        self.btn_checkout.setFixedHeight(44)
        self.btn_checkout.setCursor(Qt.PointingHandCursor)
        self.btn_checkout.clicked.connect(self.do_checkout)
        total_bar.addWidget(self.btn_checkout)
        layout.addLayout(total_bar)

        self.input_search.returnPressed.connect(self.do_search)

    def _get_stok(self, id_barang: int) -> int:
        batches = database.get_batch_by_barang(id_barang)
        return sum(b["jumlah_stok"] for b in batches)

    def do_search(self) -> None:
        q = self.input_search.text().strip()
        if not q:
            return

        t_start = time.perf_counter()
        if q.isdigit():
            result = self.avl_by_id.search(int(q))
            found_list = [result] if result else []
        else:
            found_list = self.avl_by_name.search_prefix(q.lower())
        elapsed = (time.perf_counter() - t_start) * 1000

        if not found_list:
            self.lbl_avl_badge.hide()
            self.lbl_search_result.setText("❌ Barang tidak ditemukan")
            self.lbl_search_result.show()
            self.btn_add_to_cart.hide()
            self.current_result = None
            return

        self.lbl_avl_badge.setText(
            f"✓ Ditemukan via AVL Tree  |  {elapsed:.3f} ms"
        )
        self.lbl_avl_badge.show()

        barang = found_list[0]
        stok = self._get_stok(barang["id_barang"])

        if len(found_list) > 1:
            names = ", ".join(b["nama_barang"] for b in found_list[:5])
            extra = f" (+{len(found_list) - 5} lainnya)" if len(found_list) > 5 else ""
            self.lbl_search_result.setText(
                f"Ditemukan {len(found_list)} barang: {names}{extra}\n"
                f"Dipilih: {barang['nama_barang']} — "
                f"{_format_rp(barang['harga_satuan'])} | Stok: {stok}"
            )
        else:
            self.lbl_search_result.setText(
                f"{barang['nama_barang']} — "
                f"{_format_rp(barang['harga_satuan'])} | Stok tersisa: {stok}"
            )
        self.lbl_search_result.show()
        self.current_result = barang
        self.btn_add_to_cart.show()

        if self.main_window is not None and hasattr(self.main_window, "avl_visual_page"):
            found_key = int(q) if q.isdigit() else barang["nama_barang"].strip().lower()
            self.main_window.avl_visual_page.highlight_found_node(found_key)

    def add_to_cart(self) -> None:
        if self.current_result is None:
            return

        barang = self.current_result
        existing = next(
            (x for x in self.keranjang if x["id_barang"] == barang["id_barang"]),
            None,
        )
        if existing:
            existing["qty"] += 1
            existing["subtotal"] = existing["qty"] * existing["harga_satuan"]
        else:
            self.keranjang.append(
                {
                    "id_barang": barang["id_barang"],
                    "nama_barang": barang["nama_barang"],
                    "harga_satuan": barang["harga_satuan"],
                    "qty": 1,
                    "subtotal": barang["harga_satuan"],
                }
            )

        self.render_keranjang()
        self.input_search.clear()
        self.lbl_avl_badge.hide()
        self.lbl_search_result.hide()
        self.btn_add_to_cart.hide()
        self.current_result = None

    def render_keranjang(self) -> None:
        self.tbl_keranjang.setRowCount(0)
        for i, item in enumerate(self.keranjang):
            row = self.tbl_keranjang.rowCount()
            self.tbl_keranjang.insertRow(row)

            self.tbl_keranjang.setItem(row, 0, QTableWidgetItem(str(i + 1)))
            self.tbl_keranjang.setItem(
                row, 1, QTableWidgetItem(item["nama_barang"])
            )
            self.tbl_keranjang.setItem(
                row, 2, QTableWidgetItem(_format_rp(item["harga_satuan"]))
            )

            spin = QSpinBox()
            spin.setMinimum(1)
            spin.setMaximum(999)
            spin.blockSignals(True)
            spin.setValue(item["qty"])
            spin.blockSignals(False)
            id_barang = item["id_barang"]
            spin.valueChanged.connect(
                lambda qty, ib=id_barang: self.update_qty(ib, qty)
            )
            self.tbl_keranjang.setCellWidget(row, 3, spin)

            self.tbl_keranjang.setItem(
                row, 4, QTableWidgetItem(_format_rp(item["subtotal"]))
            )

            btn_del = QPushButton("✕")
            btn_del.setFixedWidth(36)
            btn_del.clicked.connect(
                lambda checked=False, ib=id_barang: self.remove_from_cart(ib)
            )
            self.tbl_keranjang.setCellWidget(row, 5, btn_del)

        self.update_total_label()

    def update_qty(self, id_barang: int, qty: int) -> None:
        for item in self.keranjang:
            if item["id_barang"] == id_barang:
                item["qty"] = qty
                item["subtotal"] = qty * item["harga_satuan"]
                break
        self.render_keranjang()

    def remove_from_cart(self, id_barang: int) -> None:
        self.keranjang = [x for x in self.keranjang if x["id_barang"] != id_barang]
        self.render_keranjang()

    def calculate_total(self) -> int:
        return sum(item["subtotal"] for item in self.keranjang)

    def update_total_label(self) -> None:
        self.lbl_total.setText(_format_rp(self.calculate_total()))

    def do_checkout(self) -> None:
        if not self.keranjang:
            QMessageBox.warning(self, "Keranjang Kosong", "Keranjang masih kosong.")
            return

        detail_list: list[dict] = []
        for item in self.keranjang:
            batches = database.get_batch_by_barang(item["id_barang"])
            remaining = item["qty"]
            for batch in batches:
                if remaining <= 0:
                    break
                take = min(remaining, batch["jumlah_stok"])
                detail_list.append(
                    {
                        "id_barang": item["id_barang"],
                        "id_batch": batch["id_batch"],
                        "qty": take,
                        "harga_satuan": item["harga_satuan"],
                    }
                )
                remaining -= take
            if remaining > 0:
                QMessageBox.critical(
                    self,
                    "Stok Tidak Cukup",
                    f"Stok tidak mencukupi untuk {item['nama_barang']}.",
                )
                return

        tgl_waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = self.calculate_total()

        try:
            id_transaksi = database.insert_transaksi(
                tgl_waktu,
                total,
                self.current_user["id_user"],
                detail_list,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Transaksi Gagal",
                f"Gagal menyimpan transaksi:\n{exc}",
            )
            return

        self.action_stack.push(
            "checkout", {"id_transaksi": id_transaksi, "total": total}
        )
        database.insert_action_log("checkout", {"id_transaksi": id_transaksi})

        dialog = QDialog(self)
        dialog.setWindowTitle("Transaksi Berhasil!")
        dialog.setMinimumWidth(420)
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setSpacing(12)
        dlg_layout.setContentsMargins(24, 24, 24, 24)

        dlg_layout.addWidget(
            QLabel(f"<b>ID Transaksi:</b> #{id_transaksi}")
        )
        dlg_layout.addWidget(QLabel(f"<b>Waktu:</b> {tgl_waktu}"))
        dlg_layout.addWidget(
            QLabel(f"<b>Total:</b> {_format_rp(total)}")
        )

        items_lbl = QLabel("<b>Detail Pembelian:</b>")
        dlg_layout.addWidget(items_lbl)
        for item in self.keranjang:
            line = QLabel(
                f"• {item['nama_barang']} × {item['qty']} = "
                f"{_format_rp(item['subtotal'])}"
            )
            dlg_layout.addWidget(line)

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("primaryBtn")
        btn_ok.setFixedHeight(40)

        def on_ok() -> None:
            self.keranjang.clear()
            self.render_keranjang()
            dialog.accept()

        btn_ok.clicked.connect(on_ok)
        dlg_layout.addWidget(btn_ok)
        dialog.exec_()

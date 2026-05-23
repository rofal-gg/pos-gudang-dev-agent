---
name: pos-gudang-dev-agent
description: >
  Gunakan skill ini untuk SEMUA tugas pengembangan pada project POS & Gudang —
  membuat aplikasi desktop PyQt5, logika AVL Tree, Priority Queue, Stack ADT,
  query SQLite, visualisasi pohon AVL menggunakan QPainter, dan tabel PyQt5.
  Aktifkan setiap kali user meminta membuat, mengedit, atau memperbaiki file
  apapun di dalam codebase project ini.
project: Sistem POS (Kasir) & Manajemen Gudang (Tugas Struktur Data)
stack: Python 3, PyQt5, SQLite3
authors: Kelompok 4 orang
---

# POS & Gudang Dev Agent — Master SKILL.md (PyQt5 Edition)

---

## 1. Project Identity

| Key | Value |
|---|---|
| **Nama Project** | Sistem POS & Manajemen Gudang — Desktop App |
| **Tujuan** | Implementasi multi-ADT (AVL Tree, Priority Queue, Stack) + SQLite untuk tugas Struktur Data |
| **Stack** | Python 3 + PyQt5 + SQLite3 — **murni desktop, tanpa web server, tanpa framework** |
| **Library Diizinkan** | `PyQt5`, `sqlite3`, `hashlib`, `heapq`, `datetime`, `os` — bebas pip install |
| **Framework DILARANG** | Flask, Django, FastAPI, Flet, Streamlit — apapun yang mengontrol alur aplikasi |
| **Database** | SQLite3 (file lokal `app.db`) |
| **Struktur Data Utama** | **AVL Tree** — indexing katalog barang in-memory |
| **Struktur Data Pendukung** | **Min-Heap (Priority Queue)** — expiry alert; **Stack** — log & undo aksi |
| **Fitur Unggulan** | Visualisasi AVL Tree live menggunakan `QPainter` PyQt5 — update real-time |
| **Arsitektur** | Monolitik desktop: UI (PyQt5) memanggil ADT dan database langsung, tanpa HTTP |
| **Deployment** | Lokal, jalan dengan `python main.py`, 100% offline |

---

## 2. ATURAN EKSEKUSI WAJIB — Anti-Halusinasi

> **Baca dan pahami semua aturan ini sebelum menulis satu baris kode pun.**

### Aturan A — Permintaan Fitur Multi-Komponen

Jika diminta fitur kompleks yang menyentuh lebih dari satu file, **DILARANG** menulis semua kode sekaligus dalam satu respons.

#### Fase 1: Konfirmasi Rencana (ZERO KODE)
1. Ulangi secara ringkas alur logika yang diminta.
2. Sebutkan file mana saja yang akan dibuat atau diedit.
3. Sebutkan query SQL yang akan dieksekusi.
4. Sebutkan apakah data melewati AVL Tree, Priority Queue, atau Stack.
5. **Tunggu persetujuan user** sebelum lanjut ke Fase 2.

#### Fase 2: Eksekusi Modular (urutan wajib)
1. ADT terlebih dahulu (`avl_tree.py`, `priority_queue.py`, `stack.py`) jika ada perubahan logika.
2. `database.py` jika ada perubahan schema atau query.
3. UI Page (`ui/kasir_page.py`, dll) untuk binding data.
4. `ui/main_window.py` jika ada perubahan navigasi.
5. `main.py` hanya disentuh jika ada perubahan inisialisasi global.

### Aturan B — Integritas Tipe Data AVL Tree

- Key AVL Tree `id_barang` → **WAJIB INTEGER MURNI**.
- Key AVL Tree `nama_barang` → **WAJIB string lowercase**: `nama.strip().lower()`.
- Dua instance terpisah: `avl_by_id` (int key) dan `avl_by_name` (str key).
- Jangan pernah mencampur tipe key dalam satu pohon.

### Aturan C — Tidak Ada Web Server

- **DILARANG**: `http.server`, Flask, FastAPI, socket server, atau apapun yang membuka port HTTP.
- UI PyQt5 memanggil fungsi Python secara langsung — bukan via HTTP request.
- Tidak ada `fetch()`, tidak ada JSON API, tidak ada `localhost:8080`.

### Aturan D — PyQt5 UI Rules

- Setiap halaman adalah class turunan dari `QWidget`.
- Navigasi antar halaman menggunakan `QStackedWidget` di `main_window.py`.
- Tabel data menggunakan `QTableWidget` — bukan HTML table.
- Visualisasi AVL Tree menggunakan `QPainter` di class `AVLVisualWidget(QWidget)`.
- Semua operasi database yang berat dijalankan di `QThread` agar UI tidak freeze.
- Signal & slot digunakan untuk komunikasi antar komponen.

### Aturan E — Semua Fitur Harus Demo-Ready

Tidak boleh ada fitur setengah jadi. Jika sebuah fitur belum selesai, sembunyikan tombolnya dari UI. Lebih baik fitur sedikit tapi semua berjalan sempurna saat demo.

### Aturan F — Warna & Style PyQt5

Gunakan `setStyleSheet()` untuk styling. Warna mengacu pada Design System di Section 7.
Jangan pernah hardcode warna di luar konstanta yang sudah didefinisikan.

---

## 3. Struktur Folder Project

```
pos_gudang_project/
│
├── main.py                    # Entry point: inisialisasi ADT + jalankan QApplication
├── avl_tree.py                # Class AVLTree (insert, search, delete, to_snapshot)
├── priority_queue.py          # Class ExpiredAlertQueue (MinHeap via heapq)
├── stack.py                   # Class ActionStack (LIFO, log & undo)
├── database.py                # SQLite3 CRUD + setup schema + seed data
├── app.db                     # File database (auto-generated)
├── requirements.txt           # Isi: PyQt5
├── README.md                  # Dokumentasi + cara run + argumen AVL Tree
│
└── ui/
    ├── main_window.py         # QMainWindow: sidebar + QStackedWidget
    ├── login_page.py          # QWidget: form login
    ├── kasir_page.py          # QWidget: POS kasir + keranjang belanja
    ├── gudang_page.py         # QWidget: manajemen barang & batch stok
    ├── dashboard_page.py      # QWidget: alert expiry + stok tipis + action log
    └── avl_visual_widget.py   # QWidget custom: render AVL Tree dengan QPainter
```

---

## 4. Arsitektur Aplikasi — Alur Data

```
[main.py]
    │
    ├─ Inisialisasi database.setup_schema()
    ├─ Inisialisasi database.seed_sample_data()
    ├─ Load semua barang → avl_by_id.insert() + avl_by_name.insert()
    ├─ Load semua batch aktif → alert_queue.rebuild()
    ├─ Inisialisasi action_stack = ActionStack()
    │
    └─ QApplication → MainWindow
            │
            ├─ LoginPage
            │       └─ database.verify_login() → set session → pindah ke halaman utama
            │
            ├─ KasirPage
            │       ├─ avl_by_id.search(int) atau avl_by_name.search_prefix(str)
            │       ├─ database.get_batch_by_barang() → FIFO stok
            │       ├─ database.insert_transaksi() → potong stok
            │       └─ action_stack.push('checkout', payload)
            │
            ├─ GudangPage
            │       ├─ database.get_inventory() → QTableWidget
            │       ├─ database.insert_barang() → avl_by_id.insert() + avl_by_name.insert()
            │       ├─ database.insert_batch() → alert_queue.push()
            │       └─ action_stack.pop() → undo → rebuild ADT
            │
            ├─ DashboardPage
            │       ├─ alert_queue.get_top_n(10) → QTableWidget expiry
            │       ├─ database.get_alerts() → stok tipis
            │       └─ action_stack.to_list() → QTableWidget log
            │
            └─ AVLVisualWidget
                    ├─ avl_by_id.to_snapshot() → render QPainter
                    └─ avl_by_name.to_snapshot() → render QPainter
```

---

## 5. Peta Fitur Per Halaman

### Halaman 1 — Login (`login_page.py`)

| Komponen | PyQt5 Widget | Logika |
|---|---|---|
| Input username | `QLineEdit` | — |
| Input password | `QLineEdit` (echoMode Password) | — |
| Tombol Masuk | `QPushButton` | `database.verify_login()` → SHA-256 |
| Pesan error | `QLabel` (hidden/shown) | Tampil jika login gagal |

Role `admin` → tampilkan GudangPage dan DashboardPage di sidebar.
Role `kasir` → tampilkan KasirPage saja.

---

### Halaman 2 — Kasir (`kasir_page.py`)

| Komponen | PyQt5 Widget | ADT |
|---|---|---|
| Input cari barang | `QLineEdit` + `QPushButton` | **AVL Tree** |
| Badge hasil AVL | `QLabel` styled | Tampil "✓ AVL Tree \| 0.12ms" |
| Tabel keranjang | `QTableWidget` | — |
| Qty per baris | `QSpinBox` di dalam tabel | — |
| Total harga | `QLabel` besar | — |
| Tombol Bayar | `QPushButton` | FIFO batch + Stack |
| Dialog struk | `QDialog` | Tampil setelah checkout sukses |

**Logika Search:**
- Input angka → `avl_by_id.search(int(q))`
- Input teks → `avl_by_name.search_prefix(q.lower())`
- Tampilkan waktu pencarian dalam ms menggunakan `time.perf_counter()`

**Logika Checkout (FIFO):**
1. Untuk setiap item keranjang, ambil batch order `tgl_expired ASC`.
2. Potong stok dari batch terlama sampai qty terpenuhi.
3. Panggil `database.insert_transaksi()`.
4. Push ke `action_stack`.

---

### Halaman 3 — Gudang (`gudang_page.py`)

| Komponen | PyQt5 Widget | ADT |
|---|---|---|
| Tabel inventory | `QTableWidget` | — |
| Highlight stok tipis | Row background merah muda | — |
| Form tambah barang | `QFormLayout` + `QLineEdit` | **AVL Tree** insert |
| Form tambah batch | `QFormLayout` + `QDateEdit` | Priority Queue push |
| Tombol Undo | `QPushButton` | **Stack** pop |
| Tabel action log | `QTableWidget` | Stack to_list |

---

### Halaman 4 — Dashboard (`dashboard_page.py`)

| Komponen | PyQt5 Widget | ADT |
|---|---|---|
| Card summary | `QFrame` styled | — |
| Tabel expiry alert | `QTableWidget` | **Min-Heap** get_top_n |
| Label penjelasan heap | `QLabel` italic | Edukasi untuk dosen |
| Tabel stok tipis | `QTableWidget` | SQLite query |
| Tabel action log | `QTableWidget` | **Stack** to_list |
| Label penjelasan stack | `QLabel` italic | Edukasi untuk dosen |

---

### Halaman 5 — Visualisasi AVL (`avl_visual_widget.py`)

| Komponen | PyQt5 Widget | Deskripsi |
|---|---|---|
| Canvas pohon | `QWidget` + `QPainter` | Render node & edge rekursif |
| Toggle ID / Nama | `QRadioButton` | Ganti antara dua pohon |
| Tombol Refresh | `QPushButton` | Reload snapshot & repaint |
| Info node | `QLabel` | Klik node → tampil detail |
| Legend warna | `QLabel` dengan warna | Default / Baru / Ditemukan |

**Rendering Algorithm (QPainter):**
1. Traverse `to_snapshot()` rekursif untuk hitung posisi (x, y) tiap node.
2. Root di tengah-atas. Level spacing: 80px vertikal.
3. Horizontal spacing: bagi lebar canvas proporsional per subtree.
4. Gambar edge dulu (`painter.drawLine`) warna `#94a3b8`.
5. Gambar node sebagai `painter.drawEllipse` radius 28px.
6. Tulis key di dalam node (`painter.drawText`) warna putih.
7. Tulis balance factor di bawah node, font kecil.
8. Node baru → highlight kuning `#f59e0b` selama 2 detik (`QTimer`).
9. Node hasil search → highlight hijau `#10b981`.

---

## 6. Schema Database SQLite (`database.py`)

### ERD Relasi Antar Tabel

```
users ──────────────────────── transaksi
(id_user)                      (id_kasir FK)
                                    │
                               detail_transaksi
                               (id_transaksi FK)
                               (id_barang FK)
                               (id_batch FK)
                                    │
barang ─────────────────────── batch_stok
(id_barang PK)                 (id_barang FK)
    │                          (id_batch PK)
    └── AVL Tree key ──────────────────────
                                    │
                               action_log
                               (payload JSON)
```

### DDL Lengkap

```sql
-- Tabel 1: Pengguna sistem
CREATE TABLE IF NOT EXISTS users (
    id_user       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    UNIQUE NOT NULL,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL CHECK(role IN ('admin', 'kasir'))
);

-- Tabel 2: Katalog barang (key AVL Tree)
CREATE TABLE IF NOT EXISTS barang (
    id_barang    INTEGER PRIMARY KEY,   -- int key untuk avl_by_id
    nama_barang  TEXT    NOT NULL,      -- str key untuk avl_by_name
    harga_satuan INTEGER NOT NULL CHECK(harga_satuan > 0)
);

-- Tabel 3: Batch stok gudang (FIFO + expiry)
CREATE TABLE IF NOT EXISTS batch_stok (
    id_batch    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_barang   INTEGER NOT NULL,
    jumlah_stok INTEGER NOT NULL DEFAULT 0 CHECK(jumlah_stok >= 0),
    tgl_masuk   TEXT    NOT NULL,   -- format: 'YYYY-MM-DD'
    tgl_expired TEXT    NOT NULL,   -- format: 'YYYY-MM-DD'
    FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
);

-- Tabel 4: Header transaksi
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    tgl_waktu    TEXT    NOT NULL,  -- format: 'YYYY-MM-DD HH:MM:SS'
    total_harga  INTEGER NOT NULL CHECK(total_harga > 0),
    id_kasir     INTEGER NOT NULL,
    FOREIGN KEY (id_kasir) REFERENCES users(id_user)
);

-- Tabel 5: Detail isi transaksi (per item per batch)
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id_detail    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER NOT NULL,
    id_barang    INTEGER NOT NULL,
    id_batch     INTEGER NOT NULL,
    qty          INTEGER NOT NULL CHECK(qty > 0),
    harga_satuan INTEGER NOT NULL,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
    FOREIGN KEY (id_barang)    REFERENCES barang(id_barang),
    FOREIGN KEY (id_batch)     REFERENCES batch_stok(id_batch)
);

-- Tabel 6: Log aksi untuk Stack ADT
CREATE TABLE IF NOT EXISTS action_log (
    id_log      INTEGER PRIMARY KEY AUTOINCREMENT,
    tgl_waktu   TEXT    NOT NULL,
    tipe_aksi   TEXT    NOT NULL,  -- 'tambah_barang'|'tambah_batch'|'checkout'|'hapus_barang'
    payload     TEXT    NOT NULL,  -- JSON string dari data sebelum aksi
    sudah_undo  INTEGER DEFAULT 0  -- 0=aktif, 1=sudah di-undo
);
```

### Query Penting

```sql
-- Ambil total stok per barang (untuk tabel inventory)
SELECT br.id_barang,
       br.nama_barang,
       br.harga_satuan,
       COALESCE(SUM(bs.jumlah_stok), 0) AS sisa_stok_total
FROM barang br
LEFT JOIN batch_stok bs ON br.id_barang = bs.id_barang
GROUP BY br.id_barang
ORDER BY br.id_barang;

-- Ambil batch FIFO (untuk checkout — expired paling dekat duluan)
SELECT id_batch, jumlah_stok, tgl_expired
FROM batch_stok
WHERE id_barang = ? AND jumlah_stok > 0
ORDER BY tgl_expired ASC;

-- Ambil batch aktif untuk rebuild Priority Queue
SELECT bs.id_batch,
       bs.id_barang,
       br.nama_barang,
       bs.jumlah_stok,
       bs.tgl_expired
FROM batch_stok bs
JOIN barang br ON bs.id_barang = br.id_barang
WHERE bs.jumlah_stok > 0
ORDER BY bs.tgl_expired ASC;

-- Barang dengan stok tipis (<= 10 unit total)
SELECT br.id_barang,
       br.nama_barang,
       COALESCE(SUM(bs.jumlah_stok), 0) AS sisa_stok_total
FROM barang br
LEFT JOIN batch_stok bs ON br.id_barang = bs.id_barang
GROUP BY br.id_barang
HAVING sisa_stok_total <= 10
ORDER BY sisa_stok_total ASC;

-- Batch yang expired dalam 7 hari ke depan
SELECT bs.id_batch,
       br.nama_barang,
       bs.tgl_expired,
       bs.jumlah_stok,
       CAST(julianday(bs.tgl_expired) - julianday('now') AS INTEGER) AS sisa_hari
FROM batch_stok bs
JOIN barang br ON bs.id_barang = br.id_barang
WHERE bs.jumlah_stok > 0
  AND julianday(bs.tgl_expired) - julianday('now') <= 7
ORDER BY sisa_hari ASC;
```

---

## 7. Design System PyQt5

### Konstanta Warna (definisikan di `main_window.py`)

```python
COLOR = {
    # Primary
    "primary":       "#6366f1",
    "primary_hover": "#4f46e5",
    "primary_light": "#e0e7ff",

    # Background
    "bg_main":       "#f8fafc",
    "bg_card":       "#ffffff",
    "bg_sidebar":    "#1e1b4b",

    # Teks
    "text_dark":     "#1e293b",
    "text_muted":    "#64748b",
    "text_sidebar":  "#c7d2fe",

    # Border
    "border":        "#e2e8f0",

    # Status
    "success_bg":    "#dcfce7",
    "success_text":  "#166534",
    "warning_bg":    "#fef3c7",
    "warning_text":  "#92400e",
    "danger_bg":     "#fee2e2",
    "danger_text":   "#991b1b",

    # AVL Node
    "node_default":  "#6366f1",
    "node_new":      "#f59e0b",
    "node_found":    "#10b981",
    "node_line":     "#94a3b8",
    "node_text":     "#ffffff",
}
```

### StyleSheet Utama (QSS)

```python
MAIN_STYLE = """
QMainWindow, QWidget#mainWidget {
    background-color: #f8fafc;
}
QWidget#sidebar {
    background-color: #1e1b4b;
    min-width: 220px;
    max-width: 220px;
}
QPushButton#navButton {
    background: transparent;
    color: #c7d2fe;
    text-align: left;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
}
QPushButton#navButton:hover {
    background-color: rgba(99,102,241,0.3);
    color: #ffffff;
}
QPushButton#navButton[active=true] {
    background-color: #6366f1;
    color: #ffffff;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #e2e8f0;
    font-size: 13px;
}
QTableWidget::item:selected {
    background-color: #e0e7ff;
    color: #1e293b;
}
QHeaderView::section {
    background-color: #f8fafc;
    color: #64748b;
    font-weight: bold;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #e2e8f0;
}
QLineEdit, QSpinBox, QDateEdit, QComboBox {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 10px;
    background: #ffffff;
    font-size: 13px;
    color: #1e293b;
}
QLineEdit:focus, QSpinBox:focus, QDateEdit:focus {
    border-color: #6366f1;
}
QPushButton#primaryBtn {
    background-color: #6366f1;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#primaryBtn:hover {
    background-color: #4f46e5;
}
QPushButton#dangerBtn {
    background-color: #fee2e2;
    color: #991b1b;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
}
QLabel#avlBadge {
    background-color: #dcfce7;
    color: #166534;
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: bold;
}
QFrame#card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}
"""
```

---

## 8. Implementasi ADT — Ringkasan Interface

### AVLTree (`avl_tree.py`)
```python
class AVLTree:
    def insert(self, key, data: dict) -> None
    def search(self, key) -> dict | None
    def search_prefix(self, prefix: str) -> list[dict]   # hanya untuk str tree
    def delete(self, key) -> None
    def to_snapshot(self) -> dict | None                  # untuk QPainter render
    # Private helpers:
    def _rotate_left(self, node) -> AVLNode
    def _rotate_right(self, node) -> AVLNode
    def _get_height(self, node) -> int
    def _get_balance(self, node) -> int
    def _update_height(self, node) -> None
```

### ExpiredAlertQueue (`priority_queue.py`)
```python
class ExpiredAlertQueue:
    def push(self, tgl_expired: str, id_batch: int, nama_barang: str, jumlah_stok: int) -> None
    def pop(self) -> dict | None
    def peek(self) -> dict | None
    def get_top_n(self, n: int) -> list[dict]
    def rebuild(self, items: list[dict]) -> None
    def size(self) -> int
```

### ActionStack (`stack.py`)
```python
class ActionStack:
    def push(self, tipe: str, payload: dict) -> None
    def pop(self) -> dict | None
    def peek(self) -> dict | None
    def is_empty(self) -> bool
    def size(self) -> int
    def to_list(self) -> list[dict]   # untuk ditampilkan di UI
```

---

## 9. Alur Inisialisasi (`main.py`)

```
python main.py
      │
      ▼
database.setup_schema()      ← buat tabel jika belum ada
database.seed_sample_data()  ← isi data contoh jika tabel kosong
      │
      ▼
avl_by_id   = AVLTree()
avl_by_name = AVLTree()
rows = database.get_all_barang()
for row in rows:
    avl_by_id.insert(row['id_barang'], row)
    avl_by_name.insert(row['nama_barang'].lower(), row)
      │
      ▼
alert_queue = ExpiredAlertQueue()
batches = database.get_all_batch_aktif()
alert_queue.rebuild(batches)
      │
      ▼
action_stack = ActionStack()
      │
      ▼
app = QApplication(sys.argv)
window = MainWindow(avl_by_id, avl_by_name, alert_queue, action_stack)
window.show()
sys.exit(app.exec_())
```

---

## 10. Seed Data untuk Demo (`database.py`)

```python
# ID dipilih tidak berurutan agar rotasi AVL terlihat saat insert
SAMPLE_BARANG = [
    (101, 'Susu Kotak',      5000),
    (103, 'Yogurt Stroberi', 12000),
    (102, 'Teh Botol',       4000),
    (107, 'Jus Jeruk',       8000),
    (105, 'Air Mineral',     3000),
    (110, 'Kopi Sachet',     2500),
    (104, 'Biskuit Coklat',  7500),
    (108, 'Mie Instan',      3500),
    (106, 'Sabun Mandi',     6000),
    (109, 'Shampo Sachet',   4500),
]
# Beberapa batch dibuat expired dalam 3-5 hari (untuk demo Priority Queue & alert)
# Beberapa batch dibuat stok <= 5 unit (untuk demo stok tipis)
```

---

## 11. Anti-Pattern — Larangan Keras

| ❌ Jangan | ✅ Harus |
|---|---|
| Import `flask`, `fastapi`, `streamlit`, `flet` | Hanya `PyQt5`, built-in Python |
| Buka HTTP server / port apapun | UI langsung panggil fungsi Python |
| `id_barang = "BRG001"` (string) | `id_barang = 1001` (integer) |
| Satu file monolitik semua kode | Pisah per file sesuai struktur folder |
| Visualisasi pakai gambar statis | `QPainter` render dari `to_snapshot()` |
| ORDER BY SQL untuk expiry alert | `heapq` Python → `ExpiredAlertQueue` |
| Password plain text | `hashlib.sha256(...).hexdigest()` |
| UI freeze saat query berat | Gunakan `QThread` untuk operasi panjang |
| Fitur setengah jadi | Sembunyikan dari UI jika belum selesai |

---

## 12. Argumen Presentasi (Hafalkan)

**Mengapa AVL Tree bukan B-Tree?**
> "Kami memilih AVL Tree karena data katalog barang di-load ke RAM saat aplikasi start. Untuk pencarian in-memory, AVL Tree memberikan O(log n) yang optimal. B-Tree dirancang untuk meminimalkan disk I/O — fungsi yang sudah ditangani SQLite secara internal. AVL Tree juga lebih mudah divisualisasikan sebagai binary tree, sehingga kami bisa menampilkan rotasi LL, RR, LR, RL secara live kepada audiens."

**Mengapa PyQt5 bukan web?**
> "PyQt5 adalah library GUI, bukan framework. Alur program sepenuhnya kami kontrol. Tidak ada server yang dijalankan, tidak ada HTTP request — UI langsung memanggil fungsi ADT dan database. Ini justru lebih bersih untuk demonstrasi alur data struktur."

**Mengapa 3 ADT?**
> "AVL Tree untuk pencarian cepat O(log n). Min-Heap sebagai Priority Queue untuk mengurutkan expiry alert tanpa sorting manual — kompleksitas insert O(log n), peek O(1). Stack untuk mencatat riwayat aksi dan mendukung operasi undo LIFO. Masing-masing ADT menyelesaikan masalah yang berbeda dan saling melengkapi."

---

## 13. Pembagian Kerja (4 Orang)

| Person | Tanggung Jawab | File |
|---|---|---|
| **P1** | AVL Tree + Widget Visualisasi | `avl_tree.py`, `ui/avl_visual_widget.py` |
| **P2** | Database + Priority Queue + Stack | `database.py`, `priority_queue.py`, `stack.py` |
| **P3** | Main Window + Login + Dashboard | `main.py`, `ui/main_window.py`, `ui/login_page.py`, `ui/dashboard_page.py` |
| **P4** | Kasir Page + Gudang Page | `ui/kasir_page.py`, `ui/gudang_page.py` |

> **Sinkronisasi wajib:** P1 dan P3 harus sepakati format return `to_snapshot()` sebelum mulai coding `avl_visual_widget.py`.
> P2 dan P3/P4 harus sepakati signature semua fungsi `database.py` sebelum UI mulai memanggil database.

---

## 14. Checklist Demo-Ready

- [ ] `pip install PyQt5` berhasil, `python main.py` jalan tanpa error
- [ ] Login admin dan kasir berhasil, role routing benar
- [ ] Kasir: search by ID → muncul data + label "✓ AVL Tree | Xms"
- [ ] Kasir: search by nama prefix → muncul hasil dari AVL traversal
- [ ] Kasir: checkout → stok terpotong FIFO, struk muncul
- [ ] Gudang: tambah barang → tabel update + node masuk AVL Tree
- [ ] Visualisasi: pohon tergambar dengan node, edge, dan balance factor
- [ ] Visualisasi: node baru highlight kuning 2 detik setelah insert
- [ ] Dashboard: tabel expiry dari Min-Heap, label "Priority Queue" terlihat
- [ ] Dashboard: tabel stok tipis muncul
- [ ] Gudang: tombol Undo berfungsi, aksi terakhir dibatalkan
- [ ] Tidak ada crash saat demo semua fitur

# Sistem POS & Manajemen Gudang

## Tugas Matakuliah Struktur Data

Aplikasi desktop **Python 3 + PyQt5 + SQLite3** untuk demonstrasi tiga struktur data (AVL Tree, Min-Heap Priority Queue, Stack) pada sistem kasir dan manajemen gudang. Berjalan 100% offline dengan `python main.py`.

### Tim (4 orang)

| Nama | NIM | Peran |
|------|-----|-------|
| *(isi nama)* | *(isi NIM)* | P1 — AVL Tree & visualisasi (`avl_tree.py`, `ui/avl_visual_widget.py`) |
| *(isi nama)* | *(isi NIM)* | P2 — Database, Priority Queue, Stack (`database.py`, `priority_queue.py`, `stack.py`) |
| *(isi nama)* | *(isi NIM)* | P3 — Main window, login, dashboard (`main.py`, `ui/main_window.py`, `ui/login_page.py`, `ui/dashboard_page.py`) |
| *(isi nama)* | *(isi NIM)* | P4 — Halaman kasir & gudang (`ui/kasir_page.py`, `ui/gudang_page.py`) |

### Cara Menjalankan

1. Pastikan Python 3 terpasang.
2. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
   atau:
   ```bash
   pip install PyQt5
   ```
3. Jalankan aplikasi dari root project:
   ```bash
   python main.py
   ```
   Schema SQLite dan data contoh di-seed otomatis saat pertama kali dijalankan (`app.db`).

### Akun Demo

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | Admin |
| kasir1   | kasir123  | Kasir |

### Struktur Data yang Diimplementasi

#### 1. AVL Tree (`avl_tree.py`)

Digunakan untuk indexing katalog barang di in-memory.

- `avl_by_id`: key = **INTEGER** `id_barang`
- `avl_by_name`: key = **STRING** `nama_barang` (lowercase)
- Operasi: insert O(log n), search O(log n), delete O(log n)
- **Mengapa AVL bukan B-Tree:** Katalog barang di-load ke RAM saat aplikasi start. Untuk pencarian in-memory, AVL Tree memberikan O(log n) yang optimal. B-Tree dirancang untuk meminimalkan disk I/O — fungsi yang sudah ditangani SQLite secara internal. AVL Tree juga lebih mudah divisualisasikan sebagai binary tree, sehingga rotasi LL, RR, LR, RL dapat ditampilkan secara live kepada audiens.
- **Visualisasi:** halaman khusus dengan `QPainter` (`ui/avl_visual_widget.py`)

#### 2. Min-Heap Priority Queue (`priority_queue.py`)

Digunakan untuk mengurutkan expiry alert tanpa SQL `ORDER BY`.

- Implementasi: Python `heapq` (`ExpiredAlertQueue`)
- Insert O(log n), peek O(1)
- Key: `tgl_expired` (format `YYYY-MM-DD`)

#### 3. Stack ADT (`stack.py`)

Digunakan untuk log aksi dan operasi Undo (LIFO).

- Push setiap aksi tambah barang, tambah batch, checkout
- Pop untuk membatalkan aksi terakhir
- Sinkron dengan tabel `action_log` di SQLite

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id_user       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    UNIQUE NOT NULL,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL CHECK(role IN ('admin','kasir'))
);

CREATE TABLE IF NOT EXISTS barang (
    id_barang    INTEGER PRIMARY KEY,
    nama_barang  TEXT    NOT NULL,
    harga_satuan INTEGER NOT NULL CHECK(harga_satuan > 0)
);

CREATE TABLE IF NOT EXISTS batch_stok (
    id_batch    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_barang   INTEGER NOT NULL,
    jumlah_stok INTEGER NOT NULL DEFAULT 0 CHECK(jumlah_stok >= 0),
    tgl_masuk   TEXT    NOT NULL,
    tgl_expired TEXT    NOT NULL,
    FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
);

CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    tgl_waktu    TEXT    NOT NULL,
    total_harga  INTEGER NOT NULL CHECK(total_harga > 0),
    id_kasir     INTEGER NOT NULL,
    FOREIGN KEY (id_kasir) REFERENCES users(id_user)
);

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

CREATE TABLE IF NOT EXISTS action_log (
    id_log     INTEGER PRIMARY KEY AUTOINCREMENT,
    tgl_waktu  TEXT    NOT NULL,
    tipe_aksi  TEXT    NOT NULL,
    payload    TEXT    NOT NULL,
    sudah_undo INTEGER DEFAULT 0
);
```

### Struktur Folder

```
pos-gudang-dev-agent/
│
├── main.py                    # Entry point: inisialisasi ADT + QApplication
├── avl_tree.py                # Class AVLTree (insert, search, delete, to_snapshot)
├── priority_queue.py          # Class ExpiredAlertQueue (MinHeap via heapq)
├── stack.py                   # Class ActionStack (LIFO, log & undo)
├── database.py                # SQLite3 CRUD + setup schema + seed data
├── app.db                     # File database (auto-generated)
├── requirements.txt           # PyQt5
├── README.md
│
└── ui/
    ├── __init__.py
    ├── main_window.py         # QMainWindow: sidebar + QStackedWidget
    ├── login_page.py          # Form login
    ├── kasir_page.py          # POS kasir + keranjang belanja
    ├── gudang_page.py         # Manajemen barang & batch stok
    ├── dashboard_page.py      # Alert expiry + stok tipis + action log
    └── avl_visual_widget.py   # Render AVL Tree dengan QPainter
```

### Tips Demo

- Jangan hapus `app.db` setelah seed agar data demo konsisten.
- Saat presentasi, tambah barang dengan ID baru (mis. 120, 125) lalu buka visualisasi AVL sebelum/sesudah insert.
- Pada halaman kasir, tunjukkan label **"✓ Via AVL Tree | X ms"** saat pencarian barang.

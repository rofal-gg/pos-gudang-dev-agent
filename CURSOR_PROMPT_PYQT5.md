# 🚀 CURSOR MASTER PROMPT — POS & Gudang PyQt5 (0% → 100%)
# Tempel setiap prompt sesuai urutan tahap.
# WAJIB: tunggu setiap tahap selesai & bisa dijalankan sebelum lanjut ke tahap berikutnya.
# Cara jalankan: python main.py

---

## ╔══════════════════════════════════════════╗
## ║   LANGKAH PERTAMA — Setup .cursorrules   ║
## ╚══════════════════════════════════════════╝

Buat file `.cursorrules` di root folder project, isi dengan teks berikut PERSIS:

```
You are a senior Python developer building a university Data Structures desktop application.

IDENTITY:
- This is a PyQt5 desktop app, NOT a web app.
- There is NO web server, NO HTTP, NO localhost port, NO fetch(), NO JSON API.
- The UI (PyQt5) calls Python functions directly. That is the only communication pattern.

HARD RULES — never violate these:

1. STACK: Python 3 + PyQt5 + SQLite3 only.
   - pip install PyQt5 is the ONLY allowed installation.
   - FORBIDDEN frameworks: Flask, Django, FastAPI, Flet, Streamlit, http.server.
   - Built-in allowed: sqlite3, hashlib, heapq, datetime, os, time, json, sys.

2. AVL TREE TYPES:
   - avl_by_id uses INTEGER keys only. Never strings.
   - avl_by_name uses lowercase STRING keys only. Never integers.
   - Never mix types in one tree instance.
   - Two separate AVLTree instances always.

3. PYQT5 UI RULES:
   - Every page = class inheriting QWidget.
   - Navigation = QStackedWidget in main_window.py.
   - All tables = QTableWidget. Never HTML.
   - AVL visualization = QPainter inside a QWidget subclass.
   - Heavy operations = QThread so the UI never freezes.
   - Inter-component communication = PyQt5 signals and slots.

4. DATA FLOW:
   - UI page calls database.py functions directly.
   - UI page calls avl_tree.py methods directly.
   - No intermediary layer, no HTTP, no serialization.

5. SECURITY:
   - Passwords stored as hashlib.sha256(pwd.encode()).hexdigest() only.
   - Never store plain text passwords.

6. COLORS: Always use the COLOR dict defined in main_window.py. Never hardcode hex values
   outside that dict.

7. MODULARITY: One responsibility per file. Never put database logic inside UI files.
   Never put UI logic inside database.py.

8. DEMO-READY: Every feature must fully work. Do not write placeholder functions
   or TODO stubs that crash. If a feature is incomplete, hide its button from the UI.

9. AVL TREE VISIBILITY: Every search result must show a label like
   "✓ Ditemukan via AVL Tree | 0.12ms". The dosen must see ADT in action.

10. PRIORITY QUEUE VISIBILITY: Dashboard must show a table labeled
    "Min-Heap Priority Queue" and a note explaining it uses heapq, not SQL ORDER BY.
```

---

## ╔══════════════════════════════════════════╗
## ║   INSTALL — Jalankan sekali di terminal  ║
## ╚══════════════════════════════════════════╝

```bash
pip install PyQt5
```

Buat juga file `requirements.txt` dengan isi:
```
PyQt5
```

---

## ╔══════════════╗
## ║  TAHAP 1/8   ║
## ║  Skeleton    ║
## ╚══════════════╝

### Prompt 1.1 — Buat Struktur Folder & File Kosong

```
Create the complete folder and file structure for this PyQt5 desktop project.
Do NOT write any real code yet. Each file should contain only a single comment
describing its responsibility.

Create exactly these files:

Root level:
- main.py          → "Entry point: initialize all ADTs and launch QApplication"
- avl_tree.py      → "AVL Tree ADT: insert, search, delete, to_snapshot, rotations"
- priority_queue.py → "Min-Heap Priority Queue ADT using heapq for expiry alerts"
- stack.py         → "Stack ADT: LIFO action log and undo support"
- database.py      → "SQLite3 layer: schema setup, CRUD, seed data, queries"
- requirements.txt → "PyQt5"
- README.md        → "Project documentation, how to run, ADT explanations"

Inside ui/ folder:
- ui/__init__.py         → "UI package"
- ui/main_window.py      → "QMainWindow: sidebar navigation + QStackedWidget"
- ui/login_page.py       → "QWidget: login form with username/password"
- ui/kasir_page.py       → "QWidget: POS cashier with AVL search and cart"
- ui/gudang_page.py      → "QWidget: warehouse management, forms, undo"
- ui/dashboard_page.py   → "QWidget: expiry alerts, stock warnings, action log"
- ui/avl_visual_widget.py → "QWidget: live AVL Tree visualization using QPainter"

After creating all files, print the folder tree to verify structure is correct.
```

---

## ╔══════════════╗
## ║  TAHAP 2/8   ║
## ║  ADT Layer   ║
## ╚══════════════╝

### Prompt 2.1 — AVL Tree

```
Implement avl_tree.py with a complete, fully working AVL Tree.

Class AVLNode:
  Fields: key (int or str), data (dict), left, right, height

Class AVLTree:
  Implement ALL of these methods completely — no stubs, no TODOs:

  1. insert(self, key, data: dict) → None
     Insert node with given key and data dict. Auto-rebalance after insert.
     Handle all 4 rotation cases: LL, RR, LR, RL.

  2. search(self, key) → dict | None
     Exact key match. Return data dict if found, None if not found.

  3. search_prefix(self, prefix: str) → list[dict]
     In-order traversal collecting all nodes where str(node.key).startswith(prefix).
     Only meaningful for string-key trees.
     Return list of data dicts (empty list if none found).

  4. delete(self, key) → None
     Remove node by key. Auto-rebalance after delete.
     Handle case: node has 0, 1, or 2 children.

  5. to_snapshot(self) → dict | None
     Return recursive dict representing entire tree structure.
     Format per node: {"key": ..., "height": int, "balance_factor": int,
                       "left": dict|None, "right": dict|None}
     Return None if tree is empty.

  Private methods (all must be implemented):
  - _insert(node, key, data) → AVLNode
  - _delete(node, key) → AVLNode
  - _rotate_left(node) → AVLNode
  - _rotate_right(node) → AVLNode
  - _get_height(node) → int   (return 0 if node is None)
  - _get_balance(node) → int  (return 0 if node is None)
  - _update_height(node) → None
  - _min_node(node) → AVLNode (for delete: find inorder successor)
  - _snapshot(node) → dict | None (recursive helper for to_snapshot)

At the bottom of the file, add:
if __name__ == "__main__":
    import json
    t = AVLTree()
    # Insert in non-sequential order to trigger rotations
    for val in [105, 102, 110, 101, 103, 107, 115, 104, 108]:
        t.insert(val, {"id_barang": val, "nama_barang": f"Barang{val}", "harga_satuan": val * 100})
    print("=== Snapshot after 9 inserts ===")
    print(json.dumps(t.to_snapshot(), indent=2))
    print("\n=== Search 103 ===")
    print(t.search(103))
    print("\n=== Search 999 (not found) ===")
    print(t.search(999))
    t.delete(103)
    print("\n=== Snapshot after delete 103 ===")
    print(json.dumps(t.to_snapshot(), indent=2))
```

### Prompt 2.2 — Priority Queue (Min-Heap)

```
Implement priority_queue.py with a complete Min-Heap Priority Queue for expiry alerts.

Use Python's built-in heapq module — the entire point is to show heapq usage, NOT SQL ORDER BY.

Class ExpiredAlertQueue:

  Internal storage: self._heap = []
  Each heap item is a tuple: (tgl_expired: str, id_batch: int, nama_barang: str, jumlah_stok: int)
  Since format is 'YYYY-MM-DD', string comparison == date comparison. heapq will sort correctly.

  Methods (all fully implemented):

  1. push(self, tgl_expired: str, id_batch: int, nama_barang: str, jumlah_stok: int) → None
     heapq.heappush(self._heap, (tgl_expired, id_batch, nama_barang, jumlah_stok))

  2. pop(self) → dict | None
     heapq.heappop if not empty. Return as dict with keys:
     {tgl_expired, id_batch, nama_barang, jumlah_stok}

  3. peek(self) → dict | None
     Return top item as dict without removing. None if empty.

  4. get_top_n(self, n: int) → list[dict]
     Return top n items as list of dicts WITHOUT permanently removing them from heap.
     Use heapq.nsmallest(n, self._heap) then convert tuples to dicts.

  5. rebuild(self, items: list[dict]) → None
     Clear heap. For each item in items list (dicts with tgl_expired, id_batch,
     nama_barang, jumlah_stok keys), heappush it.

  6. size(self) → int
     Return len(self._heap)

At the bottom add:
if __name__ == "__main__":
    q = ExpiredAlertQueue()
    q.push("2025-06-01", 1, "Yogurt", 20)
    q.push("2025-05-28", 2, "Susu Kotak", 5)
    q.push("2025-07-15", 3, "Air Mineral", 100)
    q.push("2025-05-29", 4, "Teh Botol", 8)
    q.push("2025-08-01", 5, "Biskuit", 30)
    print("=== Top 3 (earliest expiry first) ===")
    for item in q.get_top_n(3):
        print(item)
    print(f"\nHeap size: {q.size()}")
```

### Prompt 2.3 — Stack ADT

```
Implement stack.py with a complete Stack ADT for action logging and undo.

Class ActionStack:

  Internal storage: self._stack = []   (Python list, append=push, pop=pop)

  Each item pushed is a dict:
  {"tipe": str, "payload": dict, "timestamp": str}
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  Valid tipe values: 'tambah_barang', 'edit_barang', 'hapus_barang',
                     'tambah_batch', 'checkout'

  Methods (all fully implemented):

  1. push(self, tipe: str, payload: dict) → None
     Build item dict with tipe, payload, and auto-generated timestamp.
     self._stack.append(item)

  2. pop(self) → dict | None
     Return self._stack.pop() if not empty, else None.

  3. peek(self) → dict | None
     Return self._stack[-1] if not empty, else None.

  4. is_empty(self) → bool

  5. size(self) → int

  6. to_list(self) → list[dict]
     Return reversed copy of stack as list (most recent first).
     Do NOT modify the original stack.

At the bottom add:
if __name__ == "__main__":
    s = ActionStack()
    s.push("tambah_barang", {"id_barang": 101, "nama_barang": "Susu"})
    s.push("tambah_batch",  {"id_batch": 1, "jumlah_stok": 50})
    s.push("checkout",      {"id_transaksi": 1, "total_harga": 25000})
    print("=== Stack size:", s.size())
    print("=== Peek (top):", s.peek())
    print("=== Pop (LIFO order):")
    while not s.is_empty():
        print(" ", s.pop())
```

---

## ╔══════════════╗
## ║  TAHAP 3/8   ║
## ║  Database    ║
## ╚══════════════╝

### Prompt 3.1 — database.py

```
Implement database.py as the complete SQLite3 data layer.

Module-level constant: DB_PATH = "app.db"

All functions use: with sqlite3.connect(DB_PATH) as conn:
Always set: conn.row_factory = sqlite3.Row
Convert rows to dicts with: dict(row) or [dict(r) for r in rows]

─── FUNCTION 1: setup_schema() ───────────────────────────────────────────────
Create all 6 tables with IF NOT EXISTS:

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

After creating tables, seed default users IF users table is empty:
  username="admin",  password="admin123", role="admin"
  username="kasir1", password="kasir123", role="kasir"
  Store passwords as: hashlib.sha256(pwd.encode()).hexdigest()

─── FUNCTION 2: seed_sample_data() ──────────────────────────────────────────
Only insert if barang table is empty (avoid duplicates on restart).

Insert barang (non-sequential IDs to show AVL rotations during demo):
  (101,'Susu Kotak',5000), (103,'Yogurt Stroberi',12000), (102,'Teh Botol',4000),
  (107,'Jus Jeruk',8000),  (105,'Air Mineral',3000),      (110,'Kopi Sachet',2500),
  (104,'Biskuit Coklat',7500), (108,'Mie Instan',3500),
  (106,'Sabun Mandi',6000), (109,'Shampo Sachet',4500)

Insert batch_stok for each barang. Use datetime.date.today() for date math.
  - 3 batches with tgl_expired = today + 3 days  (for expiry alert demo)
  - 3 batches with tgl_expired = today + 5 days
  - 4 batches with tgl_expired = today + 60 days
  - Vary jumlah_stok: some batches with stok = 3 or 5 (for stok tipis demo)
  - tgl_masuk = today - 30 days for all batches

─── FUNCTIONS 3-16: ─────────────────────────────────────────────────────────

def get_all_barang() → list[dict]:
  SELECT id_barang, nama_barang, harga_satuan FROM barang ORDER BY id_barang

def get_barang_by_id(id_barang: int) → dict | None:
  SELECT single row by id_barang

def insert_barang(id_barang: int, nama_barang: str, harga_satuan: int) → bool:
  INSERT OR IGNORE. Return True if inserted, False if id already exists.

def update_barang(id_barang: int, nama_barang: str, harga_satuan: int) → bool:
  UPDATE barang SET ... WHERE id_barang=?

def get_inventory() → list[dict]:
  SELECT br.id_barang, br.nama_barang, br.harga_satuan,
         COALESCE(SUM(bs.jumlah_stok),0) AS sisa_stok_total
  FROM barang br LEFT JOIN batch_stok bs ON br.id_barang=bs.id_barang
  GROUP BY br.id_barang ORDER BY br.id_barang

def get_batch_by_barang(id_barang: int) → list[dict]:
  SELECT id_batch, jumlah_stok, tgl_expired
  FROM batch_stok WHERE id_barang=? AND jumlah_stok > 0
  ORDER BY tgl_expired ASC

def insert_batch(id_barang: int, jumlah_stok: int, tgl_masuk: str, tgl_expired: str) → int:
  INSERT INTO batch_stok. Return lastrowid (new id_batch).

def update_stok_batch(id_batch: int, jumlah_baru: int) → bool:
  UPDATE batch_stok SET jumlah_stok=? WHERE id_batch=?

def verify_login(username: str, password: str) → dict | None:
  Hash the input password with SHA-256.
  SELECT user WHERE username=? AND password_hash=?
  Return dict WITHOUT password_hash field. Return None if not found.

def get_all_batch_aktif() → list[dict]:
  SELECT bs.id_batch, bs.id_barang, br.nama_barang, bs.jumlah_stok, bs.tgl_expired
  FROM batch_stok bs JOIN barang br ON bs.id_barang=br.id_barang
  WHERE bs.jumlah_stok > 0 ORDER BY bs.tgl_expired ASC

def insert_transaksi(tgl_waktu: str, total_harga: int, id_kasir: int,
                     detail_list: list[dict]) → int:
  detail_list items have keys: {id_barang, id_batch, qty, harga_satuan}
  In ONE transaction:
    1. INSERT INTO transaksi → get id_transaksi
    2. For each detail: INSERT INTO detail_transaksi
    3. For each detail: UPDATE batch_stok SET jumlah_stok = jumlah_stok - qty WHERE id_batch=?
  Return id_transaksi. Raise exception (rollback) on any error.

def get_alerts() → dict:
  Return {
    "expiry_soon": rows where tgl_expired within 7 days AND jumlah_stok > 0,
                   include sisa_hari calculated via julianday() in SQL,
    "stok_tipis":  barang where sisa_stok_total <= 10
  }

def get_action_log() → list[dict]:
  SELECT * FROM action_log WHERE sudah_undo=0 ORDER BY id_log DESC LIMIT 30

def insert_action_log(tipe_aksi: str, payload_dict: dict) → int:
  Convert payload_dict to JSON string using json.dumps().
  INSERT INTO action_log. Return id_log.

def mark_undo(id_log: int) → bool:
  UPDATE action_log SET sudah_undo=1 WHERE id_log=?

def delete_barang(id_barang: int) → bool:
  DELETE FROM barang WHERE id_barang=?
  Also DELETE FROM batch_stok WHERE id_barang=?

def delete_batch(id_batch: int) → bool:
  DELETE FROM batch_stok WHERE id_batch=?

─── __main__ TEST BLOCK: ──────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_schema()
    seed_sample_data()
    print("Schema and seed OK")
    items = get_inventory()
    print(f"Total barang: {len(items)}")
    for item in items[:3]:
        print(" ", item)
    alerts = get_alerts()
    print(f"Expiry alerts: {len(alerts['expiry_soon'])}")
    print(f"Stok tipis: {len(alerts['stok_tipis'])}")
```

---

## ╔══════════════╗
## ║  TAHAP 4/8   ║
## ║  main.py     ║
## ╚══════════════╝

### Prompt 4.1 — Entry Point

```
Implement main.py as the application entry point.

Imports needed:
  sys, database, avl_tree (AVLTree), priority_queue (ExpiredAlertQueue),
  stack (ActionStack), PyQt5.QtWidgets (QApplication),
  ui.main_window (MainWindow)

Steps in main():

1. Call database.setup_schema()
2. Call database.seed_sample_data()

3. Build avl_by_id = AVLTree()
   Build avl_by_name = AVLTree()
   rows = database.get_all_barang()
   For each row:
     avl_by_id.insert(row['id_barang'], dict(row))
     avl_by_name.insert(row['nama_barang'].strip().lower(), dict(row))
   Print: f"AVL Tree loaded: {len(rows)} barang"

4. Build alert_queue = ExpiredAlertQueue()
   batches = database.get_all_batch_aktif()
   alert_queue.rebuild(batches)
   Print: f"Priority Queue loaded: {alert_queue.size()} batch aktif"

5. action_stack = ActionStack()

6. app = QApplication(sys.argv)
   window = MainWindow(avl_by_id, avl_by_name, alert_queue, action_stack)
   window.show()
   sys.exit(app.exec_())

Wrap everything in:
if __name__ == "__main__":
    main()

After writing this file, run: python main.py
If a window appears (even blank), Tahap 4 is complete.
Fix any import errors before continuing.
```

---

## ╔══════════════╗
## ║  TAHAP 5/8   ║
## ║  MainWindow  ║
## ║  + Login     ║
## ╚══════════════╝

### Prompt 5.1 — main_window.py

```
Implement ui/main_window.py as the application shell.

Define COLOR dict at the top of this file:
COLOR = {
    "primary": "#6366f1", "primary_hover": "#4f46e5", "primary_light": "#e0e7ff",
    "bg_main": "#f8fafc", "bg_card": "#ffffff", "bg_sidebar": "#1e1b4b",
    "text_dark": "#1e293b", "text_muted": "#64748b", "text_sidebar": "#c7d2fe",
    "border": "#e2e8f0",
    "success_bg": "#dcfce7", "success_text": "#166534",
    "warning_bg": "#fef3c7", "warning_text": "#92400e",
    "danger_bg": "#fee2e2", "danger_text": "#991b1b",
    "node_default": "#6366f1", "node_new": "#f59e0b",
    "node_found": "#10b981", "node_line": "#94a3b8", "node_text": "#ffffff",
}

Define MAIN_STYLE QSS string (apply to QApplication):
  - QMainWindow background: COLOR["bg_main"]
  - QWidget#sidebar: background COLOR["bg_sidebar"], fixed width 220px
  - QPushButton#navBtn: text-align left, color COLOR["text_sidebar"],
    padding 10px 20px, no border, border-radius 6px, font-size 14px
  - QPushButton#navBtn:hover: background rgba(99,102,241,0.3), color white
  - QPushButton#navBtn[active="true"]: background COLOR["primary"], color white
  - QTableWidget: background white, border 1px solid COLOR["border"], border-radius 8px,
    gridline-color COLOR["border"], font-size 13px
  - QTableWidget::item:selected: background COLOR["primary_light"]
  - QHeaderView::section: background COLOR["bg_main"], color COLOR["text_muted"],
    font-weight bold, padding 8px, no border, border-bottom 1px solid COLOR["border"]
  - QLineEdit, QSpinBox, QDateEdit, QComboBox: border 1px solid COLOR["border"],
    border-radius 6px, padding 6px 10px, background white, font-size 13px
  - QLineEdit:focus: border-color COLOR["primary"]
  - QPushButton#primaryBtn: background COLOR["primary"], color white, no border,
    border-radius 6px, padding 8px 20px, font-size 13px, font-weight bold
  - QPushButton#primaryBtn:hover: background COLOR["primary_hover"]
  - QPushButton#dangerBtn: background COLOR["danger_bg"], color COLOR["danger_text"],
    border none, border-radius 6px, padding 8px 20px
  - QLabel#avlBadge: background COLOR["success_bg"], color COLOR["success_text"],
    border-radius 4px, padding 4px 10px, font-size 12px, font-weight bold
  - QFrame#card: background white, border 1px solid COLOR["border"], border-radius 10px

Class MainWindow(QMainWindow):
  Constructor: __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack)
  Store all 4 as self attributes.
  self.current_user = None

  Setup:
  - setWindowTitle("Sistem POS & Manajemen Gudang")
  - setMinimumSize(1200, 700)
  - Apply MAIN_STYLE via QApplication.instance().setStyleSheet(MAIN_STYLE)

  Central widget = QWidget with QHBoxLayout:
    Left: self.sidebar (QWidget, objectName="sidebar")
    Right: self.stack = QStackedWidget()

  self.sidebar layout = QVBoxLayout:
    - Logo label: "POS & Gudang" bold 16px, color white, padding 20px
    - Subtitle: "Struktur Data" 11px, muted, padding 0 20px 16px
    - Separator line (QFrame horizontal)
    - Nav buttons added dynamically by show_main_ui()
    - addStretch() at bottom
    - Logout button

  Methods:
  1. show_login(self)
     Import LoginPage, create instance, add to stack, setCurrentWidget.
     Hide sidebar.

  2. show_main_ui(self, user: dict)
     self.current_user = user
     Show sidebar.
     Import and create: KasirPage, GudangPage, DashboardPage, AVLVisualWidget
     Pass (avl_by_id, avl_by_name, alert_queue, action_stack, user) to each.
     Add all pages to self.stack.
     Build nav buttons based on role:
       - role "kasir":  [Kasir, Visualisasi AVL]
       - role "admin":  [Gudang, Dashboard, Visualisasi AVL]
     Each nav button calls self.navigate(page_widget)
     Navigate to first page automatically.

  3. navigate(self, page_widget)
     self.stack.setCurrentWidget(page_widget)
     Update nav button active state (set property "active" true/false, update style)

  4. logout(self)
     self.current_user = None
     Clear stack, rebuild login page.
     show_login()

  Call show_login() at end of __init__.
```

### Prompt 5.2 — login_page.py

```
Implement ui/login_page.py as the login screen.

Import: database from parent package (use: import database)
Import: QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QPushButton, QFrame from PyQt5.QtWidgets
Import: Qt, QFont from PyQt5.QtCore / PyQt5.QtGui

Class LoginPage(QWidget):
  Constructor: __init__(self, main_window)
    Store self.main_window = main_window

  UI Layout (centered card):
    Outer layout: QVBoxLayout with alignment AlignCenter
    Inner card: QFrame (objectName="card"), fixed width 380px
    Card layout: QVBoxLayout padding 40px, spacing 16px

    Contents of card:
    - Title label: "Selamat Datang" bold 22px, centered, color #1e293b
    - Subtitle: "Sistem POS & Manajemen Gudang" 13px muted, centered
    - Spacer 16px
    - Username section:
        QLabel "Username"
        QLineEdit self.input_username (placeholder: "Masukkan username")
    - Password section:
        QLabel "Password"
        QLineEdit self.input_password (placeholder: "Masukkan password")
        input_password.setEchoMode(QLineEdit.Password)
    - Spacer 8px
    - self.lbl_error: QLabel hidden, text red color, centered
    - self.btn_login: QPushButton "Masuk" (objectName="primaryBtn")
      full width, height 42px
    - Note label: "Demo: admin/admin123  atau  kasir1/kasir123"
      12px, muted, centered

    Connect: btn_login.clicked → self.do_login()
    Connect: input_username.returnPressed → self.do_login()
    Connect: input_password.returnPressed → self.do_login()

  Method do_login(self):
    username = self.input_username.text().strip()
    password = self.input_password.text()
    if not username or not password:
        show error "Username dan password tidak boleh kosong"
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
```

**Setelah Prompt 5 selesai — TEST:**
```
python main.py
```
Harus muncul jendela login dengan form username & password. Coba login dengan `admin` / `admin123`. Jika berhasil masuk ke halaman utama, lanjut ke Tahap 6.

---

## ╔══════════════╗
## ║  TAHAP 6/8   ║
## ║  Halaman UI  ║
## ╚══════════════╝

### Prompt 6.1 — avl_visual_widget.py

```
Implement ui/avl_visual_widget.py as the live AVL Tree visualization page.
This is the most important UI file — make it visually impressive.

Imports: QPainter, QColor, QFont, QPen, QTimer from PyQt5.QtGui / PyQt5.QtCore
         QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
         QRadioButton, QButtonGroup, QScrollArea from PyQt5.QtWidgets

Class AVLVisualWidget(QWidget):
  Constructor: __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user)
    Store avl references. self.current_tree = avl_by_id. self.highlight_key = None
    self.highlight_color = "#f59e0b"  ← yellow for new node
    self.found_key = None              ← green for search result

  Full page layout (QVBoxLayout):
    1. Header row (QHBoxLayout):
       - Title: "Visualisasi AVL Tree" bold 18px
       - Radio buttons: "🔢 by ID (Integer)" | "🔤 by Nama (String)"
         Toggle sets self.current_tree and calls self.canvas.update()
       - Refresh button (objectName="primaryBtn"): calls refresh()

    2. Info bar (QHBoxLayout with 3 QFrame cards):
       - "Total Node" card: self.lbl_total
       - "Height Pohon" card: self.lbl_height
       - "Last Updated" card: self.lbl_updated

    3. Canvas: self.canvas = AVLCanvas(self) — takes all remaining space
       Set minimum height 500px. Put inside QScrollArea for large trees.

    4. Legend row (QHBoxLayout):
       Three colored dots with labels:
       - ● #6366f1  "Node default"
       - ● #f59e0b  "Node baru diinsert"
       - ● #10b981  "Node ditemukan (search)"

    5. Info box (QLabel, italic, 12px, muted color):
       "Angka dalam node = key barang | bf = balance factor (-1/0/1 = seimbang)
        Node kuning = baru diinsert | Node hijau = hasil pencarian terakhir"

  Method refresh(self):
    snapshot = self.current_tree.to_snapshot()
    self.canvas.snapshot = snapshot
    self.canvas.highlight_key = self.highlight_key
    self.canvas.highlight_color = self.highlight_color
    self.canvas.found_key = self.found_key
    Update info bar: count nodes (recursive), get height from snapshot
    self.lbl_updated.setText(datetime.now().strftime("%H:%M:%S"))
    self.canvas.update()  ← triggers paintEvent

  Method highlight_new_node(self, key):
    self.highlight_key = key
    self.highlight_color = "#f59e0b"
    self.refresh()
    QTimer.singleShot(2000, self.clear_highlight)

  Method highlight_found_node(self, key):
    self.found_key = key
    self.refresh()
    QTimer.singleShot(2000, self.clear_found)

  Method clear_highlight(self): self.highlight_key = None; self.canvas.update()
  Method clear_found(self):     self.found_key = None;    self.canvas.update()


Class AVLCanvas(QWidget):
  Constructor: __init__(self, parent)
    self.snapshot = None
    self.highlight_key = None
    self.highlight_color = "#f59e0b"
    self.found_key = None
    self.node_radius = 28
    self.level_height = 90
    self._positions = {}  ← cache node positions for click detection
    setMouseTracking(True)

  Method paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    if self.snapshot is None:
        draw centered text "Pohon AVL kosong" in muted color
        return
    canvas_width = self.width()
    self._positions = {}
    self._calculate_positions(self.snapshot, 0, canvas_width, 50)
    self._draw_edges(painter, self.snapshot)
    self._draw_nodes(painter, self.snapshot)

  Method _calculate_positions(self, node, x_left, x_right, y):
    if node is None: return
    x_center = (x_left + x_right) // 2
    self._positions[node["key"]] = (x_center, y)
    mid = (x_left + x_right) // 2
    self._calculate_positions(node.get("left"),  x_left, mid,     y + self.level_height)
    self._calculate_positions(node.get("right"), mid,    x_right, y + self.level_height)

  Method _draw_edges(self, painter, node):
    if node is None: return
    px, py = self._positions[node["key"]]
    pen = QPen(QColor("#94a3b8")); pen.setWidth(2); painter.setPen(pen)
    for child_key in [node.get("left"), node.get("right")]:
        if child_key:
            cx, cy = self._positions[child_key["key"]]
            painter.drawLine(px, py, cx, cy)
            self._draw_edges(painter, child_key)

  Method _draw_nodes(self, painter, node):
    if node is None: return
    self._draw_nodes(painter, node.get("left"))
    self._draw_nodes(painter, node.get("right"))
    x, y = self._positions[node["key"]]
    r = self.node_radius
    # Determine color
    if node["key"] == self.highlight_key:
        color = QColor(self.highlight_color)
    elif node["key"] == self.found_key:
        color = QColor("#10b981")
    else:
        color = QColor("#6366f1")
    # Draw circle
    painter.setBrush(color)
    painter.setPen(QPen(color.darker(120), 2))
    painter.drawEllipse(x - r, y - r, r*2, r*2)
    # Draw key text (white, bold, 13px)
    painter.setPen(QColor("white"))
    font = QFont(); font.setBold(True); font.setPointSize(10); painter.setFont(font)
    painter.drawText(x - r, y - r, r*2, r*2, Qt.AlignCenter, str(node["key"]))
    # Draw balance factor below node (12px, muted)
    painter.setPen(QColor("#64748b"))
    font2 = QFont(); font2.setPointSize(8); painter.setFont(font2)
    bf_text = f"bf:{node['balance_factor']}"
    painter.drawText(x - 20, y + r + 2, 40, 16, Qt.AlignCenter, bf_text)

  Method mousePressEvent(self, event):
    click_x, click_y = event.x(), event.y()
    for key, (nx, ny) in self._positions.items():
        if ((click_x - nx)**2 + (click_y - ny)**2) ** 0.5 <= self.node_radius:
            self.parent().show_node_info(key)
            break

After implementing, also add method show_node_info(self, key) to AVLVisualWidget:
  Find the node data in current_tree.search(key) or current_tree.search(str(key))
  Show QMessageBox with: Key, Nama Barang, Harga Satuan, Balance Factor
```

### Prompt 6.2 — kasir_page.py

```
Implement ui/kasir_page.py as the POS cashier interface.

Imports: database, time
         All needed PyQt5 widgets and classes

Class KasirPage(QWidget):
  Constructor: __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user)

  self.keranjang = []  ← list of dicts: {id_barang, nama_barang, harga_satuan, qty, subtotal}
  self.current_user = user
  self.avl_by_id = avl_by_id
  self.avl_by_name = avl_by_name
  self.action_stack = action_stack

  Page layout (QVBoxLayout):

  ── Header ──────────────────────────────────────────────────
  QLabel "Kasir — Point of Sale" bold 18px
  QLabel f"Login sebagai: {user['username']}" muted 12px

  ── Search Card (QFrame#card) ────────────────────────────────
  Title: "🔍 Cari Barang (AVL Tree)" bold 14px
  Row: QLineEdit self.input_search (placeholder "ID barang atau nama...") +
       QPushButton "Cari" (objectName="primaryBtn") connected to do_search()
  Connect input_search.returnPressed → do_search()
  self.lbl_avl_badge: QLabel (objectName="avlBadge") hidden initially
  self.lbl_search_result: QLabel hidden initially (shows nama, harga, stok)
  self.btn_add_to_cart: QPushButton "➕ Tambah ke Keranjang" hidden initially
                        connected to add_to_cart()
  self.current_result = None  ← stores last search result dict

  ── Keranjang Card (QFrame#card) ─────────────────────────────
  Title: "🛒 Keranjang Belanja" bold 14px
  self.tbl_keranjang: QTableWidget
    Columns: No | Nama Barang | Harga Satuan | Qty | Subtotal | Hapus
    Column widths: 40, *, 120, 80, 120, 70
    setEditTriggers(NoEditTriggers) except Qty column uses QSpinBox delegate

  ── Total & Checkout Bar ─────────────────────────────────────
  QHBoxLayout:
    QLabel "Total Pembayaran:" bold 14px
    self.lbl_total: QLabel "Rp 0" bold 20px primary color
    addStretch()
    self.btn_checkout: QPushButton "💳 Proses Bayar" (objectName="primaryBtn")
                       height 44px, connected to do_checkout()

  Methods:

  do_search(self):
    q = self.input_search.text().strip()
    if not q: return
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

    Show badge: f"✓ Ditemukan via AVL Tree  |  {elapsed:.3f} ms"
    self.lbl_avl_badge.show()
    If single result: show nama, harga, sisa stok (query database)
    If multiple: show list of names, let user pick (show first one for simplicity)
    self.current_result = found_list[0]
    self.btn_add_to_cart.show()

  add_to_cart(self):
    if self.current_result is None: return
    barang = self.current_result
    existing = next((x for x in self.keranjang if x['id_barang'] == barang['id_barang']), None)
    if existing:
        existing['qty'] += 1
        existing['subtotal'] = existing['qty'] * existing['harga_satuan']
    else:
        self.keranjang.append({
            'id_barang': barang['id_barang'],
            'nama_barang': barang['nama_barang'],
            'harga_satuan': barang['harga_satuan'],
            'qty': 1,
            'subtotal': barang['harga_satuan']
        })
    self.render_keranjang()
    self.input_search.clear()
    self.lbl_avl_badge.hide()
    self.lbl_search_result.hide()
    self.btn_add_to_cart.hide()

  render_keranjang(self):
    Clear and rebuild tbl_keranjang from self.keranjang.
    For Qty column: place QSpinBox(min=1, max=999) with current qty.
      Connect spinbox valueChanged → lambda qty, item=item: update_qty(item['id_barang'], qty)
    For Hapus column: place QPushButton "✕" → remove_from_cart(id_barang)
    Update total.

  update_qty(self, id_barang, qty):
    Find item, update qty and subtotal. render_keranjang().

  remove_from_cart(self, id_barang):
    Remove item. render_keranjang().

  calculate_total(self) → int:
    Return sum(item['subtotal'] for item in self.keranjang)

  update_total_label(self):
    total = self.calculate_total()
    self.lbl_total.setText(f"Rp {total:,}".replace(",", "."))

  render_keranjang must call update_total_label at end.

  do_checkout(self):
    if not self.keranjang:
        show QMessageBox warning "Keranjang masih kosong"
        return

    Build detail_list for each keranjang item:
      Get batches FIFO: database.get_batch_by_barang(item['id_barang'])
      Distribute qty across batches (earliest expired first):
        remaining = item['qty']
        for batch in batches:
            if remaining <= 0: break
            take = min(remaining, batch['jumlah_stok'])
            detail_list.append({
                'id_barang': item['id_barang'],
                'id_batch': batch['id_batch'],
                'qty': take,
                'harga_satuan': item['harga_satuan']
            })
            remaining -= take
        if remaining > 0:
            show error "Stok tidak mencukupi untuk {nama_barang}"
            return

    tgl_waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = self.calculate_total()
    id_transaksi = database.insert_transaksi(tgl_waktu, total,
                                              self.current_user['id_user'],
                                              detail_list)
    self.action_stack.push('checkout', {'id_transaksi': id_transaksi, 'total': total})
    database.insert_action_log('checkout', {'id_transaksi': id_transaksi})

    Show QDialog "Transaksi Berhasil!":
      Content: id_transaksi, tgl_waktu, total formatted as Rp X.XXX
      List of items purchased
      OK button clears keranjang and render_keranjang()
```

### Prompt 6.3 — gudang_page.py

```
Implement ui/gudang_page.py as the warehouse admin page.

Class GudangPage(QWidget):
  Constructor: __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user)

  Page layout (QVBoxLayout):

  ── Header ──────────────────────────────────────────────────
  QLabel "Manajemen Gudang" bold 18px
  QLabel f"Admin: {user['username']}" muted 12px

  ── Inventory Table Card (QFrame#card) ───────────────────────
  Header row: Title "📦 Katalog & Stok Barang" + QPushButton "🔄 Refresh" → load_inventory()
  self.tbl_inventory: QTableWidget
    Columns: ID | Nama Barang | Harga Satuan | Stok Total | Status
    setEditTriggers(NoEditTriggers)
    Alternate row colors, highlight stok tipis row background COLOR["danger_bg"]
    Status column: show badge "⚠ Tipis" if stok <= 10, else "✓ Aman"

  ── Two-column form area (QHBoxLayout) ───────────────────────

  Left card "➕ Tambah Barang Baru" (QFrame#card):
    QFormLayout:
      "ID Barang:"    QSpinBox self.spin_id (min=1, max=99999)
      "Nama Barang:"  QLineEdit self.input_nama
      "Harga Satuan:" QSpinBox self.spin_harga (min=1, max=9999999, prefix="Rp ")
    QPushButton "Tambah Barang" (objectName="primaryBtn") → do_tambah_barang()
    self.lbl_barang_msg: QLabel hidden

  Right card "📥 Tambah Batch Stok" (QFrame#card):
    QFormLayout:
      "Barang:"       QComboBox self.combo_barang (populated from inventory)
      "Jumlah Stok:"  QSpinBox self.spin_stok (min=1, max=99999)
      "Tgl Masuk:"    QDateEdit self.date_masuk (default: today)
      "Tgl Expired:"  QDateEdit self.date_expired (default: today + 30 days)
    QPushButton "Tambah Batch" (objectName="primaryBtn") → do_tambah_batch()
    self.lbl_batch_msg: QLabel hidden

  ── Undo & Log Card (QFrame#card) ────────────────────────────
  Header row:
    QLabel "📋 Riwayat Aksi (Stack ADT)" bold 14px
    QPushButton "↩ Undo Aksi Terakhir" (objectName="dangerBtn") → do_undo()
  self.tbl_log: QTableWidget
    Columns: Waktu | Tipe Aksi | Status
    Load from database.get_action_log()

  Methods:

  load_inventory(self):
    rows = database.get_inventory()
    Rebuild tbl_inventory. Populate combo_barang.
    For each row, highlight if sisa_stok_total <= 10.

  do_tambah_barang(self):
    id_b = self.spin_id.value()
    nama = self.input_nama.text().strip()
    harga = self.spin_harga.value()
    if not nama: show error; return
    success = database.insert_barang(id_b, nama, harga)
    if not success: show error "ID sudah ada"; return
    row_data = database.get_barang_by_id(id_b)
    self.avl_by_id.insert(id_b, row_data)
    self.avl_by_name.insert(nama.strip().lower(), row_data)
    self.action_stack.push('tambah_barang', row_data)
    database.insert_action_log('tambah_barang', row_data)
    load_inventory()
    load_log()
    Show success message. Clear form.

  do_tambah_batch(self):
    Get selected barang from combo (store id_barang as combo item data)
    jumlah = self.spin_stok.value()
    tgl_masuk = self.date_masuk.date().toString("yyyy-MM-dd")
    tgl_expired = self.date_expired.date().toString("yyyy-MM-dd")
    if tgl_expired <= tgl_masuk: show error; return
    id_batch = database.insert_batch(id_barang, jumlah, tgl_masuk, tgl_expired)
    self.alert_queue.push(tgl_expired, id_batch, nama_barang, jumlah)
    self.action_stack.push('tambah_batch', {'id_batch': id_batch})
    database.insert_action_log('tambah_batch', {'id_batch': id_batch})
    load_inventory()
    load_log()

  do_undo(self):
    action = self.action_stack.pop()
    if action is None:
        show QMessageBox "Tidak ada aksi yang bisa di-undo"; return
    tipe = action['tipe']
    payload = action['payload']
    if tipe == 'tambah_barang':
        database.delete_barang(payload['id_barang'])
        self.avl_by_id.delete(payload['id_barang'])
        self.avl_by_name.delete(payload['nama_barang'].strip().lower())
    elif tipe == 'tambah_batch':
        database.delete_batch(payload['id_batch'])
        Rebuild alert_queue from database
    Mark action log: find most recent unundo'd log matching tipe, mark as done.
    load_inventory()
    load_log()
    show QMessageBox f"Aksi '{tipe}' berhasil di-undo"

  load_log(self):
    rows = database.get_action_log()
    Rebuild tbl_log. Show status "Aktif" in green, "Di-undo" in red.

  Call load_inventory() and load_log() at end of __init__.
```

### Prompt 6.4 — dashboard_page.py

```
Implement ui/dashboard_page.py as the analytics dashboard.

Class DashboardPage(QWidget):
  Constructor: __init__(self, avl_by_id, avl_by_name, alert_queue, action_stack, user)

  Page layout (QVBoxLayout):

  ── Header ──────────────────────────────────────────────────
  QLabel "Dashboard" bold 18px

  ── Summary Cards Row (QHBoxLayout, 3 cards) ─────────────────
  Card 1 "⚠ Expiry Alert": self.lbl_expiry_count (large number, danger color)
  Card 2 "📉 Stok Tipis": self.lbl_stok_count (large number, warning color)
  Card 3 "📋 Total Aksi": self.lbl_log_count (large number, primary color)
  Each card: QFrame#card, QVBoxLayout, title label 12px muted + count label 28px bold

  ── Min-Heap Priority Queue Card (QFrame#card) ───────────────
  Header: "🔺 Min-Heap Priority Queue — Expiry Terdekat"
  Explanation label (italic, 12px, muted):
    "Data diurutkan menggunakan Min-Heap (Python heapq), bukan SQL ORDER BY.
     Insert O(log n) | Peek O(1) | Kompleksitas ruang O(n)"
  self.tbl_heap: QTableWidget
    Columns: Rank | Nama Barang | Tgl Expired | Sisa Hari | Stok
    Show top 10 from alert_queue.get_top_n(10)
    Color rows: red bg if sisa_hari <= 3, orange bg if sisa_hari <= 7

  ── Stok Tipis Card (QFrame#card) ────────────────────────────
  Title: "📉 Barang Stok Tipis (≤ 10 unit)"
  self.tbl_stok: QTableWidget
    Columns: ID | Nama Barang | Sisa Stok Total
    From database.get_alerts()["stok_tipis"]
    Highlight all rows background COLOR["warning_bg"]

  ── Stack ADT Log Card (QFrame#card) ─────────────────────────
  Title: "📋 Log Aksi — Stack ADT"
  Explanation label (italic, 12px, muted):
    "Setiap aksi dicatat ke Stack (LIFO). Undo tersedia di halaman Gudang."
  self.tbl_log: QTableWidget
    Columns: Waktu | Tipe Aksi | Status
    From database.get_action_log()
    Status "Aktif" = green badge, "Di-undo" = red badge

  Refresh button top-right of page: calls load_all()

  Method load_all(self):
    Load heap table, stok tipis, action log.
    Update summary card numbers.
    Calculate sisa_hari in Python: (datetime.strptime(tgl_expired,'%Y-%m-%d').date() - date.today()).days

  Call load_all() at end of __init__.
```

---

## ╔══════════════╗
## ║  TAHAP 7/8   ║
## ║  Integrasi   ║
## ╚══════════════╝

### Prompt 7.1 — Hubungkan Visualisasi ke Gudang

```
Update gudang_page.py and avl_visual_widget.py so they communicate when
a new barang is added.

The goal: when admin adds a new barang in GudangPage, the AVLVisualWidget
automatically highlights the new node in yellow for 2 seconds.

Implementation approach:
- In MainWindow.show_main_ui(), store references to both pages:
  self.gudang_page and self.avl_visual_page
- After GudangPage.do_tambah_barang() succeeds, call:
  self.main_window.avl_visual_page.highlight_new_node(id_barang)
- Pass main_window reference to GudangPage so it can call this.

Also update KasirPage.do_search():
- After a successful search, call:
  self.main_window.avl_visual_page.highlight_found_node(found_key)
- This shows the found node in green in the visualization.

Make sure no circular import occurs. Use late imports or pass references
through constructor arguments.
```

### Prompt 7.2 — Seed Data & Demo Verification

```
Add function seed_sample_data() to database.py if not already complete.

Verify these specific demo scenarios work end-to-end:

Scenario 1 — AVL Rotation Demo:
  The 10 sample barang IDs (101,103,102,107,105,110,104,108,106,109) are inserted
  in this non-sequential order so AVL rotations occur during tree building.
  Run python avl_tree.py and confirm the snapshot shows a balanced tree
  (no node has balance_factor outside -1,0,1).

Scenario 2 — Expiry Alert Demo:
  At least 3 batches must have tgl_expired within 5 days of today.
  Run python database.py and confirm get_alerts()["expiry_soon"] returns >= 3 items.

Scenario 3 — Stok Tipis Demo:
  At least 2 barang must have sisa_stok_total <= 10.
  Confirm get_alerts()["stok_tipis"] returns >= 2 items.

Fix seed_sample_data() if any scenario fails.
After fixing, delete app.db and run python main.py to regenerate with fresh data.
```

---

## ╔══════════════╗
## ║  TAHAP 8/8   ║
## ║  Polish &    ║
## ║  Bug Fix     ║
## ╚══════════════╝

### Prompt 8.1 — Bug Sweep & Polish

```
Perform a complete final sweep. Find and fix ALL of these issues:

UI Polish:
1. avl_visual_widget.py: if canvas is too small for the tree, add QScrollArea so
   user can scroll to see all nodes. Set canvas minimum size based on tree width.
2. kasir_page.py: format ALL currency as "Rp X.XXX" with dots as thousand separator.
   Use f"Rp {value:,}".replace(",", ".") consistently.
3. gudang_page.py: after tambah_barang succeeds, clear all form fields and reset
   spin_id, input_nama, spin_harga to defaults.
4. All QTableWidget: call setAlternatingRowColors(True) and
   setSelectionBehavior(QAbstractItemView.SelectRows).
5. All QTableWidget: call horizontalHeader().setStretchLastSection(True) so
   the last column fills remaining width.
6. Sidebar nav buttons: ensure active page button is visually distinct
   (background primary color) when navigating between pages.
7. Add setWindowIcon if you have an icon, otherwise skip.

Robustness:
8. kasir_page.py do_checkout: if database.insert_transaksi raises an exception,
   catch it, show QMessageBox critical error, do NOT clear keranjang.
9. gudang_page.py do_undo: handle case where avl_tree.delete() raises KeyError
   (key not found). Catch and show user-friendly error.
10. database.py insert_transaksi: wrap in try/except, on exception call conn.rollback()
    explicitly before re-raising.
11. main.py: wrap QApplication and window creation in try/except. On exception,
    print clear error message and sys.exit(1).

Final verification:
12. Run python main.py — window opens, no console errors.
13. Login as kasir1, search "susu", confirm AVL badge shows with timing.
14. Add to cart, checkout, confirm struk dialog appears.
15. Login as admin, go to Gudang, add barang ID=120 nama="Coklat Susu" harga=8000.
16. Go to Visualisasi, confirm node 120 is visible in the tree.
17. Back to Gudang, click Undo — node 120 disappears from tree.
18. Open Dashboard — confirm Min-Heap table shows data with sisa_hari column.
```

### Prompt 8.2 — README.md

```
Write README.md with the following sections:

# Sistem POS & Manajemen Gudang
## Tugas Matakuliah Struktur Data

### Tim (4 orang)
[list team members]

### Cara Menjalankan
1. pip install PyQt5
2. python main.py

### Akun Demo
| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | Admin |
| kasir1   | kasir123  | Kasir |

### Struktur Data yang Diimplementasi

#### 1. AVL Tree (avl_tree.py)
Digunakan untuk indexing katalog barang di in-memory.
- avl_by_id: key = INTEGER id_barang
- avl_by_name: key = STRING nama_barang (lowercase)
- Operasi: insert O(log n), search O(log n), delete O(log n)
- Mengapa AVL bukan B-Tree: [tulis argumen dari SKILL.md section 12]
- Visualisasi: halaman khusus dengan QPainter

#### 2. Min-Heap Priority Queue (priority_queue.py)
Digunakan untuk mengurutkan expiry alert tanpa SQL ORDER BY.
- Implementasi: Python heapq
- Insert O(log n), Peek O(1)
- Key: tgl_expired (YYYY-MM-DD format)

#### 3. Stack ADT (stack.py)
Digunakan untuk log aksi dan operasi Undo (LIFO).
- Push setiap aksi tambah barang, tambah batch, checkout
- Pop untuk membatalkan aksi terakhir
- Sync dengan tabel action_log di SQLite

### Database Schema
[Paste the 6 CREATE TABLE statements from database.py]

### Struktur Folder
[Paste the folder tree]
```

---

## 📌 CATATAN PENTING UNTUK CURSOR

### Urutan yang WAJIB diikuti:
```
Tahap 1 → 2 → 3 → TEST (python avl_tree.py, python database.py) →
4 → TEST (python main.py) → 5 → TEST (login berhasil) →
6 → 7 → 8 → DEMO FINAL
```

### Jika ada error import:
- Cek `ui/__init__.py` ada dan tidak kosong (isi minimal: `# UI Package`)
- Dari `ui/kasir_page.py`, import database dengan: `import sys; sys.path.insert(0, '..')`
  atau gunakan relative import dengan benar
- Semua `ui/*.py` mengimport `database` dan ADT dari root level

### Jika visualisasi pohon tidak muncul:
- Pastikan `avl_tree.to_snapshot()` mengembalikan dict yang benar (test di `python avl_tree.py`)
- Cek `AVLCanvas.paintEvent` dipanggil: tambahkan `print("paintEvent called")` sementara
- Pastikan `self.canvas.update()` dipanggil setelah set snapshot

### Jika UI freeze saat query:
- Pindahkan operasi database ke QThread
- Emit signal setelah selesai untuk update UI di main thread

### Untuk demo yang mulus:
- Jangan hapus `app.db` setelah seed data selesai
- Insert barang baru saat demo dengan ID yang belum ada (misal: 120, 125)
- Tunjukkan visualisasi AVL sebelum dan sesudah insert untuk efek wow
- Tunjukkan label "✓ Via AVL Tree | X ms" kepada dosen saat search

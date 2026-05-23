"""SQLite3 layer: schema setup, CRUD, seed data, queries."""

import hashlib
import json
import sqlite3
from datetime import date, datetime, timedelta

DB_PATH = "app.db"

SAMPLE_BARANG = [
    (101, "Susu Kotak", 5000),
    (103, "Yogurt Stroberi", 12000),
    (102, "Teh Botol", 4000),
    (107, "Jus Jeruk", 8000),
    (105, "Air Mineral", 3000),
    (110, "Kopi Sachet", 2500),
    (104, "Biskuit Coklat", 7500),
    (108, "Mie Instan", 3500),
    (106, "Sabun Mandi", 6000),
    (109, "Shampo Sachet", 4500),
]


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def setup_schema() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.executescript(
            """
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
            """
        )
        count = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        if count == 0:
            defaults = [
                ("admin", "admin123", "admin"),
                ("kasir1", "kasir123", "kasir"),
            ]
            for username, password, role in defaults:
                conn.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                    """,
                    (username, _hash_password(password), role),
                )
        conn.commit()


def seed_sample_data() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        count = conn.execute("SELECT COUNT(*) AS n FROM barang").fetchone()["n"]
        if count > 0:
            return

        today = date.today()
        tgl_masuk = (today - timedelta(days=30)).isoformat()
        exp_3 = (today + timedelta(days=3)).isoformat()
        exp_5 = (today + timedelta(days=5)).isoformat()
        exp_60 = (today + timedelta(days=60)).isoformat()

        for row in SAMPLE_BARANG:
            conn.execute(
                "INSERT INTO barang (id_barang, nama_barang, harga_satuan) VALUES (?, ?, ?)",
                row,
            )

        # One batch per barang: 3× +3d, 3× +5d, 4× +60d; low stock on first two for stok tipis demo
        batch_plan = [
            (101, 3, exp_3),
            (103, 5, exp_3),
            (102, 25, exp_3),
            (107, 30, exp_5),
            (105, 5, exp_5),
            (110, 40, exp_5),
            (104, 50, exp_60),
            (108, 45, exp_60),
            (106, 35, exp_60),
            (109, 60, exp_60),
        ]
        for id_barang, jumlah_stok, tgl_expired in batch_plan:
            conn.execute(
                """
                INSERT INTO batch_stok (id_barang, jumlah_stok, tgl_masuk, tgl_expired)
                VALUES (?, ?, ?, ?)
                """,
                (id_barang, jumlah_stok, tgl_masuk, tgl_expired),
            )
        conn.commit()


def get_all_barang() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id_barang, nama_barang, harga_satuan
            FROM barang ORDER BY id_barang
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_barang_by_id(id_barang: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT id_barang, nama_barang, harga_satuan
            FROM barang WHERE id_barang = ?
            """,
            (id_barang,),
        ).fetchone()
        return dict(row) if row else None


def insert_barang(id_barang: int, nama_barang: str, harga_satuan: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO barang (id_barang, nama_barang, harga_satuan)
            VALUES (?, ?, ?)
            """,
            (id_barang, nama_barang, harga_satuan),
        )
        conn.commit()
        return cur.rowcount > 0


def update_barang(id_barang: int, nama_barang: str, harga_satuan: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            UPDATE barang SET nama_barang = ?, harga_satuan = ?
            WHERE id_barang = ?
            """,
            (nama_barang, harga_satuan, id_barang),
        )
        conn.commit()
        return cur.rowcount > 0


def get_inventory() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT br.id_barang, br.nama_barang, br.harga_satuan,
                   COALESCE(SUM(bs.jumlah_stok), 0) AS sisa_stok_total
            FROM barang br
            LEFT JOIN batch_stok bs ON br.id_barang = bs.id_barang
            GROUP BY br.id_barang
            ORDER BY br.id_barang
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_batch_by_barang(id_barang: int) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id_batch, jumlah_stok, tgl_expired
            FROM batch_stok
            WHERE id_barang = ? AND jumlah_stok > 0
            ORDER BY tgl_expired ASC
            """,
            (id_barang,),
        ).fetchall()
        return [dict(r) for r in rows]


def insert_batch(
    id_barang: int, jumlah_stok: int, tgl_masuk: str, tgl_expired: str
) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT INTO batch_stok (id_barang, jumlah_stok, tgl_masuk, tgl_expired)
            VALUES (?, ?, ?, ?)
            """,
            (id_barang, jumlah_stok, tgl_masuk, tgl_expired),
        )
        conn.commit()
        return cur.lastrowid


def update_stok_batch(id_batch: int, jumlah_baru: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "UPDATE batch_stok SET jumlah_stok = ? WHERE id_batch = ?",
            (jumlah_baru, id_batch),
        )
        conn.commit()
        return cur.rowcount > 0


def verify_login(username: str, password: str) -> dict | None:
    pwd_hash = _hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT id_user, username, role
            FROM users
            WHERE username = ? AND password_hash = ?
            """,
            (username, pwd_hash),
        ).fetchone()
        return dict(row) if row else None


def get_all_batch_aktif() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT bs.id_batch, bs.id_barang, br.nama_barang,
                   bs.jumlah_stok, bs.tgl_expired
            FROM batch_stok bs
            JOIN barang br ON bs.id_barang = br.id_barang
            WHERE bs.jumlah_stok > 0
            ORDER BY bs.tgl_expired ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def insert_transaksi(
    tgl_waktu: str,
    total_harga: int,
    id_kasir: int,
    detail_list: list[dict],
) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO transaksi (tgl_waktu, total_harga, id_kasir)
                VALUES (?, ?, ?)
                """,
                (tgl_waktu, total_harga, id_kasir),
            )
            id_transaksi = cur.lastrowid
            for d in detail_list:
                conn.execute(
                    """
                    INSERT INTO detail_transaksi
                        (id_transaksi, id_barang, id_batch, qty, harga_satuan)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        id_transaksi,
                        d["id_barang"],
                        d["id_batch"],
                        d["qty"],
                        d["harga_satuan"],
                    ),
                )
                conn.execute(
                    """
                    UPDATE batch_stok
                    SET jumlah_stok = jumlah_stok - ?
                    WHERE id_batch = ?
                    """,
                    (d["qty"], d["id_batch"]),
                )
            conn.commit()
            return id_transaksi
        except Exception:
            conn.rollback()
            raise


def get_alerts() -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        expiry_rows = conn.execute(
            """
            SELECT bs.id_batch, bs.id_barang, br.nama_barang,
                   bs.tgl_expired, bs.jumlah_stok,
                   CAST(julianday(bs.tgl_expired) - julianday('now') AS INTEGER) AS sisa_hari
            FROM batch_stok bs
            JOIN barang br ON bs.id_barang = br.id_barang
            WHERE bs.jumlah_stok > 0
              AND julianday(bs.tgl_expired) - julianday('now') <= 7
            ORDER BY sisa_hari ASC
            """
        ).fetchall()
        stok_rows = conn.execute(
            """
            SELECT br.id_barang, br.nama_barang,
                   COALESCE(SUM(bs.jumlah_stok), 0) AS sisa_stok_total
            FROM barang br
            LEFT JOIN batch_stok bs ON br.id_barang = bs.id_barang
            GROUP BY br.id_barang
            HAVING sisa_stok_total <= 10
            ORDER BY sisa_stok_total ASC
            """
        ).fetchall()
        return {
            "expiry_soon": [dict(r) for r in expiry_rows],
            "stok_tipis": [dict(r) for r in stok_rows],
        }


def get_action_log() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT * FROM action_log
            WHERE sudah_undo = 0
            ORDER BY id_log DESC
            LIMIT 30
            """
        ).fetchall()
        return [dict(r) for r in rows]


def insert_action_log(tipe_aksi: str, payload_dict: dict) -> int:
    tgl_waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = json.dumps(payload_dict)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT INTO action_log (tgl_waktu, tipe_aksi, payload)
            VALUES (?, ?, ?)
            """,
            (tgl_waktu, tipe_aksi, payload),
        )
        conn.commit()
        return cur.lastrowid


def mark_undo(id_log: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "UPDATE action_log SET sudah_undo = 1 WHERE id_log = ?",
            (id_log,),
        )
        conn.commit()
        return cur.rowcount > 0


def delete_barang(id_barang: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM batch_stok WHERE id_barang = ?", (id_barang,))
        cur = conn.execute("DELETE FROM barang WHERE id_barang = ?", (id_barang,))
        conn.commit()
        return cur.rowcount > 0


def delete_batch(id_batch: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM batch_stok WHERE id_batch = ?", (id_batch,))
        conn.commit()
        return cur.rowcount > 0


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

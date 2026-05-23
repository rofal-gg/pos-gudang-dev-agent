import sys

from PyQt5.QtWidgets import QApplication

import database
from avl_tree import AVLTree
from priority_queue import ExpiredAlertQueue
from stack import ActionStack
from ui.main_window import MainWindow


def main() -> None:
    try:
        database.setup_schema()
        database.seed_sample_data()

        avl_by_id = AVLTree()
        avl_by_name = AVLTree()
        rows = database.get_all_barang()
        for row in rows:
            avl_by_id.insert(row["id_barang"], dict(row))
            avl_by_name.insert(row["nama_barang"].strip().lower(), dict(row))
        print(f"AVL Tree loaded: {len(rows)} barang")

        alert_queue = ExpiredAlertQueue()
        batches = database.get_all_batch_aktif()
        alert_queue.rebuild(batches)
        print(f"Priority Queue loaded: {alert_queue.size()} batch aktif")

        action_stack = ActionStack()

        app = QApplication(sys.argv)
        window = MainWindow(avl_by_id, avl_by_name, alert_queue, action_stack)
        window.show()
        sys.exit(app.exec_())
    except Exception as exc:
        print(f"ERROR: Gagal menjalankan aplikasi — {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

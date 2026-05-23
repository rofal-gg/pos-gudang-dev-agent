import datetime


class ActionStack:
    """LIFO stack for action logging and undo."""

    def __init__(self):
        self._stack = []

    def push(self, tipe: str, payload: dict) -> None:
        item = {
            "tipe": tipe,
            "payload": payload,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._stack.append(item)

    def pop(self) -> dict | None:
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self) -> dict | None:
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)

    def to_list(self) -> list[dict]:
        return list(reversed(self._stack))


if __name__ == "__main__":
    s = ActionStack()
    s.push("tambah_barang", {"id_barang": 101, "nama_barang": "Susu"})
    s.push("tambah_batch", {"id_batch": 1, "jumlah_stok": 50})
    s.push("checkout", {"id_transaksi": 1, "total_harga": 25000})
    print("=== Stack size:", s.size())
    print("=== Peek (top):", s.peek())
    print("=== Pop (LIFO order):")
    while not s.is_empty():
        print(" ", s.pop())

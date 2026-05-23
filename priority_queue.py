# Min-Heap Priority Queue ADT using heapq for expiry alerts

import heapq


class ExpiredAlertQueue:
    """Min-heap priority queue for batch expiry alerts (earliest date first)."""

    def __init__(self) -> None:
        self._heap: list[tuple[str, int, str, int]] = []

    def push(
        self,
        tgl_expired: str,
        id_batch: int,
        nama_barang: str,
        jumlah_stok: int,
    ) -> None:
        heapq.heappush(self._heap, (tgl_expired, id_batch, nama_barang, jumlah_stok))

    def pop(self) -> dict | None:
        if not self._heap:
            return None
        tgl_expired, id_batch, nama_barang, jumlah_stok = heapq.heappop(self._heap)
        return {
            "tgl_expired": tgl_expired,
            "id_batch": id_batch,
            "nama_barang": nama_barang,
            "jumlah_stok": jumlah_stok,
        }

    def peek(self) -> dict | None:
        if not self._heap:
            return None
        tgl_expired, id_batch, nama_barang, jumlah_stok = self._heap[0]
        return {
            "tgl_expired": tgl_expired,
            "id_batch": id_batch,
            "nama_barang": nama_barang,
            "jumlah_stok": jumlah_stok,
        }

    def get_top_n(self, n: int) -> list[dict]:
        top = heapq.nsmallest(n, self._heap)
        return [
            {
                "tgl_expired": tgl_expired,
                "id_batch": id_batch,
                "nama_barang": nama_barang,
                "jumlah_stok": jumlah_stok,
            }
            for tgl_expired, id_batch, nama_barang, jumlah_stok in top
        ]

    def rebuild(self, items: list[dict]) -> None:
        self._heap.clear()
        for item in items:
            heapq.heappush(
                self._heap,
                (
                    item["tgl_expired"],
                    item["id_batch"],
                    item["nama_barang"],
                    item["jumlah_stok"],
                ),
            )

    def size(self) -> int:
        return len(self._heap)


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

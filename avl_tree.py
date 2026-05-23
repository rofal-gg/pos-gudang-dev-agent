# AVL Tree ADT: insert, search, delete, to_snapshot, rotations


class AVLNode:
    def __init__(self, key, data: dict):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data: dict) -> None:
        self.root = self._insert(self.root, key, data)

    def search(self, key) -> dict | None:
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.data
        return None

    def search_prefix(self, prefix: str) -> list[dict]:
        results: list[dict] = []
        self._search_prefix(self.root, prefix, results)
        return results

    def _search_prefix(self, node, prefix: str, results: list[dict]) -> None:
        if node is None:
            return
        key_str = str(node.key)
        if key_str < prefix:
            self._search_prefix(node.right, prefix, results)
        elif not key_str.startswith(prefix):
            self._search_prefix(node.left, prefix, results)
        else:
            self._search_prefix(node.left, prefix, results)
            results.append(node.data)
            self._search_prefix(node.right, prefix, results)

    def delete(self, key) -> None:
        new_root, deleted = self._delete(self.root, key)
        if not deleted:
            raise KeyError(key)
        self.root = new_root

    def to_snapshot(self) -> dict | None:
        return self._snapshot(self.root)

    def _insert(self, node, key, data: dict):
        if node is None:
            return AVLNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data
            return node

        self._update_height(node)
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _delete(self, node, key):
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            successor = self._min_node(node.right)
            node.key = successor.key
            node.data = successor.data
            node.right, _ = self._delete(node.right, successor.key)

        if node is None:
            return None, deleted

        self._update_height(node)
        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node), deleted
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node), deleted
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node), deleted
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node), deleted

        return node, deleted

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _get_height(self, node) -> int:
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node) -> int:
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node) -> None:
        node.height = 1 + max(
            self._get_height(node.left),
            self._get_height(node.right),
        )

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _snapshot(self, node) -> dict | None:
        if node is None:
            return None
        return {
            "key": node.key,
            "height": node.height,
            "balance_factor": self._get_balance(node),
            "left": self._snapshot(node.left),
            "right": self._snapshot(node.right),
        }


if __name__ == "__main__":
    import json

    t = AVLTree()
    # Same order as database.seed_sample_data() — triggers AVL rotations
    for val in [101, 103, 102, 107, 105, 110, 104, 108, 106, 109]:
        t.insert(val, {"id_barang": val, "nama_barang": f"Barang{val}", "harga_satuan": val * 100})
    print("=== Snapshot after 10 inserts (seed order) ===")
    print(json.dumps(t.to_snapshot(), indent=2))
    print("\n=== Search 103 ===")
    print(t.search(103))
    print("\n=== Search 999 (not found) ===")
    print(t.search(999))
    t.delete(103)
    print("\n=== Snapshot after delete 103 ===")
    print(json.dumps(t.to_snapshot(), indent=2))

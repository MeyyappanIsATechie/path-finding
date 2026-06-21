class Node:
    def __init__(self, node_id: str, x: float, y: float):
        self.id = node_id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.id})"
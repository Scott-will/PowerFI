from server.db.models.transactions.transaction import Transaction


class TransactionTreeNode:

    def __init__(self, transaction : Transaction):
        self.transaction = transaction  # This can be any object, like a dict or a custom Transaction class
        self.children : [TransactionTreeNode] = []

    def add_child(self, child_node):
        if isinstance(child_node, TransactionTreeNode):
            self.children.append(child_node)
        else:
            raise TypeError("Child node must be an instance of TreeNode")

import hashlib

class Node:
    def __init__(self, left, right, value, content):
        self.left = left
        self.right = right
        self.value = value
        self.content = content

    @staticmethod
    def hash(data):
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

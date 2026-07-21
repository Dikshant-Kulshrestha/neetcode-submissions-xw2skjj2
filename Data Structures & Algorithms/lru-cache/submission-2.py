class Node:
    def __init__(self, key, value):
        self.val, self.key = value, key
        self.prev = self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}

        self.right, self.left = Node(0,0), Node(0,0)
        self.left.next, self.right.prev = self.right, self.left

    #insert node at right
    def insert(self, node):
        nxt, prev = self.right, self.right.prev
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    #remove node from list
    def remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev
        
    def get(self, key: int) -> int:
        #update use freq
        if key in self.cache:
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        else:
            return -1
        

    def put(self, key: int, value: int) -> None:
        
        if key in self.cache:
            self.remove(self.cache[key])
        
        self.cache[key] = Node(key,value)
        #update use freq
        self.insert(self.cache[key])

        #check cap
        if len(self.cache)>self.cap:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

        

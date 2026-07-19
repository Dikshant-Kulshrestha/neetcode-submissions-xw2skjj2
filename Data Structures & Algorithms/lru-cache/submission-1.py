class Node:
    def __init__(self, key, value):
        self.key, self.val = key, value
        self.prev = self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        
        self.left, self.right = Node(0,0), Node(0,0)
        self.left.next, self.right.prev = self.right, self.left
    
    #remove from linked list
    def remove(self,node):
        prev,nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev
        
    #insert at the right 
    def insert(self, node):
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt        


    def get(self, key: int) -> int:
        
        if key in self.cache:
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        else:
            return -1
        
        #update use freq
     

    def put(self, key: int, value: int) -> None:

        if key in self.cache:
            self.remove(self.cache[key])
         
        self.cache[key] = Node(key,value)
        #update use freq
        self.insert(self.cache[key])

        #check capacity, if exceeded, remove LRU
        if len(self.cache) > self.cap:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]
        

        

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        currentnode = head
        prev = None

        while currentnode:
            # print(currentnode.val)
            # currentnode = currentnode.next
            nxt = currentnode.next
            currentnode.next = prev
            prev = currentnode
            currentnode = nxt
        return prev
            
        

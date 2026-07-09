# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        
       
        l =0
        curr = head
        while curr:
            l+=1 
            curr = curr.next

        

        ele = l-n
        if ele ==0:
            return head.next
        curr = head
        while curr:
            
            if ele == 1:
                curr.next = curr.next.next
 
            ele -= 1

            prev = curr
            curr = curr.next
        return head
        


        
        
        
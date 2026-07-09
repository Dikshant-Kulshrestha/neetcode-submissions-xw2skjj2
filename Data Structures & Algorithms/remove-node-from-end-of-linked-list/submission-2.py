# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        
       #find length
        l =0
        curr = head
        while curr:
            l+=1 
            curr = curr.next

        
        ele = l-n

        #edge case
        if ele ==0:
            return head.next

        #remove the node
        curr = head
        while curr:
            
            if ele == 1:
                curr.next = curr.next.next
                break
 
            ele -= 1

            curr = curr.next
        return head
        


        
        
        
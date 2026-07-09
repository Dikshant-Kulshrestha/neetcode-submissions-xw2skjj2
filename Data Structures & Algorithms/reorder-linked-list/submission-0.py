# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        
        # finding half
        fast,slow = head.next, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        #reverse the second half
        second = slow.next
        prev = slow.next = None

        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt

        #merge these two lists
        first = head
        second = prev

        while second:
            tmp1,tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first = tmp1
            second = tmp2

        

        
        
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        
        self.res = []

        def bfs(root):
            if not root:
                return 0
                        
            q = deque([root])
            
            while q:
                
                for i in range(len(q)):
                    node = q.popleft()

                    if i==0:
                        self.res.append(node.val)

                    if node.right:
                        q.append(node.right)
    
                    if node.left:
                        q.append(node.left)
                   
        bfs(root)
        return self.res
                    
                    
                        
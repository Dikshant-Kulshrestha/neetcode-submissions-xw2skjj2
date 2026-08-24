# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        self.res = []        

        def bfs(root):
            if not root:
                return 0

            
            q = deque([root])

            while q:
                level =[]
                for i in range(len(q)):
                    node = q.popleft()
                    level.append(node.val)
                    
                    
                    if node.left:
                        q.append(node.left)
                    if node.right:
                        q.append(node.right)
                    
                self.res.append(level)

    
        bfs(root)
        return self.res
    
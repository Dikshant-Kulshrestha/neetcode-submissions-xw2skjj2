class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        
        res = []
        sol = []

        def dfs(i):
            #are we at leaf node?
            if i == len(nums):
                res.append(sol.copy())
                return
            
            # include nums[i] in solution
            sol.append(nums[i])
            dfs(i+1)

            #not include in sol
            sol.pop()
            dfs(i+1)
        dfs(0)
        return res
                
        
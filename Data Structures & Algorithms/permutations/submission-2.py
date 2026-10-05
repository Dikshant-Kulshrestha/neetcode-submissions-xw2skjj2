class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res,sol = [],[]

        def backtrack():

            if len(sol) == len(nums):
                res.append(sol.copy())
                return
            
            for x in nums:
                if x not in sol:
                    sol.append(x)
                    backtrack()
                    sol.pop()
        backtrack()
        return res
        
        
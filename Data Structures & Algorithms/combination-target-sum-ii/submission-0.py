class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        res,sol =[],[]
        candidates.sort()

        n = len(candidates)


        def backtrack(i,curr_sum):

            if curr_sum == target:
                res.append(sol.copy())
                return
            
            if curr_sum>target or i == n:
                return
            
            #skip curr ele
            j = i+1
            while j<n and candidates[j] == candidates[i]:
                j += 1

            backtrack(j,curr_sum)


            #consider current ele
            sol.append(candidates[i])
            backtrack(i+1,curr_sum+candidates[i])
            sol.pop()
        
        backtrack(0,0)
        return res
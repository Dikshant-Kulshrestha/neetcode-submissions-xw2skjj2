class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        l,r = 0, k
        res = []

        while r<= len(nums):
            great = max(nums[l:r])
            res.append(great)
            l += 1
            r += 1

        return res
        
        


        
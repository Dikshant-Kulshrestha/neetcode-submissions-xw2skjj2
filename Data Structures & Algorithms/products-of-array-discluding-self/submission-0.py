class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        
    #all elements multiplied before it

        prefix = 1
        n = len(nums)
        res = [1]*n

        for i in range(n):
            res[i] = prefix
            prefix = prefix * nums[i]

    #all elements after it

        postfix = 1
        for i in range (n-1, -1, -1):
            res[i] = res[i] * postfix
            postfix = postfix * nums[i]

        return res
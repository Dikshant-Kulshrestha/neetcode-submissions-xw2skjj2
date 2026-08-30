class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        
        seen = {} #store val:index

        for i, n in enumerate(nums):
            compliment = target - n
            #look for it in hashmap, return if found
            if compliment in seen:
                return [seen[compliment], i]

            seen[n] = i

                
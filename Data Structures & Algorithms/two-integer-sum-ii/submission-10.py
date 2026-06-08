class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:

        r = len(numbers)- 1
        l = 0


        while l<r:
            twoSum = numbers[l] + numbers[r]

            if twoSum<target:
                l += 1
            elif twoSum>target:
                r -= 1
            else:
                return [l+1,r+1]
            
        
            
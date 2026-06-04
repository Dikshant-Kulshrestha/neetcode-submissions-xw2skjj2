class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        
        n = len(numbers)
        R = n-1
        L = 0

        while L<R:
            res = numbers[L] + numbers[R]

            if res>target:
                R -= 1
            elif res<target:
                L += 1
            else:
                return [L+1, R+1]
        
            
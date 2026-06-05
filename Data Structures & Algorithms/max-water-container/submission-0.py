class Solution:
    def maxArea(self, heights: List[int]) -> int:
        

        res = 0
        r = len(heights) -1
        l = 0

        while l<r:
            area = (r-l) * min(heights[r], heights[l])
            res = max(area,res)

            if heights[l]<heights[r]:
                l += 1
            elif heights[l]>heights[r]:
                r -= 1
            else:
                r -=1
        
        return (res)
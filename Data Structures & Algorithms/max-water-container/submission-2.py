class Solution:
    def maxArea(self, heights: List[int]) -> int:

        l =0
        r = len(heights)-1

        res = 0

        while l<r:
            area = (r-l) * min(heights[l],heights[r])
            res = max(area,res)

            if heights[l]<heights[r]:
                l += 1
                continue

            if heights[r]<heights[l]:
                r -= 1
                continue
            
            else:
                l += 1
        return (res)
            

        
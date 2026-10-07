class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        max_area = 0


        def dfs(i,j):

            if i<0 or i>=m or j<0 or j>=n or grid[i][j]!= 1:
                return 0
            else:
                grid[i][j] = 0
                area = 1
                area += dfs(i,j+1)
                area += dfs(i-1,j)
                area += dfs(i+1,j)
                area += dfs(i,j-1)

            return area
        

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    area = dfs(i,j)
                    max_area = max(area,max_area)
        
        return max_area

        
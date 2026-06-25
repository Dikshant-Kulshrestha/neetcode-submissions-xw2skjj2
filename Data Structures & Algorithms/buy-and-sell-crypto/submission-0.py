class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l,r = 0, 1
        maxProfit = 0

        while r<len(prices):
            #profitable?
            if prices[r]>prices[l]:
                profit = prices[r] - prices[l]
                maxProfit = max(maxProfit, profit)
            else:
                l = r
            r += 1
            
        return (maxProfit)
            

        
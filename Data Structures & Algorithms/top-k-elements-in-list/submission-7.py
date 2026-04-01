class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        

        group = defaultdict(int)

        for i, num in enumerate(nums):
            group[num] += 1


        res = sorted(group, key = group.get, reverse = True)
        return res[:k]

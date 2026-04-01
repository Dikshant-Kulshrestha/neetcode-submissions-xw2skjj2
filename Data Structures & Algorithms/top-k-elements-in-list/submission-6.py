class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        
        frequency_counter = Counter(nums)

        most_frequent_k = frequency_counter.most_common(k)

        res = []
        for num, count in most_frequent_k:
            res.append(num)

        return res
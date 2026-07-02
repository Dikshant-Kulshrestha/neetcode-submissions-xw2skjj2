class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        l,r = 0,0
        maxLen = 0
        sub = set()

        while r<len(s):
            while s[r] in sub:
                sub.remove(s[l])
                l += 1
            else:
                sub.add(s[r])
                r += 1
                maxLen = max(maxLen, len(sub))
        return (maxLen)
        
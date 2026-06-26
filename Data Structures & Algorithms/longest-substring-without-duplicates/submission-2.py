class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        maxlength = 0
        l,r = 0,0
        sub = set()
        # sub.add(s[0])

        while r<len(s):
            while s[r] in sub:
                sub.remove(s[l])
                l += 1
            else:
                sub.add(s[r])
                r += 1
                maxlength = max(len(sub), maxlength)
        return (maxlength)

        
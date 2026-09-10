class Solution:

    def encode(self, strs: List[str]) -> str:
        res = ""
        for word in strs:
            res += str(len(word))+"#"+word
        print(res)
        return res

    def decode(self, s: str) -> List[str]:

        
        i=0
        res = []
        print(s)

        while i<len(s):
            j=i
            while s[j] != "#":
                j = j+1
            length = int(s[i:j])
            
            #word extraction
            word = s[j+1: (j+length+1)]
            res.append(word)

            i = j+1+length
                
        
        return res

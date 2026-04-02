class Solution:

    def encode(self, strs: List[str]) -> str:

        encoded = ""
        for word in strs:
            length = len(word)
            encoded += str(length) + "#" + word

        return encoded


    def decode(self, s: str) -> List[str]:
        
        res = []
        i=0
        print(s)

        while i<len(s):
            j=i
            while s[j] != "#":
                j = j+1

            length = int(s[i:j])

            #word extraction
            word = s[j+1: (j+1+length)]
            res.append(word)

            i = j+1+length
        
        print(res)
        return res


            



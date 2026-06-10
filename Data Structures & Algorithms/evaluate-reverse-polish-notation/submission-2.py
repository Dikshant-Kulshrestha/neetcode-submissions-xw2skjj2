class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        res = 0
        stack = []

        for token in tokens:
            if token in {"+","-","*","/"}:
                a = stack.pop()
                b = stack.pop()

                if token == "+":
                    res = (a+b)
                elif token == "-":
                    res = (b-a)
                elif token == "*":
                    res = a*b
                elif token == "/":
                    res = int(b/a) 

                stack.append(res)
            else:
                stack.append(int(token))
        return (stack[0])    

                

        
        
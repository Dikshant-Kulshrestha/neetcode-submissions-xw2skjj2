class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        
        cars = list(zip(position,speed))
        # cars.sort(reverse = True)
        stack = [] #store time

        for pos,sp in sorted(cars, reverse=True):
            time = (target-pos) / sp
            if not stack or time>stack[-1]:
                stack.append(time)
        
        return len(stack)
        
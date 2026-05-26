class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        #check row
        for row in board:
            seen = set()

            for num in row:
                if num == ".":
                    continue
                if num in seen:
                    return False
                
                seen.add(num)

        #check column
        for col in range(9):
            seen = set()
            for row in range(9):
                num = board[row][col]
                if num == ".":
                    continue
                if num in seen:
                    return False
                
                seen.add(num)

        #check 9x9 box

        for box_row in range(0,9,3):
            for col_row in range(0,9,3):

                seen = set()

                for row in range(box_row, box_row+3):
                    for col in range(col_row, col_row+3):
                        num = board[row][col]

                        if num == ".":
                            continue
                        if num in seen:
                            return False
                        
                        seen.add(num)
        return True

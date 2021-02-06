class Halma:
    def __init__(self):
        self.tbstate = [
            ["WH", "WH", "WH", "WH", "WH", ".", ".", ".", ".", "."],
            ["WH", "WH", "WH", "WH", ".", ".", ".", ".", ".", "."],
            ["WH", "WH", "WH", ".", ".", ".", ".", ".", ".", "."],
            ["WH", "WH", ".", ".", ".", ".", ".", ".", ".", "."],
            ["WH", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "BK"],
            [".", ".", ".", ".", ".", ".", ".", ".", "BK", "BK"],
            [".", ".", ".", ".", ".", ".", ".", "BK", "BK", "BK"],
            [".", ".", ".", ".", ".", ".", "BK", "BK", "BK", "BK"],
            [".", ".", ".", ".", ".", "BK", "BK", "BK", "BK", "BK"]
        ]

        # Black Player always starts
        self.pturn = "WH"

    # Draws Halma Board in console
    def draw_halma_board(self):
        boardTop = "┌" + "┬".join(["─" * 4] * 10) + "┐\n"
        boardBottom = "└" + "┴".join(["─" * 4] * 10) + "┘"
        boardMiddle = "├" + "┼".join(["─" * 4] * 10) + "┤\n"
        print(boardTop +
              boardMiddle.join(
                  "│" +
                  "│".join(' {} '.format(self.tbstate[x][y] if self.tbstate[x][y] != "." else "  ")
                           for y in range(10)) +
                  "│\n"
                  for x in range(10)) +
              boardBottom)

    # Determinates if coordinates sent are valid
    def is_valid_cord(self, cx, cy):
        return True if 0 <= cx < 10 and 0 <= cy < 10 else False

    # Determinates if is a valid move
    def is_valid_move(self, dx, dy):
        if not self.is_valid_cord(dx, dy): return False
        return True if self.tbstate[dx][dy] == "." else False

    # Determinates if is a valid hop
    def is_valid_hope(self, dx, dy, ox, oy):
        if not self.is_valid_cord(dx, dy): return False
        return True if self.tbstate[dx][dy] == "." and  self.tbstate[(dx + ox) / 2][(dy + oy) / 2] != "." else False

    # Determinates if game has ended and returns the winner in each case
    def is_winner(self, isBlack=True):
        # Black Wins
        isCornerFull = True

        # Checking if white corner camp is full
        for x in range(5):
            if not isCornerFull: break
            for y in range(5-x):
                if self.tbstate[x if isBlack else 9 - x][y if isBlack else 9 - y] == ".":
                    isCornerFull = False
                    break

        # Cheking if is at least one black piece is on to declare black winning
        if isCornerFull:
            for x in range(5):
                for y in range(5-x):
                    if isBlack:
                        if self.tbstate[x][y] == "BK": return "BK"
                    else:
                        if self.tbstate[9 - x][9 - y] == "WH": return "WH"


        return None

    def generate_childs(self):
        generated_childs = []
        for x in range(10):
            for y in range(10):
                if self.tbstate[x][y] == self.pturn:
                    for z in range(x - 1, x + 2):
                        for w in range(y - 1, y + 2):
                            if not (x == z and y == w):
                                if self.is_valid_move(z, w):
                                    generated_childs.append([[y, x], [w, z]])
                                elif self.is_valid_move(2*z-x, 2*w-y):
                                    generated_childs.append([[y, x], [2*w-y, 2*z-x]])

        return generated_childs


if __name__ == '__main__':
    halmaGame = Halma()
    halmaGame.draw_halma_board()
    num = halmaGame.generate_childs()
    print("Numero de Hijos: {}".format(len(num)))
    print("Hijos:\n",num)
    # print(halmaGame.is_winner())

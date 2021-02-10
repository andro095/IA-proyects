import math
import time

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
        return True if self.tbstate[dx][dy] == "." and  self.tbstate[(dx + ox) // 2][(dy + oy) // 2] != "." else False

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

    def generate_childs(self, turn):
        generated_childs = []
        visitated_pos = []
        for y in range(10):
            for x in range(10):
                if self.tbstate[y][x] == turn:
                    for w in range(y - 1, y + 2):
                        for z in range(x - 1, x + 2):
                            if not (y == w and x == z):
                                if self.is_valid_move(w, z):
                                    generated_childs.append([[y, x], [w, z]])
                                elif self.is_valid_move(2*w-y, 2*z-x):
                                    generated_childs.append([[y, x], [2*w-y, 2*z-x]])
                                    visitated_pos.append([y, x])
                                    if [2*w-y, 2*z-x] not in visitated_pos:
                                        origins = [[y, x]]
                                        new_generated_childs, visitated_pos = self.gen_derivated_child(2*w-y, 2*z-x, origins, visitated_pos)
                                        generated_childs += new_generated_childs

        return generated_childs

    def gen_derivated_child(self, cy, cx, origins, visitated_pos):
        generated_childs = []
        for y in range(cy - 1, cy + 2):
            for x in range(cx - 1, cx + 2):
                if not (cy == y and cx == x):
                    if self.is_valid_hope(2*y-cy, 2*x-cx, cy, cx):
                        if [2*y-cy, 2*x-cx] not in origins:
                            generated_childs.append([[origins[0][0], origins[0][1]], [2*y-cy, 2*x-cx]])
                            visitated_pos.append([cx, cy])
                            if [2*y-cy, 2*x-cx] not in visitated_pos:
                                origins.append([cy, cx])
                                new_generated_childs, visitated_pos = self.gen_derivated_child(2*y-cy, 2*x-cx, origins, visitated_pos)
                                generated_childs += new_generated_childs

        return generated_childs, visitated_pos

    def gen_value(self, op, cy, cx):
        goal_val = abs((cx + cy - 14)/math.sqrt(2)) if self.pturn == "WH" else abs((cx + cy - 4)/math.sqrt(2))
        op_val = math.sqrt((cy - op[0])**2 + (cx - op[1])**2)
        reg_val = 0
        for y in range(cy - 1, cy + 2):
            for x in range(cx - 1, cx + 2):
                if self.is_valid_cord(y, x):
                    if self.tbstate[y][x] != ".":
                        if self.is_valid_hope(2*cy-y, 2*cx-x, y, x):
                            reg_val += 1 if self.tbstate[cy][cx] == self.tbstate[y][x] else -1

        return goal_val * 0.25 + op_val * 0.35 + reg_val * 0.40


    def min(self, node, depth, alpha, beta):
        if depth == 3:
            return self.gen_value(node[0], node[1][0], node[1][1]), node[1][0], node[1][1], node[0][0], node[0][1]

        minv = 1000
        ox = None
        oy = None
        px = None
        py = None

        generated_childs = self.generate_childs("BK")

        for childnode in generated_childs:
            self.tbstate[childnode[1][1]][childnode[1][0]] = "BK"
            self.tbstate[childnode[0][1]][childnode[0][0]] = "."

            mval, max_y, max_x, o_y, o_x = self.max(childnode, depth + 1, alpha, beta)

            if mval < minv:
                minv = mval
                py = childnode[1][0]
                px = childnode[1][1]
                oy = childnode[0][0]
                ox = childnode[0][1]

            self.tbstate[childnode[1][1]][childnode[1][0]] = "."
            self.tbstate[childnode[0][1]][childnode[0][0]] = "BK"

            if minv <= alpha:
                return minv, py, px, oy, ox

            if minv < beta:
                beta = minv

        return minv, py, px, oy, ox


    def max(self, node, depth, alpha, beta):
        if depth == 3:
            return self.gen_value(node[0], node[1][0], node[1][1]), node[1][0], node[1][1], node[0][0], node[0][1]

        maxv = -1000

        ox = None
        oy = None
        px = None
        py = None

        generated_childs = self.generate_childs("WH")

        for childnode in generated_childs:
            self.tbstate[childnode[1][1]][childnode[1][0]] = "WH"
            self.tbstate[childnode[0][1]][childnode[0][0]] = "."

            mval, min_y, min_x, o_y, o_x = self.min(childnode, depth + 1, alpha, beta)

            if mval > maxv:
                maxv = mval
                py = childnode[1][0]
                px = childnode[1][1]
                oy = childnode[0][0]
                ox = childnode[0][1]

            self.tbstate[childnode[1][1]][childnode[1][0]] = "."
            self.tbstate[childnode[0][1]][childnode[0][0]] = "WH"

            if maxv >= beta:
                return maxv, py, px, oy, ox

            if maxv > alpha:
                alpha = maxv

        return maxv, py, px, oy, ox

    def play(self):
        while True:
            self.draw_halma_board()
            isBlackWinner = self.is_winner()
            isWhiteWinner = self.is_winner(isBlack=False)
            if isBlackWinner is not None or isWhiteWinner is not None:
                if isBlackWinner == "BK": print("Jugador Humano ha ganado")
                if isWhiteWinner == "WH": print("La computadora ha ganado")
                exit(3)

            if self.pturn == "BK":
                while True:
                    time_start = time.time()
                    mval, py, px, oy, ox = self.min([], 0, -1000, 1000)
                    time_end = time.time()
                    print("Resultado obtenido en {}s".format(round(time_end-time_start, 3)))
                    print("Movimiento Recomendado: De x = {} y = {} a x = {} y = {} ".format(ox + 1, oy + 1, px + 1, py + 1))
                    try:
                        iox = int(input("Ingresa la coordenada x de la ficha a mover: "))
                        ioy = int(input("Ingresa la coordenada y de la ficha a mover: "))
                        idx = int(input("Ingresa la coordenada x destino: "))
                        idy = int(input("Ingresa la coordenada y destino: "))
                        if self.is_valid_cord(ioy - 1, iox - 1) and self.is_valid_cord(idy - 1, idx - 1):
                            self.tbstate[ioy - 1][iox - 1] = "."
                            self.tbstate[idy - 1][idx - 1] = "BK"
                            self.pturn = "WH"
                            break
                        else:
                            print("Coordenadas no válidas. Ingresa de nuevo")
                    except Exception:
                        print("Coordenadas no válidas. Ingresa de nuevo")
            else:
                ml, cy, cx, oy, ox = self.max([], 0, -1000, 1000)
                self.tbstate[oy][ox] = "."
                self.tbstate[cy][cx] = "WH"
                self.pturn = "BK"


if __name__ == '__main__':
    halmaGame = Halma()
    halmaGame.play()

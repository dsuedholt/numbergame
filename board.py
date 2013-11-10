from math import ceil

class Board(object):
    
    ROW_LENGTH = 9

    default = (1, 2, 3, 4, 5, 6, 7, 8, 9,
               1, 1, 1, 2, 1, 3, 1, 4, 1,
               5, 1, 6, 1, 7, 1, 8, 1, 9)
    
    def __init__(self):
        self.board = list(Board.default)
    
    def cleanInput(self, p1, p2):
        if (isinstance(p1, tuple) and isinstance(p2, tuple)):
            p1 = p1[0] + p1[1] * Board.ROW_LENGTH
            p2 = p2[0] + p2[1] * Board.ROW_LENGTH

        elif not (isinstance(p1, int) and isinstance(p2, int)):
            raise ValueError("Tiles have to be represented as tuples or ints")

        if not self.valid(p1) or not self.valid(p2):
            print p1, p2
            raise ValueError("Tiles are not in the board")

        return p1, p2

    def cross(self, p1, p2):
        p1, p2 = self.cleanInput(p1, p2)

        if not self.crossable(p1, p2):
            raise ValueError("The two tiles can't be crossed out")
        self.board[p1] = 0
        self.board[p2] = 0
    
    def won(self):
        for i in self.board:
            if i != 0:
                return False
        return True
    
    def deadlock(self):
        for i in range(len(self.board)):
            for j in range(i+1, len(self.board)):
                if self.crossable(i, j):
                    return False
        return True
    
    def crossable(self, p1, p2):
        p1, p2 = self.cleanInput(p1, p2)

        # convenience
        if p1 > p2:
            p1, p2 = p2, p1

        if p1 == p2:
            return False
        val1 = self.board[p1]
        val2 = self.board[p2]
        if (val1 != val2 and val1 + val2 != 10) or val1 == 0:
            return False

        vert, horiz = (p2 - p1) % Board.ROW_LENGTH == 0, True

        # the values are ok, let's see if they're above...
        for i in range(p1 + Board.ROW_LENGTH, p2, Board.ROW_LENGTH):
            if self.board[i] != 0:
                vert = False
        # ...or next to each other
        for i in range(p1 + 1, p2):
            if self.board[i] != 0:
                horiz = False
        return vert or horiz


    def valid(self, p):
        return 0 <= p < len(self.board)
    
    def expand(self):
        self.board += [i for i in self.board if i != 0]

    def rows(self):
        return int(ceil(len(self.board) * 1./ Board.ROW_LENGTH))

    def iterator2D(self):
        for r in range(self.rows()):
            for c in range(Board.ROW_LENGTH):
                if r * Board.ROW_LENGTH + c >= len(self.board):
                    break
                yield r, c, self[r][c]

    def __getitem__(self, idx):
        """Return the row that can be accessed further"""
        if idx * Board.ROW_LENGTH >= len(self.board):
            raise IndexError("Row index {0} out of range".format(idx))
        return self.board[idx*Board.ROW_LENGTH : (idx+1)*Board.ROW_LENGTH]

    def __repr__(self):
        res = ""
        for i in range(int(ceil(len(self.board) * 1. / Board.ROW_LENGTH))):
            res += str(i) + ': '
            res += str(self[i])
            res += '\n'
        return res


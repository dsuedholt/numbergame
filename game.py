import pickle
from board import Board
from ui import *


class Game(object):

    def __init__(self):
        self.ui = GameWindow(self)
        self.board = None
        self.modified = False
        self.selectedTile = None
        self.boardView = None

    def getTileAt(self, r, c):
        return self.board[r][c]

    def start(self):
        if self.modified and not self.ui.confirmLeaveAction():
            return
        self.board = Board()
        self.boardView = BoardScene(self, Board.ROW_LENGTH,
                                    self.ui.centralWidget())
        self.ui.centralWidget().setScene(self.boardView)

    def save(self):
        path = str(self.ui.getSavePath())
        if not path:
            return
        if not path.endswith(".nbg"):
            path += ".nbg"
        with open(path, 'w') as f:
            pickle.dump(self.board, f)
        self.modified = False

    def load(self):
        if self.modified and not self.ui.confirmLeaveAction():
            return
        path = self.ui.getOpenPath()
        board = None
        try:
            with open(path, 'r') as f:
                board = pickle.load(f)
        except Error:
            self.ui.statusBar().showMessage(
                "Unable to load game :(", 3000
            )
        if board:
            self.modified = False
            self.board = board
            self.boardView = BoardScene(self, Board.ROW_LENGTH,
                                        self.ui.centralWidget())
            self.ui.centralWidget().setScene(self.boardView)

    def exit(self):
        if self.modified and not self.ui.confirmLeaveAction():
            return
        self.ui.close()

    def showInfo(self):
        self.ui.showMessage(
            "This game was written with Python and the PyQt4 library.\n" +
            "View the source code at the author's github page:\n" + 
            "\n\thttps://github.com/dsuedholt\n\n" + 
            "The game itself was not invented by me, but was shown\n" + 
            "to me by a malicious fellow student aiming to waste my time.",
            "About this game"
        )

    def showHelp(self):
        self.ui.showMessage(
            "The rules for this game are simple. Your goal is to\n" +
            "cross out all the numbers. You can cross out any two\n" +
            "numbers that are equal to another or add up to ten,\n" +
            "as long as they're directly next to or above each other.\n" +
            "If only crossed numbers lie between two other numbers,\n" +
            "they count as adjacent! Crossing over line breaks is also\n" +
            "allowed. When you can't make any more moves, the game\n" + 
            "will expand the board by adding every number you didn't\n" +
            "cross yet to the bottom of the board. Clicking any tile\n" +
            "will show you the tiles you can cross with the selected one." +
            "\n\nStart a new game by going to the \"Game\" menu or\n" +
            "by pressing Ctrl+N.",
            "How to play"
        )

    def handleClick(self, tileR, tileC):
        if not (0 <= tileR < self.board.rows()
                and 0 <= tileC < Board.ROW_LENGTH):
            return

        if self.board.isCrossed(tileR, tileC):
            self.ui.statusBar().showMessage(
                "You already crossed this one!", 3000
            )
            return
        if self.selectedTile:
            if (tileR, tileC) == self.selectedTile:
                for (r, c) in self.board.iterator2D():
                    if not self.board.isCrossed(r, c):
                        self.boardView.setTileStatus(r, c, TileItem.NORMAL)
                self.selectedTile = None

            elif self.board.crossable(self.selectedTile, (tileR, tileC)):
                self.board.cross(self.selectedTile, (tileR, tileC))
                self.boardView.setTileStatus(tileR, tileC, TileItem.CROSSED)
                self.boardView.setTileStatus(*self.selectedTile,
                                             status=TileItem.CROSSED)
                for (r, c) in self.board.iterator2D():
                    if not self.board.isCrossed(r, c):
                        self.boardView.setTileStatus(r, c, TileItem.NORMAL)
                self.selectedTile = None
                self.modified = True
                while self.board.deadlock():
                    self.ui.statusBar().showMessage(
                        "No more moves! Expanding Board", 3000
                    )
                    self.board.expand()
                    self.boardView.expand()
            else:
                self.ui.statusBar().showMessage(
                    "These two tiles can't be crossed!", 3000
                )

        else:
            self.boardView.setTileStatus(tileR, tileC, TileItem.SELECTED)
            self.selectedTile = (tileR, tileC)
            for (r, c) in self.board.iterator2D():
                if self.board.crossable(self.selectedTile, (r, c)):
                    self.boardView.setTileStatus(r, c, TileItem.AVAILABLE)
                elif (not self.board.isCrossed(r, c)
                      and (r, c) != self.selectedTile):
                    self.boardView.setTileStatus(r, c, TileItem.UNAVAILABLE)

        if self.board.won():
            self.ui.statusBar().showMessage(
                "You crossed all the tiles! You win!", 3000
            )

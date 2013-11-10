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
		if self.modified:
			#TODO: show message box to confirm
			pass
		self.board = Board()
		self.boardView = BoardScene(self, Board.ROW_LENGTH, self.ui.centralWidget())
		self.ui.centralWidget().setScene(self.boardView)

	def save(self):
		pass

	def load(self):
		pass

	def exit(self):
		pass

	def handleClick(self, tileX, tileY):
		if not (0 <= tileX < Board.ROW_LENGTH and 0 <= tileY < self.board.rows()):
			return

		if self.board[tileY][tileX] == 0:
			self.ui.statusBar().showMessage(
				"You already crossed this one!", 3000)
			return
		if self.selectedTile:
			if (tileX, tileY) == self.selectedTile:
				for (r, c, val) in self.board.iterator2D():
					if val != 0:
						self.boardView.setTileStatus(c, r, TileItem.NORMAL)
				self.selectedTile = None

			elif self.board.crossable(self.selectedTile, (tileX, tileY)):
				self.board.cross(self.selectedTile, (tileX, tileY))
				self.boardView.setTileStatus(tileX, tileY, TileItem.CROSSED)
				self.boardView.setTileStatus(*self.selectedTile, 
					status=TileItem.CROSSED)
				for (r, c, val) in self.board.iterator2D():
					if val != 0:
						self.boardView.setTileStatus(c, r, TileItem.NORMAL)
				self.selectedTile = None
				self.modified = True
				while self.board.deadlock():
					self.ui.statusBar().showMessage(
						"No more moves! Expanding Board", 3000)
					self.board.expand()
					self.boardView.expand()
			else:
				self.ui.statusBar().showMessage(
					"These two tiles can't be crossed!", 3000)

		else:
			self.boardView.setTileStatus(tileX, tileY, TileItem.SELECTED)
			self.selectedTile = (tileX, tileY)
			for (r, c, val) in self.board.iterator2D():
				if self.board.crossable(self.selectedTile, (c, r)):
					self.boardView.setTileStatus(c, r, TileItem.AVAILABLE)
				elif val != 0 and (c, r) != self.selectedTile:
					self.boardView.setTileStatus(c, r, TileItem.UNAVAILABLE)

		if self.board.won():
			self.ui.statusBar().showMessage(
				"You crossed all the tiles! You win!", 3000)
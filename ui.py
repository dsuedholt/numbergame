from PyQt4 import QtGui, QtCore

class TileItem(QtGui.QGraphicsRectItem):

	CROSSED = 0
	NORMAL = 1
	SELECTED = 2
	AVAILABLE = 3
	UNAVAILABLE = 4

	def __init__(self, rect, number):
		super(TileItem, self).__init__(rect)
		self._status = TileItem.NORMAL
		self._number = number
		self.setBrush(self.getTileStyle())

	def paint(self, painter, option, widget):
		painter.setBrush(self.brush())
		radius = self.rect().width() / 10
		painter.drawRoundedRect(self.rect(), radius, radius)
		font = QtGui.QFont()
		font.setPixelSize(int(self.rect().height() * .75))
		painter.setFont(font)
		textoption = QtGui.QTextOption(QtCore.Qt.AlignCenter)
		painter.drawText(self.rect(), str(self.number()), textoption)


	def getTileStyle(self):
		brush = self.brush()
		if self.status() == TileItem.CROSSED:
			brush.setColor(QtCore.Qt.black)
			brush.setStyle(QtCore.Qt.Dense4Pattern)
		elif self.status() == TileItem.NORMAL:
			brush.setColor(QtGui.QColor(70, 235, 188))
			brush.setStyle(QtCore.Qt.SolidPattern)
		elif self.status() == TileItem.SELECTED:
			brush.setColor(QtGui.QColor(0, 0, 255))
			brush.setStyle(QtCore.Qt.SolidPattern)
		elif self.status() == TileItem.AVAILABLE:
			brush.setColor(QtGui.QColor(0, 255, 0))
			brush.setStyle(QtCore.Qt.SolidPattern)
		elif self.status() == TileItem.UNAVAILABLE:
			brush.setColor(QtGui.QColor(200, 50, 50))
			brush.setStyle(QtCore.Qt.SolidPattern)
		return brush


	def setStatus(self, status):
		self._status = status
		self.setBrush(self.getTileStyle())

	def status(self):
		return self._status

	def number(self):
		return self._number

class BoardScene(QtGui.QGraphicsScene):

	def __init__(self, game, row_length, parent):
		super(BoardScene, self).__init__(parent=parent)
		self.parent = parent
		self.game = game
		self.row_length = row_length
		self.tilewidth = (self.parent.width() - 
			self.parent.verticalScrollBar().width()) / self.row_length
		self.tiles = []
		self.expand()

	def setTileStatus(self, r, c, status):
		tile = self.tiles[r*self.row_length + c]
		tile.setStatus(status)
		tile.update()

	def expand(self):
		old_len = len(self.tiles)
		for (r, c) in self.game.board.iterator2D():
			if c + r*self.row_length < old_len:
				continue
			tile_rect = QtCore.QRectF(c*self.tilewidth, r*self.tilewidth,
				self.tilewidth, self.tilewidth)
			tile = TileItem(tile_rect, self.game.getTileAt(r, c))
			if self.game.board.isCrossed(r, c):
				tile.setStatus(TileItem.CROSSED)
			self.addItem(tile)
			self.tiles.append(tile)

	def redraw(self):
		self.tilewidth = (self.parent.width() - 
			self.parent.verticalScrollBar().width()) / self.row_length
		for (i, j) in self.game.board.iterator2D():
			self.tiles[j + i*self.row_length].setRect(
				j*self.tilewidth, i*self.tilewidth,
				self.tilewidth, self.tilewidth)
			self.tiles[j + i*self.row_length].update()

	def getTileIndex(self, x, y):
		return self.row_length * (y / self.tilewidth) + (x / self.tilewidth)

	def mousePressEvent(self, e):
		tileC, tileR = int(e.scenePos().x()), int(e.scenePos().y())
		self.game.handleClick(tileR / self.tilewidth, tileC / self.tilewidth)


class GameWindow(QtGui.QMainWindow):
	def __init__(self, game):
		super(GameWindow, self).__init__()
		self.game = game
		self.initUI()

	def showHelp(self):
		pass

	def showInfo(self):
		pass

	def confirmLeaveAction(self):
		reply = QtGui.QMessageBox.question(self, 'Are you sure?',
    		"Are you sure?\nUnsaved Progress will be lost.",
    		QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		return reply == QtGui.QMessageBox.Yes

	def getOpenPath(self):
		return QtGui.QFileDialog.getOpenFileName(self, "Load Game", "/home",
			"Save files (*.nbg)")

	def getSavePath(self):
		return QtGui.QFileDialog.getSaveFileName(self, "Save Game", "/home",
			"Save files (*.nbg)")


	def initUI(self):
		self.setGeometry(500, 400, 500, 300)
		self.setCentralWidget(QtGui.QGraphicsView(parent=self))
		self.setStyleSheet("background-color: gray;")
		self.setWindowTitle('Numbergame')
		off = QtCore.Qt.ScrollBarAlwaysOff
		on = QtCore.Qt.ScrollBarAlwaysOn
		self.centralWidget().setHorizontalScrollBarPolicy(off)
		self.centralWidget().setVerticalScrollBarPolicy(on)

		menubar = self.menuBar()

		statusbar = self.statusBar()
		statusbar.setStyleSheet("background-color: white")

		newGameAction = QtGui.QAction('&New', self)
		newGameAction.setShortcut('Ctrl+N')
		newGameAction.setStatusTip('Start a new game')
		newGameAction.triggered.connect(self.game.start)

		saveAction = QtGui.QAction('&Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save the Game')
		saveAction.triggered.connect(self.game.save)

		loadAction = QtGui.QAction('&Load', self)
		loadAction.setShortcut('Ctrl+O')
		loadAction.setStatusTip("Open a previous game")
		loadAction.triggered.connect(self.game.load)

		exitAction = QtGui.QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit the Game')
		exitAction.triggered.connect(self.game.exit)

		gameMenu = menubar.addMenu('&Game')
		gameMenu.addAction(newGameAction)
		gameMenu.addAction(saveAction)
		gameMenu.addAction(loadAction)
		gameMenu.addAction(exitAction)

		helpAction = QtGui.QAction('&Help', self)
		helpAction.setShortcut('F1')
		helpAction.setStatusTip('How do you play this?')
		helpAction.triggered.connect(self.showHelp)

		aboutAction = QtGui.QAction('&About', self)
		aboutAction.setShortcut('F2')
		aboutAction.setStatusTip('About this game')
		aboutAction.triggered.connect(self.showInfo)

		infoMenu = menubar.addMenu('&Info')
		infoMenu.addAction(helpAction)
		infoMenu.addAction(aboutAction)

		self.show()

	def resizeEvent(self, e):
		scene = self.centralWidget().scene()
		if scene:
			scene.redraw()

	def closeEvent(self, e):
		self.game.exit()
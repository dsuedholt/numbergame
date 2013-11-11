#!/usr/bin/env python2

import sys
from PyQt4 import QtGui
from game import Game


def main():
    app = QtGui.QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

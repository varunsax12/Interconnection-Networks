from PyQt4 import QtGui
from mainwindow import GuiMainWindow


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GuiMainWindow = GuiMainWindow()
    #GuiMainWindow.show()
    sys.exit(app.exec_())

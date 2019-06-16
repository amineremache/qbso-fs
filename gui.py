import PyQt5 as qt
import sys

app = qt.QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.setGeometry(100,100,500,300)
window.setWindowTitle("Test")

window.show()
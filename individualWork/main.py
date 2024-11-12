import sys
from PyQt5.QtWidgets import QApplication
from math_app import MathApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec()) 
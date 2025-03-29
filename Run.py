import sys
from PyQt5.QtWidgets import QApplication
from Main import Main_

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main_()
    main_window.showNormal()
    sys.exit(app.exec())
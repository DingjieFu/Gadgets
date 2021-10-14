# 用户：夜卜小魔王

import sys
from gui import UI
from PySide2.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.main_window.show()
    sys.exit(app.exec_())

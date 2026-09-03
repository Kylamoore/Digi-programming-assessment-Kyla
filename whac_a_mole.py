import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget
import random

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window presets
        self.setWindowTitle ("Whac-A-Mole")
        self.setFixedSize (500, 500)

        # make buttons
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range(4):
            row_buttons = []
            for col in range(4):
                button = QPushButton()
                button.setFixedSize(70, 70)
                grid_layout.addWidget(button, row, col)
                row_buttons.append(button)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_clicked(r, c))
            self.buttons.append(row_buttons)

        # create grid
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(grid_layout)

    # button actions
    def button_clicked(self, row, col):
        self.clicked_button = self.buttons[row][col]
        pass

# start game
app = QApplication(sys.argv)
window = GameWindow()
window.show()
sys.exit(app.exec())
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

        self.mole_status = None
        self.add_mole()

    # add mole when all the buttons are blank
    def add_mole(self):
        if self.mole_status is None:
            # choose a random button
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            # set that random button to mole
            self.buttons[row][col].setText("Mole")
            self.mole_status = (row, col)
            self.print_mole_status = (row+1, col+1)
            print (self.mole_status)

    # button actions
    def button_clicked(self, row, col):
        self.clicked_button = self.buttons[row][col]
        if (row, col) == self.mole_status:
            self.buttons[row][col].setText("")
            self.mole_status = None
            self.add_mole()

# start game
app = QApplication(sys.argv)
window = GameWindow()
window.show()
sys.exit(app.exec())
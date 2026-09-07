import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout
import random
from PyQt6.QtCore import QTimer

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window presets
        self.setWindowTitle ("Whac-A-Mole")
        self.setFixedSize (380, 400)

        self.score_label = QLabel("Score: 0")
        self.time_label = QLabel("60s")

        heading_h_box = QHBoxLayout()
        heading_h_box.addWidget(self.score_label)
        heading_h_box.addStretch()
        heading_h_box.addWidget(self.time_label)

        # make buttons grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
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

        main_layout = QVBoxLayout()
        main_layout.addLayout(heading_h_box)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        # create central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        # starting score and mole
        self.player_score_counter = 0
        self.mole_status = None
        # start first mole
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
        # if the button that was clicked is actually a mole, set it blank and add point
        if (row, col) == self.mole_status:
            self.buttons[row][col].setText("")
            self.mole_status = None
            self.player_score()
            self.add_mole()

    # add a point to the players score
    def player_score(self):
        self.player_score_counter = self.player_score_counter + 1
        print (self.player_score_counter)
        self.score_label.setText(f"Score: {self.player_score_counter}")


# start game
app = QApplication(sys.argv)
window = GameWindow()
window.show()
sys.exit(app.exec())
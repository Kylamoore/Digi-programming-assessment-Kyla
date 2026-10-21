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

        # set starting labels
        self.score_label = QLabel("Score: 0")
        self.time_label = QLabel("60s")

        # Store labels evenly across
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

        #create layout with everything evenly
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

        # set up timer
        self.time_left = 60
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

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
        # update score label
        self.score_label.setText(f"Score: {self.player_score_counter}")

    # update timer every second
    def update_timer(self):
        self.time_left = self.time_left - 1
        self.time_label.setText(f"{self.time_left}s")
        # stop game (disable buttons) when time runs out
        if self.time_left == 0:
            self.timer.stop()
            for row in self.buttons:
                for button in row:
                    button.setEnabled(False)
            

# start game
app = QApplication(sys.argv)
window = GameWindow()
window.show()
sys.exit(app.exec())
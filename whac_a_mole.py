import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QDialog, QSpinBox
import random
from PyQt6.QtCore import QTimer

# first dialog to ask for game settings
class StartDialog(QDialog):
    def __init__(self):
        super().__init__()

        # choose the elements of the dialog window
        self.setWindowTitle ("Whac-A-Mole - Settings")
        self. setFixedSize (200,200)

        # make the spinbox and restrict its inputs
        self.time_input_label = QLabel("Input a time between 15 and 60")
        self.time_input_choice = QSpinBox()
        self.time_input_choice.setMinimum(15)
        self.time_input_choice.setMaximum(60)

        self.time_input_choice.textChanged.connect(self.check_button_valid)

        # make start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.accept)

        # add everything to the layout
        settings_main_layout = QVBoxLayout()
        settings_main_layout.addWidget(self.time_input_label)
        settings_main_layout.addWidget(self.time_input_choice)
        settings_main_layout.addWidget(self.start_button)

        self.setLayout(settings_main_layout)

    def get_game_time(self):
        return self.time_input_choice.value()

    def check_button_valid(self):
        try:
            current_number_choice = int(self.time_input_choice.text())
        except ValueError:
            current_number_choice = 0

        if current_number_choice <= 60 and current_number_choice >= 15:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)


# start the dialog box to get game choices
app = QApplication(sys.argv)
first_dialog = StartDialog()
dialog_result = first_dialog.exec()

# game window
class GameWindow(QMainWindow):
    def __init__(self, game_time):
        super().__init__()

        # set window presets
        self.setWindowTitle ("Whac-A-Mole")
        self.setFixedSize (380, 400)

        # set starting labels
        self.score_label = QLabel("Score: 0")
        self.time_label = QLabel(f"{game_time}s")

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
        self.time_left = game_time
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
            

# start the game if the dialog box was succesful in what it was doing
if dialog_result == QDialog.DialogCode.Accepted:
    game_time = first_dialog.get_game_time()
    window = GameWindow(game_time=game_time)
    window.show()
    sys.exit(app.exec())

# close game if the dialog box was closed instead of "started" to pass to next window
else:
    sys.exit(0) # 0 is because the game cant give the computer a code when it finished(because it never started) so we give it one to make it happy :)
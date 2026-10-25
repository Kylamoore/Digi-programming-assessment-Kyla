import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QDialog, QLineEdit, QMessageBox
import random
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QIcon # QFont, QFontDatabase
import os

MIN_TIME = 15
MAX_TIME = 60
BG_COLOUR = "#836539"
BUTTON_BG_COLOUR = "#6e5531"

# first dialog to ask for game settings
class StartDialog(QDialog):
    def __init__(self):
        super().__init__()

        # choose the elements of the dialog window
        self.setWindowTitle ("Whac-A-Mole - Settings")
        self.setFixedSize (300,300)
        self.setStyleSheet(f"background-color: {BG_COLOUR}")

        # name input
        self.type_name_heading = QLabel("Enter name:")
        self.type_name_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_name_heading.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 15px")
        self.type_name_box = QLineEdit()
        self.type_name_box.setFixedSize(250, 25)
        self.type_name_box.setPlaceholderText("Name here")
        self.type_name_box.setStyleSheet (f"background-color: {BUTTON_BG_COLOUR}; color: #cd9f74; border: 2px solid #5e4726; border-radius: 6px")
        type_name_center_layout = QHBoxLayout()
        type_name_center_layout.addStretch()
        type_name_center_layout.addWidget(self.type_name_box)
        type_name_center_layout.addStretch()

        self.type_name_box.textEdited.connect(self.check_button_valid)

        # make the time input
        self.time_input_label = QLabel(f"Input a time between {MIN_TIME} and {MAX_TIME}:")
        self.time_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_input_label.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 15px")
        self.time_input_choice = QLineEdit()
        self.time_input_choice.setFixedSize(250, 25)
        self.time_input_choice.setPlaceholderText("Seconds")
        self.time_input_choice.setStyleSheet (f"background-color: {BUTTON_BG_COLOUR}; color: #cd9f74; border: 2px solid #5e4726; border-radius: 6px")
        
        time_choice_center_layout = QHBoxLayout()
        time_choice_center_layout.addStretch()
        time_choice_center_layout.addWidget(self.time_input_choice)
        time_choice_center_layout.addStretch()

        self.time_input_choice.textEdited.connect(self.check_button_valid)

        # make start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize (200,30)
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.accept)
        self.start_button.setStyleSheet (f"QPushButton {{background-color: {BUTTON_BG_COLOUR}; color: #cd9f74; border: 2px solid #5e4726; border-radius: 6px; font-weight: bold; font-size: 15px}}" \
        "QPushButton:disabled {background-color: #866a43; color: #c0a58b; border: 2px solid #5e4726; border-radius: 6px; font-weight: bold; font-size: 15px}")

        start_button_center_layout = QHBoxLayout()
        start_button_center_layout.addStretch()
        start_button_center_layout.addWidget(self.start_button)
        start_button_center_layout.addStretch()

        # add everything to the layout
        settings_main_layout = QVBoxLayout()
        settings_main_layout.addStretch()
        settings_main_layout.addWidget(self.type_name_heading)
        settings_main_layout.addLayout(type_name_center_layout)
        settings_main_layout.addStretch()
        settings_main_layout.addWidget(self.time_input_label)
        settings_main_layout.addLayout(time_choice_center_layout)
        settings_main_layout.addStretch()
        settings_main_layout.addLayout(start_button_center_layout)
        settings_main_layout.addStretch()

        # set the layout
        self.setLayout(settings_main_layout)

    # make the game time and name accesible
    def get_game_time(self):
        return int(self.time_input_choice.text())

    def get_player_name(self):
        return (self.type_name_box.text())

    # check if the input is valid for time and disable button if it is not
    def check_button_valid(self):
        try:
            current_number_choice = int(self.time_input_choice.text())
        except ValueError:
            current_number_choice = 0

        if current_number_choice <= MAX_TIME and current_number_choice >= MIN_TIME and self.type_name_box.text() != "":
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)


# start the dialog box to get game choices
app = QApplication(sys.argv)
game_window = None
first_dialog = StartDialog()
dialog_result = first_dialog.exec()

# game window
class GameWindow(QMainWindow):
    def __init__(self, game_time, player_name):
        super().__init__()

        # set window presets
        self.setWindowTitle ("Whac-A-Mole")
        self.setFixedSize (380, 400)
        self.setStyleSheet(f"background-color: {BG_COLOUR}")

        # set starting labels
        self.score_label = QLabel("Score: 0")
        self.score_label.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 15px")
        self.time_label = QLabel(f"{game_time}s")
        self.time_label.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 15px")

        # make time avaliable for end screen
        self.game_time = game_time

        # layout
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
                hole_photo = QIcon()
                hole_photo.addFile("oval hole.png", QSize(67, 60), QIcon.Mode.Normal)
                hole_photo.addFile("oval hole.png", QSize(67, 60), QIcon.Mode.Disabled)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_clicked(r, c, hole_photo))
                button.setStyleSheet(f"QPushButton {{background-color: {BUTTON_BG_COLOUR}; border: 2px solid #5e4726; border-radius: 6px}}" \
        "QPushButton:disabled {background-color: #866a43; border: 2px solid #5e4726; border-radius: 6px}")
                button.setIcon(hole_photo)
                button.setIconSize(QSize(67, 60))
            self.buttons.append(row_buttons) 

        #create even game layout
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
        self.old_mole = None
        self.player_name = player_name

        # set up timer
        self.time_left = game_time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # start first mole
        self.add_mole()

    # add a little time before the next mole pops up
    def pause_before_mole(self):
        if self.mole_status is None:
            time_waiting = random.randint(50, 200)
            print (f"waiting {time_waiting}")
            QTimer.singleShot(time_waiting, self.add_mole)

    # add mole to random button when all the buttons are blank
    def add_mole(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        # set that random button to mole if it is not the same as previous mole
        while self.old_mole == (row, col):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            print ("dupe caught!")

        # make mole photo appear
        mole_photo = QIcon()
        mole_photo.addFile("mole_with_grass.png", QSize(60, 60), QIcon.Mode.Normal)
        mole_photo.addFile("mole_with_grass.png", QSize(60, 60), QIcon.Mode.Disabled)

        self.buttons[row][col].setIcon(mole_photo)
        self.buttons[row][col].setIconSize(QSize(60, 60))
        self.mole_status = (row, col)
        self.old_mole = (row, col)
        self.print_mole_status = (row+1, col+1)
        print (self.print_mole_status)

    # button actions
    def button_clicked(self, row, col, hole_photo):
        self.clicked_button = self.buttons[row][col]
        # if the button that was clicked is actually a mole, set it blank and add point
        if (row, col) == self.mole_status:
            self.buttons[row][col].setIcon(QIcon(hole_photo))
            self.mole_status = None
            self.player_score()
            self.pause_before_mole()

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
            self.end_dialog = EndDialog(self.player_score_counter, self.player_name, self)
            self.end_dialog.exec()

class EndDialog(QDialog):
    def __init__(self, end_score, player_name, game_window):
        super().__init__()
        self.game_window = game_window

        # make window
        self.setWindowTitle("Game Over!")
        self.setFixedSize(220,250)
        self.setStyleSheet(f"background-color: {BG_COLOUR}")

        # make heading, name heading, name input and play again button
        self.game_over_label = QLabel("Game Over!")
        self.game_over_label.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 25px")
        self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.player_name_label = QLabel(player_name)
        self.player_name_label.setStyleSheet("color: #cd9f74; font-weight: bold; font-size: 15px")
        self.player_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.end_score_label = QLabel(str(end_score))
        self.end_score_label.setStyleSheet("color: #cd9f74; font-weight: 1000; font-size: 60px")
        self.end_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.clicked.connect(self.play_again_clicked)
        self.play_again_button.setStyleSheet (f"background-color: {BUTTON_BG_COLOUR}; color: #cd9f74; border: 2px solid #5e4726; border-radius: 6px; font-weight: bold; font-size: 15px")

        main_stats_layout = QVBoxLayout()
        main_stats_layout.setSpacing(1)
        main_stats_layout.addWidget(self.player_name_label)
        main_stats_layout.addWidget(self.end_score_label)

        # add everything into the layout
        end_screen_layout = QVBoxLayout()
        end_screen_layout.addStretch()
        end_screen_layout.addWidget(self.game_over_label)
        end_screen_layout.addStretch()
        end_screen_layout.addLayout(main_stats_layout)
        end_screen_layout.addStretch()
        end_screen_layout.addWidget(self.play_again_button)
        end_screen_layout.addStretch()

        self.setLayout(end_screen_layout)

        self.append_score(end_score, player_name)

    # make the play again button actually start the game again
    def play_again_clicked(self):
        global game_window

        # close old game window when play again is clicked
        self.game_window.close()
        self.accept()

        new_dialog = StartDialog()

        #if starting again get the new/reset the time and name and start
        if new_dialog.exec() == QDialog.DialogCode.Accepted:
            game_time = new_dialog.get_game_time()
            player_name = new_dialog.get_player_name()

            # start new game
            game_window = GameWindow(game_time, player_name)
            game_window.show()

    # add score to file
    def append_score(self, end_score, player_name):
        try:
            with open("whack_a_mole_scores.txt", "a") as f:
                f.write(f"{self.game_window.game_time}s, {end_score}, {player_name}\n")
        except IOError as e:
            QMessageBox.critical(self, "File Error", f"Could not write to file.txt: {e}")
    
    # close the game window if the end dialog is closed due to pushing 'x' instead of playing again.
    def closeEvent(self, event):
        self.game_window.close()
        event.accept()


# start the game if the dialog box was succesful in what it was doing
if dialog_result == QDialog.DialogCode.Accepted:
    game_time = first_dialog.get_game_time()
    player_name = first_dialog.get_player_name()
    window = GameWindow(game_time, player_name)
    window.show()
    sys.exit(app.exec())

# close game if the dialog box was closed instead of "started" to pass to next window
else:
    sys.exit(0) # 0 is because the game cant give the computer a code when it finished(because it never started) so we give it one to make it happy :)
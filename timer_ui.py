from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QUrl
import csv_writer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class Timer_UI(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.player = QMediaPlayer()

        # Timer Type Names
        self.timer_types = ["IT", "Film & Photo", "TEFL"]

        # Timer Settings
        self.timer_setting = [(10 * 60), (25 * 60), (30 * 60), (40 * 60)]
        self.remaining_time = 0

        self.running_timer = None
        self.current_duration = 0

        # Timers
        timer_a = QTimer()
        timer_b = QTimer()
        timer_c = QTimer()
        timer_d = QTimer()

        # Grid Layout
        self.grid_layout = QtWidgets.QGridLayout()

         # Combobox Layout
        self.combobox = QtWidgets.QComboBox()
        self.combobox.setObjectName("combobox")
        self.combobox.setFixedSize(200, 60)
        self.grid_layout.addWidget(self.combobox, 0, 1, 1, 1)
        self.combobox.addItems(self.timer_types)


        # Section A layout
        self.hbox_a = QtWidgets.QHBoxLayout()


            # Intialize Label
        self.label_a1 = QtWidgets.QLabel(f"00:{int(self.timer_setting[0] / 60)}:00")
        self.label_a1.setObjectName('label_a1')
        self.label_a1.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.label_a1, 1, 0, 1, 1)
        self.label_a1.setStyleSheet('font-size: 25pt')
        
            # Initialize Buttons
        self.hbox_a_container = QWidget()
        self.hbox_a_container.setLayout(self.hbox_a)

        self.pushButton_a1 = QtWidgets.QPushButton("Start")
        self.hbox_a.addWidget(self.pushButton_a1)   
        
        self.grid_layout.addWidget(self.hbox_a_container, 2, 0, 1, 1)

       
        # Section B layout
        self.hbox_b = QtWidgets.QHBoxLayout()

            # Initialize Label
        self.label_b1 = QtWidgets.QLabel(f"00:{int(self.timer_setting[1] / 60)}:00")
        self.label_b1.setObjectName('label_b1')
        self.label_b1.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.label_b1, 1, 2, 1, 1)
        self.label_b1.setStyleSheet('font-size: 25pt')

            # Initialize Buttons
        self.hbox_b_container = QWidget()
        self.hbox_b_container.setLayout(self.hbox_b)

        self.pushButton_b1 = QtWidgets.QPushButton("Start")
        self.hbox_b.addWidget(self.pushButton_b1)
          
        
        self.grid_layout.addWidget(self.hbox_b_container, 2, 2, 1, 1)

        # Section C layout
        self.hbox_c = QtWidgets.QHBoxLayout()

            # Initialize Label
        self.label_c1 = QtWidgets.QLabel(f"00:{int(self.timer_setting[2] / 60)}:00")
        self.label_c1.setObjectName('label_c1')
        self.label_c1.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.label_c1, 3, 0, 1, 1)
        self.label_c1.setStyleSheet('font-size: 25pt')

            # Initialize Buttons
        self.hbox_c_container = QWidget()
        self.hbox_c_container.setLayout(self.hbox_c)

        self.pushButton_c1 = QtWidgets.QPushButton("Start")
        self.hbox_c.addWidget(self.pushButton_c1)
            
        
        self.grid_layout.addWidget(self.hbox_c_container, 4, 0, 1, 1)    

        # Section D layout
        self.hbox_d = QtWidgets.QHBoxLayout()


            # Initialize Label
        self.label_d1 = QtWidgets.QLabel(f"00:{int(self.timer_setting[3] / 60)}:00")
        self.label_d1.setObjectName('label_d1')
        self.label_d1.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.label_d1, 3, 2, 1, 1)
        self.label_d1.setStyleSheet('font-size: 25pt')

            # Initialize Buttons
        self.hbox_d_container = QWidget()
        self.hbox_d_container.setLayout(self.hbox_d)

        self.pushButton_d1 = QtWidgets.QPushButton("Start")
        self.hbox_d.addWidget(self.pushButton_d1)
           
        
        self.grid_layout.addWidget(self.hbox_d_container, 4, 2, 1, 1)

        
        # Set Grid layout to window
        self.setLayout(self.grid_layout)
        
    # Start / Reset Button Links
        self.pushButton_a1.clicked.connect(lambda: self.change_button(self.pushButton_a1, self.timer_setting[0], self.label_a1, timer_a, 0))
        self.pushButton_b1.clicked.connect(lambda: self.change_button(self.pushButton_b1, self.timer_setting[1], self.label_b1, timer_b, 1))
        self.pushButton_c1.clicked.connect(lambda: self.change_button(self.pushButton_c1, self.timer_setting[2], self.label_c1, timer_c, 2))
        self.pushButton_d1.clicked.connect(lambda: self.change_button(self.pushButton_d1, self.timer_setting[3], self.label_d1, timer_d, 3))

    
    # Audio Player Function
    def play_audio(self):
        audio_file = QUrl.fromLocalFile("timer_sound_modified.mp3")
        self.player.setMedia(QMediaContent(audio_file))
        self.player.play()


    def change_button(self, button, setting, current_label, timer, status):
        if self.running_timer == None or self.running_timer == status:

            self.current_duration = (setting // 60)
            self.running_timer = status

            if self.remaining_time == 0:
                self.remaining_time = setting - 1

            if button.text() == "Start":
                button.setText("Reset")

                try:
                    timer.timeout.disconnect()
                except TypeError:
                    pass
                
                timer.timeout.connect(lambda: self.update_timer(current_label, timer))
                timer.start(1000)
            
            else:
                button.setText("Start")
                self.reset_timer(current_label, timer, setting, status, button)
        else:
            pass
        

    def update_timer(self, current_label, timer):
        
        self.current_mode = self.combobox.currentText()
        if self.remaining_time > 0:
                seconds = self.remaining_time % 60
                minutes = (self.remaining_time // 60) % 60
                hours = self.remaining_time // 3600
                current_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
                self.remaining_time -= 1
        else:
                current_label.setText("00:00:00")
                timer.stop()
                csv_writer.write_to_csv(self.current_duration, self.current_mode)
                self.play_audio()
                self.running_timer = None

    def reset_timer(self, current_label, timer, setting, status, button):
        if self.running_timer == None or self.running_timer == status:
            timer.stop()
            self.player.stop()
            current_label.setText(f"00:{int(setting / 60)}:00")
            button.setText("Start")
            self.remaining_time = 0
            self.running_timer = None
        else:
            pass



    
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Timer_UI(None)
    window.resize(700, 450)
    window.show()
    sys.exit(app.exec_())

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

class About_page(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget



        
        

        self.paragraph = QLabel("""About the App

                                """)
        layout = QtWidgets.QVBoxLayout()  # Create a vertical layout
        layout.addWidget(self.paragraph)  # Add the label to the layout

        self.paragraph.setWordWrap(True)


        self.paragraph.setText("""
    <div style='line-height: 150%; font-size: 10pt;'>
    Hey there! This app is designed to help you stay focused. 
    It’s a simple focus timer that lets you track your sessions across different activities—so you can see not just how long you’ve focused, 
    but where your time is going. Originally built with students in mind, I’ve found it just as useful for freelancers and professionals. 
    Whether you're studying, working, or doing deep creative tasks, this app helps you stay on track.
</div>

<div style='line-height: 150%; font-size: 10pt;'>
    To get started, just head to the Timer page, choose one of the four focus timers, 
    and set your desired duration. You can view your progress on the Stats page.
</div>

<div style='line-height: 150%; font-size: 10pt;'>
    🔄 Note: The app is still in early development, so you'll need to restart it to refresh the stats page.
    Your feedback and support mean a lot—thank you for trying it out!
</div>           
                    
""")
        
        self.setLayout(layout)  
        # Aligmnent
        self.paragraph.setAlignment(QtCore.Qt.AlignCenter)

        

    

        

          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = About_page(None)
    window.resize(700, 450)
    window.show()
    sys.exit(app.exec_())

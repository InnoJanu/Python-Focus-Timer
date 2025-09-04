import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

import timer_ui

class Settings_Page(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Set up layout
        layout = QVBoxLayout()

        
        for label in range(3):
            vertical_box = QWidget()
            vertical_box_layout = QHBoxLayout()

            input_text = QLineEdit()
            input_text.setPlaceholderText("Custom 1")
            set_button = QPushButton('Set')
            
            vertical_box_layout.addWidget(input_text)
            vertical_box_layout.addWidget(set_button)
            
            vertical_box.setLayout(vertical_box_layout)
            layout.addWidget(vertical_box)

        

        # Add a button
        button = QPushButton("Click Me")
        layout.addWidget(button)

        # Set layout to the widget
        self.setLayout(layout)
        self.setWindowTitle("Basic PyQt5 Page")
        self.resize(400, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Settings_Page(None)
    window.show()
    sys.exit(app.exec_())
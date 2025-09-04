import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class Settings_Page(QWidget):
    def __init__(self, stacked_widget, timer_instance):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Set up layout
        layout = QVBoxLayout()

        # Set Input Boxes
        self.set_inputs = []

        input_count = 0
        for _ in range(3):
            set_input = QLineEdit()
            set_input.setPlaceholderText(timer_instance.combobox.itemText(input_count))
            layout.addWidget(set_input)

            self.set_inputs.append(set_input)
            input_count += 1

        apply_button = QPushButton('Apply')
        layout.addWidget(apply_button)
        
        apply_button.clicked.connect(lambda: update_combo_box())

        def update_type_list():
            for i, field in enumerate(self.set_inputs):
                text = field.text().strip()
                if text:
                    timer_instance.timer_types[i] = text
                    field.clear()
                    self.set_inputs[i].setPlaceholderText(text)

            print(timer_instance.timer_types)
        
        def update_combo_box():
            update_type_list()
            timer_instance.combobox.clear()
            timer_instance.combobox.addItems(timer_instance.timer_types)
            

        # Set layout to the widget
        self.setLayout(layout)
        self.setWindowTitle("Basic PyQt5 Page")
        self.resize(400, 200)

if __name__ == "__main__":
    print("=====================================")
    print("Use the main script to see settings")
    print("=====================================")
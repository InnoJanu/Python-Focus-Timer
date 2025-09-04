# PyQt Imports
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QHBoxLayout, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QSizePolicy



# Import Scripts
from timer_ui import Timer_UI
from graph import Graph_Window
from about import About_page
from settings import Settings_Page

colors1 = ['#4682A9', '#749BC2', '#91C8E4']
colors2 = ['#FBFBFB', '#789DBC', '#BCCCDC']

# Initialize application
app = QApplication(sys.argv)
stacked_widget = QStackedWidget()

# Add Timer Script to the stacked widget
timer_window = Timer_UI(stacked_widget)
stacked_widget.addWidget(timer_window)

graph_window = Graph_Window(stacked_widget)
stacked_widget.addWidget(graph_window)

about_window = About_page(stacked_widget)
stacked_widget.addWidget(about_window)

settings_window = Settings_Page(stacked_widget, timer_window)
stacked_widget.addWidget(settings_window)

# App Size
app_width = stacked_widget.width()
app_height = stacked_widget.height()


# Show the stacked Widget
stacked_widget.setCurrentIndex(0)

# Side bar
side_bar = QWidget()
side_bar_layout = QVBoxLayout()
side_bar_layout.setSpacing(0)
side_bar_layout.setContentsMargins(0, 0, 0, 0)
side_bar.setLayout(side_bar_layout)

button1 = QPushButton("Timers")
button2 = QPushButton("Stats")
button3 = QPushButton("About")
button4 = QPushButton("Settings")



side_bar_layout.addWidget(button1)
side_bar_layout.addWidget(button2)
side_bar_layout.addWidget(button3)
side_bar_layout.addWidget(button4)
side_bar_layout.addStretch()
side_bar.setMinimumWidth(100)

for button in [button1, button2, button3, button4]:
    button.setStyleSheet(f"""
        QPushButton {{
            border: none;
            background-color: #1a1a1a;
            color: white;
        }}

        QPushButton:hover {{
            background-color: {colors2[2]};
                         }}
    """)
    button.setFixedHeight(30)

side_bar.setStyleSheet("""
    background-color: #1a1a1a;
""")


app.setStyleSheet("""
    QWidget {
        background-color: #292929;
        color: #ffffff;
    }
                  
    QPushButton {
            background-color: gray;
        }
                  
    QComboBox {
        background-color: #222222;
        color: #ffffff;
        border: 1px solid #444444;
        padding: 5px;
    }
""")

    

# Button Functionallity
button1.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
button2.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
button3.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
button4.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))


# Main Layout
main_layout = QHBoxLayout()
main_layout.addWidget(side_bar, 1)
main_layout.addWidget(stacked_widget, 4)



window = QWidget()
window.setLayout(main_layout)
window.setWindowTitle("Focus Timer")

window.resize(1200, 800)

window.show()

# window.move(x, y)

sys.exit(app.exec_())


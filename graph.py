import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
import os

from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel
# Data imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Graph_Window(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.grid_layout = QGridLayout()
        self.figure_layout = QHBoxLayout()
        self.figure_container = QWidget()
        self.figure_container.setLayout(self.figure_layout)
        colors1 = ['#4682A9', '#749BC2', '#91C8E4']
        colors2 = ['#FBFBFB', '#789DBC', '#BCCCDC']


        # Data handling
        csv_path = 'timer_sessions.csv'
        df = pd.read_csv(csv_path)
        df.index = df.index + 1
        df['date'] = pd.to_datetime(df["date"])
        df['weekday'] = df['date'].dt.day_name()
        # Filters
        today = pd.Timestamp.today().normalize()
        current_monday = today - pd.Timedelta(days=today.weekday())
        current_sunday = current_monday + pd.Timedelta(weeks=0.9)
        current_week = df[(df['date'] <= today) & (df['date'] >= current_monday)]
        prev_monday = current_monday - pd.Timedelta(weeks=1)
        prev_sunday = current_monday - pd.Timedelta(days=1)
        prev_week = df[(df['date'] >= prev_monday) & (df['date'] <= prev_sunday)]

      # Reconstruct Full DataFrame
        full_dates = pd.date_range(start=current_monday, end=current_sunday)
        full_dates_df = pd.DataFrame({'date': full_dates})

        # Filter Categories for visulizations
        cur_study_filter = current_week[current_week['timer_type'] == 'Study']
        cur_study_filter = cur_study_filter[['date', 'duration']].groupby('date').sum().reset_index()

        s_cur_week_final = pd.merge(
            full_dates_df,
            cur_study_filter, 
            on='date',
            how='left'
        )
        s_cur_week_final['duration'] = s_cur_week_final['duration'].fillna(0)
        study_duration_list = s_cur_week_final['duration'].tolist()

        if not os.path.exists(csv_path) or pd.read_csv(csv_path).empty:
            self.main_layout = QVBoxLayout()

            # Botton Layout
            self.unavailable_text = QLabel('No Sessions Recorded')
            self.unavailable_text.setAlignment(Qt.AlignCenter)
            self.main_layout.addWidget(self.unavailable_text)

            self.setLayout(self.main_layout)
        else:
        
            # ----------------------------------------------------------------------------------------------------------------
            cur_business_filter = current_week[current_week['timer_type'] == 'Business']
            cur_business_filter = cur_business_filter[['date', 'duration']].groupby('date').sum().reset_index()

            b_cur_week_final = pd.merge(
                full_dates_df,
                cur_business_filter, 
                on='date',
                how='left'
            )
            b_cur_week_final['duration'] = b_cur_week_final['duration'].fillna(0)
            business_duration_list = b_cur_week_final['duration'].tolist()
            
            #-------------------------------------------------------------------------------------------------
            cur_reading_filter = current_week[current_week['timer_type'] == 'Reading']
            cur_reading_filter = cur_reading_filter[['date', 'duration']].groupby('date').sum().reset_index()

            r_cur_week_final = pd.merge(
                full_dates_df,
                cur_reading_filter, 
                on='date',
                how='left'
            )
            r_cur_week_final['duration'] = r_cur_week_final['duration'].fillna(0)
            reading_duration_list = r_cur_week_final['duration'].tolist()
            
            # Blocks
            self.today_total_focus = df[df['date'] == today]['duration'].sum()
            self.week_avg = current_week['duration'].sum() // (today.dayofweek + 1)
            self.week_total = current_week['duration'].sum()
        

            # Pie numbers
            total_study =  cur_study_filter['duration'].sum()
            total_business = cur_business_filter['duration'].sum()
            total_reading = cur_reading_filter['duration'].sum()
            
            

            
            # ================================================ Pie Chart ================================================
            # Data
            pie_labels = ['Study', 'Business', 'Reading']
            pie_sizes = [total_study, total_business, total_reading]
            pie_colors = colors1

            filtered_data = [(label, size, color) for label, size, color in zip(pie_labels, pie_sizes, pie_colors) if size > 0]

            # Create Figure and Canvas
            fig = Figure(figsize=(5, 5))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.set_title('Time Allocation', fontsize=18)

            fig.subplots_adjust(left=.3, right=.7, top=0.9, bottom=0.1)

            canvas.setMinimumSize(400, 300)

            

            if not filtered_data:
                # If all values are zero, show a fallback message
                ax.text(0.5, 0.5, 'No data to display', ha='center', va='center', fontsize=14)
                ax.axis('off')
            else:
                # Unpack the filtered data
                filtered_labels, filtered_sizes, filtered_colors = zip(*filtered_data)

            ax.pie(
                    filtered_sizes,
                    labels=filtered_labels,
                    colors=filtered_colors,
                    autopct='%1.1f%%',
                    startangle=140
                )
            ax.axis('equal')
            self.figure_layout.addWidget(canvas)
            # ================================================ Tiles ================================================
            # Calculations
            self.total_hours = self.week_total // 60
            self.total_mins = self.week_total % 60

            self.avg_hours = self.week_avg // 60
            self.avg_mins = self.week_avg % 60
            
            self.today_hours = self.today_total_focus // 60
            self.today_mins = self.today_total_focus % 60
            
            self.block1 = QWidget()
            self.block1_layout = QVBoxLayout()
            self.block1.setLayout(self.block1_layout)

            self.heading1 = QLabel("Daily Avg")
            self.sub_heading1 = QLabel(f"{self.avg_hours}h {self.avg_mins}m")

            self.block1_layout.addWidget(self.heading1)
            self.block1_layout.addWidget(self.sub_heading1)

            # Block 2
            self.block2 = QWidget()
            self.block2_layout = QVBoxLayout()
            self.block2.setLayout(self.block2_layout)

            self.heading2 = QLabel("Week Total")
            self.sub_heading2 = QLabel(f"{self.total_hours}h {self.total_mins}m")

            self.block2_layout.addWidget(self.heading2)
            self.block2_layout.addWidget(self.sub_heading2)

            # Block 3
            self.block3 = QWidget()
            self.block3_layout = QVBoxLayout()
            self.block3.setLayout(self.block3_layout)

            self.heading3 = QLabel("Today")
            self.sub_heading3 = QLabel(f"{self.today_hours}h {self.today_mins}m")  # Define these vars

            self.block3_layout.addWidget(self.heading3)
            self.block3_layout.addWidget(self.sub_heading3)

            # Add blocks to layout
            self.blocks_layout = QHBoxLayout()
            self.blocks_layout.addWidget(self.block1)
            self.blocks_layout.addWidget(self.block2)
            self.blocks_layout.addWidget(self.block3)

    # ============================= Bar Charts ============================================================

    # Switch Buttion
            self.cat1_button = QPushButton("Study")
            self.cat2_button = QPushButton("Business")
            self.cat3_button = QPushButton("Reading")  # New button

            self.button_layout = QHBoxLayout()
            self.button_container = QWidget()
            self.button_container.setLayout(self.button_layout)

            for button in [self.cat1_button, self.cat2_button, self.cat3_button]:
            
                self.button_layout.addWidget(button)
                button.setStyleSheet("color: black")

            self.last_btn = self.cat1_button

            self.cat1_button.clicked.connect(lambda: swith_charts(self.cat1_button, self.last_btn, 0))
            self.cat2_button.clicked.connect(lambda: swith_charts(self.cat2_button, self.last_btn, 1))
            self.cat3_button.clicked.connect(lambda: swith_charts(self.cat3_button, self.last_btn, 2))  # Connect signal

            def swith_charts(cur_btn, last_btn, index):
                
                cur_btn.setStyleSheet(f"""
                                            QPushButton {{
                                            background-color: {colors2[1]};
                                            color: white;
                                            }}
                                            QPushButton:hover {{
                                                background-color: {colors2[2]}
                                                }}
                                            
                                            """)
                if last_btn == cur_btn:
                    pass
                else:
                    last_btn.setStyleSheet(f"""
                                                QPushButton {{
                                                background-color: white;
                                                color: black
                                                }}
                                                QPushButton:hover {{
                                                background-color: {colors2[2]}
                                                }}
                                            """)
                    
                self.last_btn = cur_btn
                self.graph_widget.setCurrentIndex(index)

            self.button_container.setStyleSheet(f"""
                                                QPushButton {{
                                                background-color: white;
                                                border: none;
                                                padding: 0px;
                                                margin: 0px;
                                                }}

                                                QPushButton:hover {{
                                                background-color: {colors2[2]};
                                            }}

                                            """)
            
            self.cat1_button.setStyleSheet(f"""
                                                QPushButton {{
                                                background-color: {colors2[1]};
                                                border: none;
                                                color: white;
                                                }}

                                                QPushButton:hover {{
                                                background-color: {colors2[2]};
                                            }}
                                            """)
            self.button_layout.setSpacing(0)
            self.button_layout.setContentsMargins(0, 0, 0, 0)
            


            # Ensure all days are present
            all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            study_hours = [round(num / 60, 1) for num in study_duration_list]

            # Set up the first plot 
            self.figure1 = Figure(figsize=(8, 5))
            self.canvas1 = FigureCanvas(self.figure1)
            self.ax1 = self.figure1.add_subplot(111)

            # self.canvas1.setMinimumHeight(350)

            bars1 = self.ax1.bar(all_days, study_hours, color=colors1[0])
            self.ax1.set_title('Study Hours p/Day')
            self.ax1.set_ylabel('Hours')
            self.ax1.set_xlabel('')
            self.ax1.set_ylim(0, max(study_hours) + 1)

            # Add data labels on top of each bar
            for bar1 in bars1:
                height = bar1.get_height()
                self.ax1.annotate(
                f'{height}',
                xy=(bar1.get_x() + bar1.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom'
                )

            for heading in [self.heading1, self.heading2, self.heading3]:
                heading.setStyleSheet("font-size: 35px; font-weight: bold;")
                heading.setAlignment(Qt.AlignCenter)

            for heading in [self.sub_heading1, self.sub_heading2, self.sub_heading3]:
                heading.setStyleSheet("font-size: 25px;")
                heading.setAlignment(Qt.AlignCenter)

            # Duplicate graph below in red
            business_hours_r = [round(num / 60, 1) for num in business_duration_list]

            self.figure2 = Figure(figsize=(8, 5))
            self.canvas2 = FigureCanvas(self.figure2)
            self.ax2 = self.figure2.add_subplot(111)

            # self.canvas2.setMinimumHeight(350)

            bars2 = self.ax2.bar(all_days, business_hours_r, color=colors1[1])
            self.ax2.set_title('Business Hours p/Day')
            self.ax2.set_ylabel('Hours')
            self.ax2.set_xlabel('')
            self.ax2.set_ylim(0, max(business_hours_r) + 1)

            for bar in bars2:
                height = bar.get_height()
                self.ax2.annotate(
                f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom'
                )

            # Duplicate graph below in red
            reading_hours_r = [round(num / 60, 1) for num in reading_duration_list]  

            self.figure3 = Figure(figsize=(8, 5))
            self.canvas3 = FigureCanvas(self.figure3)
            self.ax3 = self.figure3.add_subplot(111)

            # self.canvas3.setMinimumHeight(350)

            bars3 = self.ax3.bar(all_days, reading_hours_r, color=colors1[2])
            self.ax3.set_title('Reading Hours p/Day')
            self.ax3.set_ylabel('Hours')
            self.ax3.set_xlabel('')
            self.ax3.set_ylim(0, max(reading_hours_r) + 1)

            for bar in bars3:
                height = bar.get_height()
                self.ax3.annotate(
                f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom'
                )

            

            self.graph_widget = QStackedWidget()
            self.graph_widget.addWidget(self.canvas1)
            self.graph_widget.addWidget(self.canvas2)
            self.graph_widget.addWidget(self.canvas3)


            self.top_widgets = QWidget()
            self.top_horizontal_layout = QHBoxLayout()
            self.top_widgets.setLayout(self.top_horizontal_layout)

            self.top_horizontal_layout.addWidget(canvas, 1)
            self.top_horizontal_layout.addWidget(self.block3, 1)
            self.top_horizontal_layout.addWidget(self.block1, 1)
            self.top_horizontal_layout.addWidget(self.block2, 1)

            
            
            self.main_layout = QVBoxLayout()

            # Botton Layout
            self.bottom_container = QWidget()
            self.bottom_layout = QVBoxLayout()
            self.bottom_container.setLayout(self.bottom_layout)

            self.bottom_layout.addWidget(self.button_container)
            self.bottom_layout.addWidget(self.graph_widget)

            self.bottom_layout.addStretch()
            self.bottom_layout.setSpacing(0)

        
            # Add Widgets to Main Layout
            self.main_layout.addWidget(self.top_widgets, 1)
            self.main_layout.addWidget(self.bottom_container)

            self.graph_widget.setCurrentIndex(0)


        self.setLayout(self.main_layout)
        


# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graph_Window(None)
    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import QWidget, QStackedWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel
import pandas as pd


class Graph_Window(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.grid_layout = QGridLayout()
        self.figure_layout = QHBoxLayout()
        self.figure_container = QWidget()
        self.figure_container.setLayout(self.figure_layout)

        self.top_widgets = QWidget()
        self.top_horizontal_layout = QHBoxLayout()
        self.top_widgets.setLayout(self.top_horizontal_layout)

        colors1 = ['#4682A9', '#749BC2', '#91C8E4']
        colors2 = ['#FBFBFB', '#789DBC', '#BCCCDC']

        self.graph_widget = QStackedWidget()

# ================================== Data Handeling ====================================================
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

            self.top_horizontal_layout.addWidget(canvas, 1)
            # ================================================ Tiles ================================================
           # Calculations
            self.total_hours = self.week_total // 60
            self.total_mins = self.week_total % 60

            self.avg_hours = self.week_avg // 60
            self.avg_mins = self.week_avg % 60
            
            self.today_hours = self.today_total_focus // 60
            self.today_mins = self.today_total_focus % 60
            
            # Set Text
            self.headings = [
                "Today",
                "Week Avg",
                "Week Total"
            ]
            
            self.sub_headings = [
                 f"{self.today_hours}h {self.today_mins}m",
                 f"{self.avg_hours}h {self.avg_mins}m",
                 f"{self.total_hours}h {self.total_mins}m",
            ]
            
            def create_blocks():
                count = 0
                for block in range(3):
                    #Intialize
                    self.block = QWidget()
                    self.block_layout = QVBoxLayout()
                    self.block.setLayout(self.block_layout)

                    self.heading = QLabel(self.headings[count])
                    self.block_layout.addWidget(self.heading)

                    self.sub_heading = QLabel(self.sub_headings[count])
                    self.block_layout.addWidget(self.sub_heading)

                    self.top_horizontal_layout.addWidget(self.block, 1)

                    # Style
                    self.heading.setStyleSheet("font-size: 40px")
                    self.heading.setAlignment(Qt.AlignCenter)
                    self.sub_heading.setStyleSheet("font-size: 25px")
                    self.sub_heading.setAlignment(Qt.AlignCenter)

                    count += 1
            create_blocks()

    # ============================= Category Buttons ============================================================
         # Category Buttons
            self.button_layout = QHBoxLayout()
            self.button_container = QWidget()
            self.button_container.setLayout(self.button_layout)

            categories = ["Study", "Business", "Reading"]
            self.cat_buttons = []

            def create_cat_buttons():
                for index, button in enumerate(categories, start=0):
                    self.cat_button = QPushButton(button)
                    self.cat_button.setStyleSheet("color: black")
                    self.button_layout.addWidget(self.cat_button)
                    self.cat_button.clicked.connect(lambda _, i=index: self.graph_widget.setCurrentIndex(i))
                    self.cat_buttons.append(button)

                    
            create_cat_buttons()
            self.button_layout.setSpacing(0)
            self.button_layout.setContentsMargins(0, 0, 0, 0)
            
# ================================== Bar Charts ============================================================
            def create_bar_charts():
                all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                study_hours = [round(num / 60, 1) for num in study_duration_list]
                business_hours_r = [round(num / 60, 1) for num in business_duration_list]
                reading_hours_r = [round(num / 60, 1) for num in reading_duration_list]
                selection_list = [study_hours, business_hours_r, reading_hours_r]
                
                count = 0

                for i in range(3):
                    self.figure4 = Figure(figsize=(8, 5))
                    self.canvas4 = FigureCanvas(self.figure4)
                    self.ax4 = self.figure4.add_subplot(111)

                    bars4 = self.ax4.bar(all_days, selection_list[count], color=colors1[count])
                    self.ax4.set_title('Study Hours p/Day')
                    self.ax4.set_ylabel('Hours')
                    self.ax4.set_xlabel('')
                    self.ax4.set_ylim(0, max(selection_list[count]) + 1)

                    for bar4 in bars4:
                        height = bar4.get_height()
                        self.ax4.annotate(
                        f'{height}',
                        xy=(bar4.get_x() + bar4.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom'
                        )
                    count += 1
                    self.graph_widget.addWidget(self.canvas4)
            create_bar_charts()
            
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
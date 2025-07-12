import csv
from datetime import date

# Define file path and current date
csv_file = r"timer_sessions.csv"
current_date = date.today()

# Ensure the directory exists
try:
    with open(csv_file, mode="x", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["session_id", "timer_type", "duration", "date"])
        writer.writeheader()
except FileExistsError:
    pass


def write_to_csv(duration, type):

    # Get the last Session Id
    def get_last_session_id():
        with open(csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)        
            dictionary = [row for row in reader]
            if not dictionary:
                return 0    
            last_session_id = dictionary[-1]["session_id"]
            return int(last_session_id)

    # Use the last Session Id to generate a new one buy incrementing by one
    def generate_session_id():
        last_session_id = get_last_session_id()
        if last_session_id >= 1:
            return last_session_id + 1
        else: 
            return 1
        
    new_session_id = generate_session_id()

    # Data format for CSV
    timer_sessions = [
        {
            "session_id": new_session_id,
            "timer_type": type,
            "duration": duration,
            "date": current_date,
        }
    ]

    # Write the data to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        for session in timer_sessions:
            writer = csv.DictWriter(file, fieldnames=["session_id", "timer_type", "duration", "date"])
            writer.writerow(session)

    print(f"Timer session data written to:\n{csv_file}")
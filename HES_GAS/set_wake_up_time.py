import tkinter as tk
from tkinter import filedialog
import command_exe_wake_up_time as time_param
import time
import get_response

def select_csv_file():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt the user to select a CSV file
    csv_file_path = filedialog.askopenfilename(
        title="Select the CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    return csv_file_path

def main():
    # Step 1: Get CSV file from user
    csv_file_path = select_csv_file()

    if not csv_file_path:
        print("No CSV file selected. Exiting...")
        return  
    
    time_param.execute_commands(csv_file_path)
    print('Wake up time is set')
    time.sleep(2)
    get_response.get_response(csv_file_path)

    print('response is downloaded')
    

if __name__ == '__main__':
    main()

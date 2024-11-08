import command_exe_mult_params as multi_params
import tkinter as tk
from tkinter import filedialog
import push_data
import wakeup_time_10_min
import get_response
import comparison
import time

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
    
    push_data.execute_commands(csv_file_path)
    print('Initial Data Downladed')
    time.sleep(2)
    multi_params.execute_commands(csv_file_path)
    print('ALl Commands fired')

    print('set wake up time')
    wakeup_time_10_min.wake_up_time(csv_file_path)

    time.sleep(700)
    print('All commands executed')
    
    print('set wake up time')
    wakeup_time_10_min.wake_up_time(csv_file_path)

    print('waiting for commands to get executed')

    time.sleep(700)
    print('All commands executed')
    
    push_data.execute_commands(csv_file_path)

    print('Data after changes is downloaded')
    time.sleep(2)

    print('get response data')
    get_response.get_response(csv_file_path)


    df1, df2 = comparison.load_csv()

    # Proceed only if both files were loaded successfully
    if df1 is not None and df2 is not None:
        # Define columns to exclude
        exclude_columns = ['meter_number', 'PF_Serial_Number', 'BP_Number', 'GA', 'project', 'battery_level_percentage']

        # Key column for merging and naming output file
        key_column = 'meter_number'

        # Check if meter numbers match in both files
        if df1[key_column].equals(df2[key_column]):
            # Use the first meter number as identifier for filename
            meter_number = str(df1[key_column].iloc[0])

            # Merge and compare the two DataFrames
            merged_data, highlight_data = comparison.compare_and_merge(df1, df2, key_column, exclude_columns)

            # Save and highlight differences in an Excel file
            comparison.save_and_highlight_excel(merged_data, highlight_data, meter_number)

            print(f"Comparison completed. Differences saved in 'result/comparison_{meter_number}.xlsx'.")
        else:
            print("Meter numbers do not match between the two files.")
    else:
        print("Operation cancelled or files not loaded correctly.")

    

if __name__ == '__main__':
    main()

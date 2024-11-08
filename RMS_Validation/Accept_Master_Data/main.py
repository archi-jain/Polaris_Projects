import tkinter as tk
from tkinter import scrolledtext
import subprocess

# Function to run a Python script and return its output
def run_script(script_func, result_text, *args):
    try:
        result = script_func(*args)  # Call the function and get the output

        # Clear the text area
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Running script\n")

        # Update the text color based on success or failure
        result_text.tag_configure("PASS", foreground="green")
        result_text.tag_configure("FAIL", foreground="red")
        result_text.tag_configure("ERROR", foreground="red")

        # Filter and color-code the relevant output lines
        for line in result.splitlines():
            if "PASS" in line:
                result_text.insert(tk.END, line + '\n', "PASS")
            elif "FAIL" in line:
                result_text.insert(tk.END, line + '\n', "FAIL")
            elif "ERROR" in line:
                result_text.insert(tk.END, line + '\n', "ERROR")
            else:
                result_text.insert(tk.END, line + '\n')

        result_text.insert(tk.END, "\n\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error running script: {str(e)}\n", "ERROR")

# Function to capture and display the output of accept_master.py
def run_accept_master():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Running Accept Master Tests\n")
    result_text.update()  # Ensure that the text area is updated before running the script

    # Run the accept_master.py script and capture the output
    try:
        process = subprocess.Popen(
            ['python', r'Accept_Master_Data\accept_master.py'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        stdout, stderr = process.communicate()

        # Display the output in the text area
        result_text.insert(tk.END, stdout)
        if stderr:
            result_text.insert(tk.END, stderr, "ERROR")

        result_text.insert(tk.END, "\n\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error running accept_master.py: {str(e)}\n", "ERROR")

def run_both_scripts():
    result_text.delete(1.0, tk.END)
    run_accept_master()

# Creating the main window
root = tk.Tk()
root.title("API Testing")

# Creating buttons
btn_both = tk.Button(root, text="All Scripts", command=run_both_scripts)
btn_accept_master = tk.Button(root, text="Run Accept Master", command=run_accept_master)

# Positioning buttons on the left
btn_both.grid(row=1, column=0, padx=10, pady=10, sticky="w")
btn_accept_master.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Creating a text area to display results on the right
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
result_text.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

# Configuring grid to make the result area expandable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Starting the GUI event loop
root.mainloop()

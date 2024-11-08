import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
from tkinter import filedialog

# Function to read login credentials from the file
def get_login_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

# Function to read unique meter data from CSV file
def get_unique_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        meter_numbers = {row.get('meter_number') for row in reader}  # Use a set to ensure unique values
    return list(meter_numbers)

# Function to log not found meters into a CSV file
def log_not_found_meter(not_found_meters):
    today_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    not_found_file = f"not_found_{today_date_time}.csv"
    
    # Write the not found meters to a CSV file
    with open(not_found_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['meter_number'])  # Header
        for meter in not_found_meters:
            writer.writerow([meter])
    print(f"Not found meters logged in {not_found_file}")

# Function to allow user to select a CSV file
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    return file_path

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Set the desired download file name
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

def execute_commands(csv_file_path):
    #  Set Chrome options to handle the download
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,  # Set custom download directory
        "download.prompt_for_download": False,       # Do not prompt for download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # Setup WebDriver with ChromeDriverManager
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    not_found_meters = []  # List to store not found meters

    try:
        # Step 1: Open the website
        driver.get('https://avdhaan.gas.polarisgrids.com/')

        # Step 2: Wait for the login page elements to load
        print("Waiting for login page...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login-email"]'))
        )

        # Step 3: Read login credentials from file
        username, password = get_login_credentials('login.txt')

        # Step 4: Enter the user ID
        print("Entering username...")
        username_field = driver.find_element(By.XPATH, '//*[@id="login-email"]')
        username_field.send_keys(username)

        # Step 5: Enter the password using the provided XPath
        print("Entering password...")
        password_field = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        password_field.send_keys(password)

        # Step 6: Submit the form
        print("Submitting login form...")
        password_field.send_keys(Keys.RETURN)

        # Step 7: Wait for the user to manually log in and complete OTP verification
        print("Please log in manually and complete OTP verification...")

        # Wait until the MDMS page loads after manual login
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
        )
        print("Login complete. Proceeding with the script...") 

        # Step 8: Navigate to the HES page after manual login
        driver.get('https://avdhaan.gas.polarisgrids.com/#/gas-distribution/office/hes')

        # Step 9: Wait for the HES page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
        )

        menu_item = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/div/div/div/ul/li[3]/a'))
        )

        # Step 10: Read all unique meter numbers from the selected CSV file
        meter_numbers = get_unique_meter_data_from_csv(csv_file_path)

        # Enter each unique meter number one by one before submitting
        for meter_number in meter_numbers:
            try:
                menu_item.click()
                time.sleep(5)

                print(f"Entering meter number: {meter_number}")
                meter_input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="react-select-26-input"]'))
                )
                meter_input_field.send_keys(meter_number)
                meter_input_field.send_keys(Keys.ENTER)
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing meter {meter_number}: {e}")
                not_found_meters.append(meter_number)
                continue  # Skip to the next meter

        # After entering all unique meter numbers, click on the submit button
        print("Clicking the submit button...")
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/div/div/div/div/div[3]/div/div[1]/div[3]/button'))
        )
        submit_button.click()
        time.sleep(5)

        # Step 12: Click the refresh icon a few times after submitting
        print("Clicking the refresh icon 2 times...")
        tab_2_container = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/div/div/div/ul/li[3]')
        refresh_icon_tab_2 = tab_2_container.find_element(By.XPATH, "(//*[local-name()='svg' and @id='refresh'])[3]")

        for _ in range(2):
            refresh_icon_tab_2.click()
            time.sleep(1)

        print("Clicking the download icon...")
        # Move to another element that does not trigger a tooltip
        other_element = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/div/div/div/div/div[3]/div/div[2]/div[1]/div[1]')
        ActionChains(driver).move_to_element(other_element).perform()
        
        time.sleep(3)
        download_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//*[local-name()='svg' and @id='download'])[3]"))
        )
        download_icon.click()
        time.sleep(10)

        # Rename the downloaded file with a timestamp
        files = os.listdir(download_dir)
        files = [f for f in files if f.endswith('.csv')]
        files.sort(key=lambda x: os.path.getctime(os.path.join(download_dir, x)))  # Sort by creation time

        # The most recent file should be the last one in the sorted list
        latest_file = files[-1]

        # Construct a new file name with the current date and time
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_file_name = f"{timestamp}_Meter_Profile.csv"
        new_file_path = os.path.join(download_dir, new_file_name)

        # Rename the downloaded file
        os.rename(os.path.join(download_dir, latest_file), new_file_path)

        # Print the path to the renamed file
        print(f"File saved as: {new_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        if not_found_meters:
            log_not_found_meter(not_found_meters)

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("No CSV file provided. Exiting...")
        exit()

    csv_file_path = sys.argv[1]  # Get the CSV file path from command line arguments
    execute_commands(csv_file_path)

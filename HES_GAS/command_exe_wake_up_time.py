import time
import csv
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.common.exceptions import TimeoutException

# Function to allow user to select a CSV file
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    return file_path

# Function to read login credentials from the file
def get_login_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

# Function to read meter number and command name from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number'), row.get('command_name'), row.get('hour'), row.get('min'), row.get('sec')  # Get the actual column names

# Function to log not found meters into a CSV file
def log_not_found_meter(not_found_meters, command_name):
    today_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    not_found_file = f"{command_name}_not_found_{today_date_time}.csv"
    
    # Write the not found meters to a CSV file
    with open(not_found_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['meter_number', 'command_name'])  # Header
        for meter in not_found_meters:
            writer.writerow(meter)
    print(f"Not found meters logged in {not_found_file}")

# Setup WebDriver with ChromeDriverManager
chrome_options = Options()
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

    # Step 5: Enter the password
    print("Entering password...")
    password_field = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    password_field.send_keys(password)

    # Step 6: Submit the form
    print("Submitting login form...")
    password_field.send_keys(Keys.RETURN)

    # Step 7: Wait for manual login (OTP verification)
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

    # Step 10: Ask the user to select the CSV file
    csv_file_path = select_csv_file()
    print(f"Selected CSV file: {csv_file_path}")

    # Loop through each row in the CSV file
    for meter_number, command_name, hour, min, sec in get_meter_data_from_csv(csv_file_path):
        try:
            time.sleep(1)

            # Step 11: Click the dropdown button
            print("Clicking on the dropdown button...")
            dropdown_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="notch"]'))
            )
            dropdown_button.click()

            time.sleep(1)

            print("Clicking on the previous button...")
            try:
                previous_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[4]/div/button[1]'))
                )
                previous_button.click()
            except TimeoutException:
                print("Previous button not found, skipping this process.")

            # Step 12: Click the meter option from the dropdown
            print("Clicking on the meter option...")
            meter_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/a'))
            )
            meter_option.click()

            time.sleep(1)

            print("Clicking on the select button...")
            select_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/form/div/div/div/div[2]/div'))
            )
            select_button.click()

            # Step 13: Enter the meter number from the CSV file
            print(f"Entering meter number: {meter_number}")
            meter_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/form/div/div/div/div[1]/div[2]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", meter_input)
            meter_input.send_keys(Keys.BACKSPACE)
            meter_input.send_keys(meter_number)
            time.sleep(2)

            # Automatically press the Enter key after filling the meter number
            meter_input.send_keys(Keys.ENTER)

            time.sleep(1)

            # Step 14: Click the next button
            print("Clicking on the next button...")
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[1]/div[2]/button[2]'))
            )
            next_button.click()

            print("Clicking on select button...")
            select_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div'))
            )
            select_button.click()

            # Step 15: Enter the command from the CSV file and press Enter
            print(f"Entering command: {command_name}")
            command_input = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/input'))
            )
            command_input.send_keys(Keys.BACKSPACE)
            command_input.send_keys(command_name)
            command_input.send_keys(Keys.RETURN)

            time.sleep(1)

            time_input = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="setClockValue"]'))
            )
            time_input.click()
            

            # Locate the hour, minute, and second input fields and set their values
            print("Setting the time values...")
            hour_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/input'))  # Replace with actual XPath for hour input
            )
            minute_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/input'))  # Replace with actual XPath for minute input
            )
            second_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[3]/input'))  # Replace with actual XPath for second input
            )

            hour_input.clear()
            hour_input.send_keys(hour)  # Set desired hour 
            minute_input.clear()
            minute_input.send_keys(min)  # Set desired minute 
            second_input.clear()
            second_input.send_keys(sec)  # Set desired second

            time.sleep(1)
            # Move to another element to give a input time delay
            other_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/a')
            ActionChains(driver).move_to_element(other_element).perform()

            time.sleep(2)

            # Click the Apply button after setting the time
            print("Clicking the apply button...")
            apply_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div[4]/div/button[2]'))  # Replace with actual XPath for apply button
            )
            apply_button.click()

            time.sleep(3)  # Wait for the command to process

        except Exception as e:
            print(f"Error processing meter {meter_number}: {e}")
            not_found_meters.append((meter_number, command_name))  # Log the meter number if any error occurs

finally:
    # Log any meters not found in a CSV file
    if not_found_meters:
        log_not_found_meter(not_found_meters, command_name)
    driver.quit()

import time
import csv
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Function to read login credentials from the file
def get_login_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password
    
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

# Function to read meter data from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number'), row.get('command_name')

# Get the user's Downloads directory
downloads_dir = Path.home() / "Downloads"
response_file_path = downloads_dir / "response.csv"

# Function to save response text to a CSV file
def save_response_to_csv(meter_number, command_name, response_text, file_name="response.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = response_file_path.is_file()

    with open(response_file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file does not exist
            writer.writerow(["Timestamp", "Meter Number", "Command Name", "Response Text"])
        # Write response data
        writer.writerow([timestamp, meter_number, command_name, response_text])

def get_response(csv_file_path):
# Setup WebDriver with ChromeDriverManager
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    not_found_meters = []  # List to store not found meters

    try:
        # Step 1: Open the website
        driver.get('https://avdhaan.gas.polarisgrids.com/#/login')

        # Step 2: Wait for the login page elements to load
        print("Waiting for login page...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login-email"]'))
        )

        # Step 3: Read login credentials from file
        username, password = get_login_credentials('login.txt')

        # Step 4: Enter the user ID
        username_field = driver.find_element(By.XPATH, '//*[@id="login-email"]')
        username_field.send_keys(username)

        # Step 5: Enter the password
        password_field = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        password_field.send_keys(password)

        # Step 6: Submit the form
        password_field.send_keys(Keys.RETURN)

        # Step 7: Wait for the user to manually log in and complete OTP verification
        print("Please log in manually and complete OTP verification...")

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

        # Loop through each row in the CSV file
        for meter_number, command_name in get_meter_data_from_csv(csv_file_path):
            try:
                time.sleep(2)
                # Step 5: Click on the filter SVG element using JavaScript
                print("Clicking on filter icon")
                filter_svg_xpath = '//*[@id="filter_table"]'
                filter_svg = WebDriverWait(driver, 80).until(
                    EC.element_to_be_clickable((By.XPATH, filter_svg_xpath))
                )
                filter_svg.click()
                time.sleep(1)

                # Enter meter number with retry logic to handle stale element error
                print('Clicking on meter input')
                meter_number_input = WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div[1]/div[2]/input'))
                )
                meter_number_input.click()
                meter_number_input.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                print('Entering meter number')
                meter_number_input.send_keys(meter_number)
                print('Pressing enter key')
                meter_number_input.send_keys(Keys.ENTER)
                
                time.sleep(2)
                
                print("Clicking on command input...")
                command_history = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//h4[@class="modal-title" and text()="Command history"]'))
                )
                actions = ActionChains(driver)
                actions.move_to_element(command_history).click().perform()

                time.sleep(1)

                command_input = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/div[2]/div/div[2]/div/div/div[1]/div[2]/input'))
                )
                command_input.click()
                command_input.send_keys(Keys.BACKSPACE)
                command_input.send_keys(command_name)
                time.sleep(1)

                print("Pressing Enter key for command name...")
                command_input.send_keys(Keys.ENTER)
                time.sleep(1)

                # Step 11: Wait for the "Apply" button and click it
                apply_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="apply"]'))
                )
                apply_button.click()
                time.sleep(2)

                # Step 12: Click on the eye icon to view the command details
                eye_icon = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "(//*[local-name()='svg' and @id='eyeIcon'])[1]"))
                )
                eye_icon.click()
                time.sleep(3)

                # Step 13: Retrieve and print the text from the specified div
                text_div = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/div[2]/div/div/div/div[2]'))
                )
                text_content = text_div.text
                print("Text in the div:", text_content)
                
                # Save the response text to response.csv
                save_response_to_csv(meter_number, command_name, text_content)

                time.sleep(1)
                cross_icon = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div[1]/button"))
                )
                cross_icon.click()

                print(f"Meter number {meter_number} processed successfully.")        

            except NoSuchWindowException:
                print("Browser window closed unexpectedly. Exiting loop.")
                break

            except Exception as e:
                print(f"Error processing meter {meter_number}: {e}")
                not_found_meters.append(meter_number)
                continue  # Skip to the next meter

    finally:
        if not_found_meters:
            print('Logs of meters not found:', not_found_meters)
        
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Provide CSV file...")
        get_response(select_csv_file())

        exit()

    csv_file_path = sys.argv[1]  # Get the CSV file path from command line arguments
    get_response(csv_file_path)

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

# Function to read login credentials from the file
def get_login_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

# Function to read meter number from CSV file
def get_meter_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('meter_number')  # Only get the meter number

# Function to read command names from CSV file
def get_commands_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row.get('command_name')  # Replace with the actual column name for command names

# Function to log not found meters into a CSV file
def log_not_found_meter(not_found_meters, command_name):
    today_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    not_found_file = f"{command_name}_not_found_{today_date_time}.csv"
   
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
    driver.get('https://avdhaan-new.gomatimvvnl.in/')

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

    # Step 7: Wait for the user to manually log in
    print("Please log in manually and complete OTP verification...")

    # Wait until the MDMS page loads after manual login
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/main'))
    )
    print("Login complete. Proceeding with the script...")

    time.sleep(5)
    
    # Step 8: Navigate to the HES page after manual login
    driver.get('https://avdhaan-new.gomatimvvnl.in/#/utility/uppcl/mdms')

    # Step 9: Wait for the MDMS page to load
    time.sleep(5)

    # Step 10: Click on the search icon (SVG element)
    try:
        print("Clicking on the search icon (SVG element)...")
        search_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/nav/div/ul/a'))
        )
        search_icon.click()
    except Exception as e:
        print(f"Error clicking on the search icon: {e}")

    # Step 11: Loop through each row in the CSV file to input meter numbers
    for meter_number in get_meter_data_from_csv('para_select.csv'):
        try:
            # Click on the input field using class name
            print(f"Searching for meter: {meter_number}...")
            input_field = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'mdms-search-text-input'))
            )
            
            # Use JavaScript to click the input field
            driver.execute_script("arguments[0].click();", input_field)

            # Clear the input field if necessary and enter the meter number
            input_field.clear()
            input_field.send_keys(meter_number)
            input_field.send_keys(Keys.RETURN)  # Press Enter to trigger the search

            # Add a delay to allow search results to load
            time.sleep(3)

            # Step 12: Click on the corresponding row with the entered meter number
            try:
                print(f"Clicking on the row for meter: {meter_number}...")
                meter_row = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f'//tr[td[contains(text(), "{meter_number}")]]'))
                )
                meter_row.click()
                
                # Wait for the new page to load
                time.sleep(5)

                # Scroll to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Optional: wait for scroll effect

                # Step 13: Click on "Other Commands"
                print("Clicking on 'Other Commands'...")
                other_commands_link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/main/div/div/div/div[4]/div/div[2]/ul/li[2]/a'))
                )
                other_commands_link.click()

                # Wait for 2 seconds after clicking "Other Commands" to allow the SVG element to load
                time.sleep(2)
                
                # Step 14: Click on the SVG icon using the new XPath with JavaScript execution
                try:
                    print("Clicking on the SVG icon...")
                    
                    svg_element = driver.find_element(By.CSS_SELECTOR, "svg.cursor-pointer")

                    # Scroll to the element if necessary and click on it
                    ActionChains(driver).move_to_element(svg_element).click().perform()

                    # Wait for 2 seconds after clicking the SVG icon for the card to pop up
                    time.sleep(5)

                    print("SVG icon clicked successfully, and the card has popped up.")

                    # Step 15: Loop through each command
                    for command_name in get_commands_from_csv('commands.csv'):
                        print("Clicking on the dropdown to select a command...")

                        # Wait for the dropdown's input field to become visible
                        input_field_dropdown = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/input')) 
                        )
                        input_field_dropdown.click()  # Click to focus on the dropdown
                        input_field_dropdown.clear()  # Clear any previous input
                        input_field_dropdown.send_keys(command_name)  # Type the command
                        time.sleep(1)  # Wait for suggestions to load
                        input_field_dropdown.send_keys(Keys.RETURN)  # Simulate pressing Enter
                        print(f"Typed '{command_name}' into the dropdown input and pressed Enter.")

                        # Step 16: Click the execute button
                        execute_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.ID, 'exec-command'))
                        )
                        execute_button.click()
                        print(f"Execute button clicked for command: {command_name}.")
                        time.sleep(2)  # Wait for the command to execute before continuing

                except Exception as e:
                    print(f"Error clicking on the SVG icon: {e}")
                    not_found_meters.append((meter_number, command_name))
                    continue  # Skip to the next meter

            except Exception as e:
                print(f"Error clicking on the meter row or 'Other Commands': {e}")
                not_found_meters.append((meter_number, command_name))
                continue  # Skip to the next meter
            
        except Exception as e:
            print(f"Error searching for meter {meter_number}: {e}")
            not_found_meters.append((meter_number, command_name))
            continue  # Move to the next row

finally:
    # Step 18: Log the not found meters into a CSV file
    log_not_found_meter(not_found_meters, "Commands Execution")

    # Close the browser
    driver.quit()

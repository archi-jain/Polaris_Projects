import requests
import csv
from datetime import datetime

# Function to fetch all daily data from the API
def fetch_all_daily_data(account_id):
    url = f'https://engine-web.test.gomatimvvnl.in/daily_energy_consumption/{account_id}/'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Ensure this returns a list of daily records
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Function to save all response data to a CSV file
def save_response_data_to_csv(account_id, data):
    csv_file = f"{account_id}_consumption.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow([
            "id", "created_at", "updated_at", "start_daily_datetime", "end_daily_datetime",
            "account_id", "meter_number", "energy_consumption_kwh", "energy_consumption_kvah",
            "energy_consumption_export_kwh", "energy_consumption_export_kvah", 
            "start_import_wh", "end_import_wh", "start_import_vah", "end_import_vah",
            "start_export_wh", "end_export_wh", "start_export_vah", "end_export_vah",
            "net_metering_flag", "max_demand", "multiplying_factor"
        ])
        for record in data:
            writer.writerow([
                record["id"],
                record["created_at"],
                record["updated_at"],
                record["start_daily_datetime"],
                record["end_daily_datetime"],
                record["account_id"],
                record["meter_number"],
                record["energy_consumption_kwh"],
                record["energy_consumption_kvah"],
                record["energy_consumption_export_kwh"],
                record["energy_consumption_export_kvah"],
                record["start_import_wh"],
                record["end_import_wh"],
                record["start_import_vah"],
                record["end_import_vah"],
                record["start_export_wh"],
                record["end_export_wh"],
                record["start_export_vah"],
                record["end_export_vah"],
                record["net_metering_flag"],
                record["max_demand"],
                record["multiplying_factor"],
            ])
    print(f"Response data saved to {csv_file}")

# Function to read consumption data from CSV file
def read_consumption_data_from_csv(account_id):
    csv_file = f"{account_id}_consumption.csv"
    data = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "id": row["id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "start_daily_datetime": row["start_daily_datetime"],
                "end_daily_datetime": row["end_daily_datetime"],
                "account_id": row["account_id"],
                "meter_number": row["meter_number"],
                "energy_consumption_kwh": float(row["energy_consumption_kwh"]),
                "energy_consumption_kvah": float(row["energy_consumption_kvah"]),
                "energy_consumption_export_kwh": float(row["energy_consumption_export_kwh"]),
                "energy_consumption_export_kvah": float(row["energy_consumption_export_kvah"]),
                "start_import_wh": float(row["start_import_wh"]),
                "end_import_wh": float(row["end_import_wh"]),
                "start_import_vah": float(row["start_import_vah"]),
                "end_import_vah": float(row["end_import_vah"]),
                "start_export_wh": float(row["start_export_wh"]),
                "end_export_wh": float(row["end_export_wh"]),
                "start_export_vah": float(row["start_export_vah"]),
                "end_export_vah": float(row["end_export_vah"]),
                "net_metering_flag": row["net_metering_flag"],
                "max_demand": float(row["max_demand"]),
                "multiplying_factor": float(row["multiplying_factor"]),
            })
    return data

# Main execution block
if __name__ == "__main__":
    account_id = input("Enter account ID: ")
    
    # Step 1: Fetch and save response data to CSV
    data = fetch_all_daily_data(account_id)
    if data:
        save_response_data_to_csv(account_id, data)

    # Step 2: (Optional) Read the saved data from CSV
    # Uncomment below to read the saved data if needed
    # consumption_data = read_consumption_data_from_csv(account_id)
    # print(consumption_data)

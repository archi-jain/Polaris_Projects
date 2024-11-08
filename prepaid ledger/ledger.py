import requests
from datetime import datetime, timedelta

# Function to fetch daily data from the API
def fetch_daily_data(account_id, start_date, end_date):
    url = f'https://engine-web.test.gomatimvvnl.in/daily_energy_consumption/{account_id}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Ensure this returns a list of daily records
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Function to calculate energy charges based on slabs
def calculate_energy_charges(daily_consumption):
    slabs = [
        (100, 3),  # Lifeline Consumer Load up to 1 kW and for consumption up to 100 kWh/month
        (200, 5.5),  # Upto 100 KWH/Month
        (150, 5.5),  # 101 to 150 KWH/Month
        (150, 6),    # 151 to 300 KWH/Month
        (float('inf'), 6.5)  # Above 300 KWH
    ]
    
    total_charge = 0
    remaining_consumption = daily_consumption
    
    for limit, rate in slabs:
        if remaining_consumption > 0:
            if remaining_consumption <= limit:
                total_charge += remaining_consumption * rate
                break
            else:
                total_charge += limit * rate
                remaining_consumption -= limit

    return total_charge

# Function to prepare ledger entries
def prepare_ledger(account_id, meter_number, start_date, end_date):
    current_date = start_date
    cumm_daily_consumption_mtd = 0
    cumm_daily_consumption_rupees_mtd = 0
    rows = []
    
    while current_date <= end_date:
        data = fetch_daily_data(account_id, current_date, current_date + timedelta(days=1))
        
        if data:
            for daily_data in data:  # Loop through each day's data
                # Extract consumption values from API data
                daily_consumption = float(daily_data['energy_consumption_kwh'])  # Daily import consumption
                daily_consumption_export = float(daily_data['energy_consumption_export_kwh'])  # Daily export consumption
                daily_max_demand = float(daily_data['max_demand'])
                
                # Calculate daily green energy charge (assumed 0.44 per kWh)
                daily_green_energy_charge = daily_consumption * 0.44  

                # Calculate daily energy charges
                daily_energy_charge = calculate_energy_charges(daily_consumption)
                cumm_daily_consumption_mtd += daily_consumption
                cumm_daily_consumption_rupees_mtd += daily_energy_charge

                # Create ledger row for the day
                row = {
                    "id": daily_data["id"],
                    "created_at": daily_data["created_at"],
                    "start_date_time": daily_data["start_daily_datetime"],
                    "end_date_time": daily_data["end_daily_datetime"],
                    "account_id": daily_data["account_id"],
                    "meter_number": daily_data["meter_number"],
                    "daily_consumption": daily_consumption,
                    "daily_consumption_in_rupees": daily_energy_charge,
                    "cumm_daily_consumption_mtd": cumm_daily_consumption_mtd,
                    "cumm_daily_consumption_rupees_mtd": cumm_daily_consumption_rupees_mtd,
                    "daily_consumption_export": daily_consumption_export,
                    "daily_consumption_export_in_rupees": 0.0,  # Update export charges calculation as needed
                    "cumm_daily_consumption_export_mtd": 0.0,  # Update cumulative export consumption as needed
                    "cumm_daily_consumption_export_rupees_mtd": 0.0,
                    "daily_consumption_export_carry_forward": 0.0,  # Export carry forward logic can be added
                    "cumm_daily_consumption_export_carry_forward_mtd": 0.0,
                    "daily_green_energy_consumption_in_rupees": daily_green_energy_charge,
                    "cumm_daily_green_energy_consumption_rupees_mtd": daily_green_energy_charge,
                    "cumm_ec_charges_mtd": cumm_daily_consumption_rupees_mtd,  # Update EC charges MTD
                    "cumm_ec_charges_mtd_conversion": cumm_daily_consumption_rupees_mtd,  # Conversion factor application
                    "daily_fixed_charges": 15.9677,  # Example daily fixed charge
                    "cumm_daily_fixed_charges_mtd": 31.9355,  # Example cumulative fixed charge
                    "daily_max_demand_adjustment": daily_max_demand * 1.0,  # Apply max demand adjustment
                    "remarks": "Prev Day Ledger Data Exists ::: Electricty charge unit consider as KWH ::: "
                }
                
                rows.append(row)
        else:
            print(f"No data for {current_date}")

        current_date += timedelta(days=1)
    
    return rows

# Main execution block
if __name__ == "__main__":
    account_id = input("Enter account ID: ")
    meter_number = input("Enter meter number: ")
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    ledger_rows = prepare_ledger(account_id, meter_number, start_date, end_date)

    # Print the prepared ledger rows (or save to a file as needed)
    for row in ledger_rows:
        print(row)

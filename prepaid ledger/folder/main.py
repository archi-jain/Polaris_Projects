import requests
import csv

# Function to fetch daily consumption from the API
def get_daily_consumption(account_id):
    url = f"https://engine-web.test.gomatimvvnl.in/daily_energy_consumption/{account_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to calculate daily consumption charges based on slabs
def calculate_charges(daily_consumption_kwh):
    if daily_consumption_kwh <= 100 / 30:
        return daily_consumption_kwh * 5.5
    elif daily_consumption_kwh <= 150 / 30:
        return daily_consumption_kwh * 5.5
    elif daily_consumption_kwh <= 300 / 30:
        return daily_consumption_kwh * 6
    else:
        return daily_consumption_kwh * 6.5

# Function to calculate additional components (fixed charges, green energy, ED, rebates, etc.)
def calculate_additional_charges(daily_consumption_kwh):
    green_energy_charge = daily_consumption_kwh * 2.5344 / 100
    fixed_charge = 15.9677  # This is based on example
    ed_charge = daily_consumption_kwh * 5 / 100
    fc_discount = daily_consumption_kwh * 0.02
    ec_rebate = daily_consumption_kwh * 0.01
    return green_energy_charge, fixed_charge, ed_charge, fc_discount, ec_rebate

# Function to save ledger data into CSV
def save_to_csv(account_id, ledger_data):
    filename = f"ledger_data_{account_id}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow([
            'id', 'created_at', 'start_date_time', 'end_date_time', 'account_id', 'meter_number',
            'daily_consumption', 'daily_consumption_in_rupees', 'cumm_daily_consumption_mtd', 'cumm_daily_consumption_rupees_mtd',
            'daily_consumption_export', 'daily_consumption_export_in_rupees', 'cumm_daily_consumption_export_mtd', 'cumm_daily_consumption_export_rupees_mtd',
            'daily_consumption_export_carry_forward', 'cumm_daily_consumption_export_carry_forward_mtd', 'daily_green_energy_consumption_in_rupees', 'cumm_daily_green_energy_consumption_rupees_mtd',
            'cumm_ec_charges_mtd', 'cumm_ec_charges_mtd_conversion', 'daily_fixed_charges', 'cumm_daily_fixed_charges_mtd', 'cumm_daily_fixed_charges_mtd_conversion',
            'daily_ec_discount', 'cumm_daily_ec_discount_mtd', 'daily_fc_discount', 'cumm_daily_fc_discount_mtd', 'daily_ec_rebate', 'cumm_daily_ec_rebate_mtd', 'daily_fc_rebate',
            'cumm_ed_charges_mtd', 'cumm_dmc_mtd', 'daily_recharges', 'cumm_daily_recharges_mtd', 'daily_arrear_charge', 'cumm_daily_arrear_charge_mtd', 'daily_lpsc_charge', 
            'cumm_daily_lpsc_charge_mtd', 'daily_late_payment_surcharge', 'cumm_daily_late_payment_surcharge_mtd', 'daily_credit_debit', 'cumm_daily_credit_debit_mtd',
            'max_demand', 'daily_max_demand_adjustment', 'cumm_daily_max_demand_adjustment_mtd', 'daily_max_demand_penalty', 'cumm_daily_max_demand_penalty_mtd', 
            'actual_cumm_daily_consumption', 'opening_balance', 'closing_balance', 'ledger_reset_flag', 'remarks'
        ])
        # Write the data rows
        for row in ledger_data:
            writer.writerow(row)
    print(f"Ledger data saved to {filename}")

# Main function to process and create the ledger
def process_daily_ledger(account_id):
    data_list = get_daily_consumption(account_id)

    if data_list:
        ledger_data = []
        cummulative_consumption = 0
        cummulative_charges = 0

        for data in data_list:
            daily_consumption_kwh = float(data.get('energy_consumption_kwh', 0))
            daily_consumption_export_kwh = float(data.get('energy_consumption_export_kwh', 0))
            max_demand = float(data.get('max_demand', 0))

            # Calculate daily charges and additional parameters
            daily_charges = calculate_charges(daily_consumption_kwh)
            green_energy_charge, fixed_charge, ed_charge, fc_discount, ec_rebate = calculate_additional_charges(daily_consumption_kwh)

            # Update cumulative values
            cummulative_consumption += daily_consumption_kwh
            cummulative_charges += daily_charges

            ledger_entry = [
                data.get('id'), data.get('created_at'), data.get('start_daily_datetime'), data.get('end_daily_datetime'),
                data.get('account_id'), data.get('meter_number'),
                daily_consumption_kwh, daily_charges, cummulative_consumption, cummulative_charges,
                daily_consumption_export_kwh, daily_consumption_export_kwh * 0,  # Assuming no export charge in rupees
                0, 0,  # Export carry forward
                green_energy_charge, green_energy_charge,  # Daily green energy charges
                cummulative_charges, cummulative_charges,  # EC charges MTD
                fixed_charge, fixed_charge,  # Daily and cumulative fixed charges
                fc_discount, fc_discount, ec_rebate, ec_rebate,  # Discounts and rebates
                ed_charge, 0,  # ED charges
                0, 0, 0,  # Arrear and other charges
                max_demand, 0, 0,  # Max demand and adjustments
                cummulative_consumption, 1603.00,  # Example opening balance
                1603.00 - cummulative_charges,  # Closing balance
                'False', 'Prev Day Ledger Data not exists ::: Electricty charge unit consider as KWH'
            ]

            # Add the ledger entry to the list
            ledger_data.append(ledger_entry)

        # Save data to CSV
        save_to_csv(account_id, ledger_data)
    else:
        print("No data to process.")

# Input account ID
account_id = input("Enter Account ID: ")
process_daily_ledger(account_id)

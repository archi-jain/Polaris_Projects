import requests
import pandas as pd
import json
import re
import random
import string

# Define the API URL and headers
url = "https://gateway.test.gomatimvvnl.in/integration/account_balance_reconciliation/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}

def generate_transaction_id(length=10):
    """Generate a random alphanumeric string of a given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_request(request_data):
    results = []

    # Ensure all fields are treated as strings for validation purposes
    account_no = str(request_data.get('accountNo', '')).strip()
    account_balance = request_data.get('accountBalance', '')
    arrear = request_data.get('arrear', '')
    meter_number = str(request_data.get('meterNumber', '')).strip()
    last_bill_date = str(request_data.get('lastBillDate', '')).strip()
    transaction_id = str(request_data.get('transactionId', '')).strip()
    lpsc = request_data.get('lpsc', '')
    param1 = str(request_data.get('param1', '')).strip()
    param2 = str(request_data.get('param2', '')).strip()

    # Validate accountNo
    if isinstance(account_no, str) and re.match(r'^\d{10}$', account_no):
        results.append('accountNo: PASS')
    else:
        results.append('accountNo: FAIL')

    # Validate accountBalance
    if isinstance(account_balance, (int, float)) and 0 <= float(account_balance) <= 99999999.99:
        results.append('accountBalance: PASS')
    else:
        results.append('accountBalance: FAIL')

    # Validate arrear
    if isinstance(arrear, (int, float)) and 0 <= float(arrear) <= 99999999.99:
        results.append('arrear: PASS')
    else:
        results.append('arrear: FAIL')

    # Validate meterNumber
    if isinstance(meter_number, str) and len(meter_number) <= 16:
        results.append('meterNumber: PASS')
    else:
        results.append('meterNumber: FAIL')

    # Validate lastBillDate
    if isinstance(last_bill_date, str) and re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', last_bill_date):
        results.append('lastBillDate: PASS')
    else:
        results.append('lastBillDate: FAIL')

    # Validate transactionId
    if isinstance(transaction_id, str) and len(transaction_id) <= 20:
        results.append('transactionId: PASS')
    else:
        results.append('transactionId: FAIL')

    # Validate lpsc
    if isinstance(lpsc, (int, float)) and 0 <= float(lpsc) <= 99999999.99:
        results.append('lpsc: PASS')
    else:
        results.append('lpsc: FAIL')

    # Validate param1 and param2
    if isinstance(param1, str) and isinstance(param2, str):
        results.append('param1: PASS')
        results.append('param2: PASS')
    else:
        results.append('param1: FAIL')
        results.append('param2: FAIL')

    return results

def test_api(request_data):
    response = requests.post(url, headers=headers, data=json.dumps(request_data))
    response_json = response.json()
    if response.status_code == 201:
        return 'Success', response_json
    elif response.status_code == 422:
        return 'Validation Error', response_json
    else:
        return 'Other Error', response_json

def main():
    # Read data from CSV
    df = pd.read_csv('Accept_Account_Balance_Recon/data.csv')
    
    for _, row in df.iterrows():
        request_data = row.to_dict()
        
        # Convert numeric fields to appropriate types
        request_data['accountBalance'] = float(request_data.get('accountBalance', 0))
        request_data['arrear'] = float(request_data.get('arrear', 0))
        request_data['lpsc'] = float(request_data.get('lpsc', 0))
        
        # Ensure accountNo is a string
        request_data['accountNo'] = str(request_data.get('accountNo', '')).strip()

        # Generate a unique transaction ID
        request_data['transactionId'] = generate_transaction_id()
        
        # Validate request data
        validation_results = validate_request(request_data)
        for result in validation_results:
            print(result)
        
        # Test the API
        status, response_data = test_api(request_data)
        print(f"API Response Status: {status}")
        print(f"Response Data: {json.dumps(response_data, indent=2)}")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()

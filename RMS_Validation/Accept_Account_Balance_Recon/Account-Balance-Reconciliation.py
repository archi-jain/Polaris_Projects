# url = "https://gateway.test.gomatimvvnl.in/integration/account_balance_reconciliation/"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
#     "Content-Type": "application/json"
# }


import requests
import json
import re

# Define the API URL and headers
url = "https://gateway.test.gomatimvvnl.in/integration/account_balance_reconciliation/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}

# Sample request JSON for testing
request_json = {
    "accountNo": "8888888888",
    "accountBalance": 99999999.99,
    "arrear": 99999999.99,
    "meterNumber": "MTR123456",
    "lastBillDate": "2024-08-28T08:11:08",
    "transactionId": "TXN123456",
    "lpsc": 99999999.99,
    "param1": "value1",
    "param2": "value2"
}

# Define validation functions
def validate_request(request_data):
    results = []
    
    # Validate accountNo
    account_no = request_data.get('accountNo', '')
    if re.match(r'^\d{10}$', account_no):
        results.append('accountNo: PASS')
    else:
        results.append('accountNo: FAIL')
    
    # Validate accountBalance
    account_balance = request_data.get('accountBalance', '')
    if isinstance(account_balance, (int, float)) and 0 <= account_balance <= 99999999.99:
        results.append('accountBalance: PASS')
    else:
        results.append('accountBalance: FAIL')
    
    # Validate arrear
    arrear = request_data.get('arrear', '')
    if isinstance(arrear, (int, float)) and 0 <= arrear <= 99999999.99:
        results.append('arrear: PASS')
    else:
        results.append('arrear: FAIL')
    
    # Validate meterNumber
    meter_number = request_data.get('meterNumber', '')
    if len(meter_number) <= 16:
        results.append('meterNumber: PASS')
    else:
        results.append('meterNumber: FAIL')
    
    # Validate lastBillDate
    last_bill_date = request_data.get('lastBillDate', '')
    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', last_bill_date):
        results.append('lastBillDate: PASS')
    else:
        results.append('lastBillDate: FAIL')
    
    # Validate transactionId
    transaction_id = request_data.get('transactionId', '')
    if len(transaction_id) <= 20:
        results.append('transactionId: PASS')
    else:
        results.append('transactionId: FAIL')
    
    # Validate lpsc
    lpsc = request_data.get('lpsc', '')
    if isinstance(lpsc, (int, float)) and 0 <= lpsc <= 99999999.99:
        results.append('lpsc: PASS')
    else:
        results.append('lpsc: FAIL')
    
    # Validate param1 and param2
    param1 = request_data.get('param1', '')
    param2 = request_data.get('param2', '')
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
    # Validate request data
    validation_results = validate_request(request_json)
    for result in validation_results:
        print(result)
    
    # Test the API
    status, response_data = test_api(request_json)
    print(f"API Response Status: {status}")
    print(f"Response Data: {json.dumps(response_data, indent=2)}")

if __name__ == "__main__":
    main()

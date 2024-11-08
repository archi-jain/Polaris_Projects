import requests
import json
import re

# Define the API URL and headers
url = "https://gateway.test.gomatimvvnl.in/integration/attribute_change/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}

# Sample request JSON for testing
request_json = {
    "requestId": "12345",
    "type": "EMAILCHANGE",
    "effectiveDate": "2024-08-28T00:00:00",
    "accountId": "1234567890",
    "changeValue": "example@example.com",
    "meterNumber": "MTR123456",
    "param1": "value1",
    "param2": "value2",
    "param3": "value3",
    "param4": "value4",
    "param5": "value5"
}

# Define validation functions
def validate_request(request_data):
    results = []
    
    # Validate requestId
    request_id = request_data.get('requestId', '')
    if re.match(r'^[0-9]{1,20}$', request_id):
        results.append('requestId: PASS')
    else:
        results.append('requestId: FAIL')
    
    # Validate type
    req_type = request_data.get('type')
    valid_types = {"LOADCHANGE", "TARIFFCHANGE", "COT", "EMAILCHANGE", "MOBILECHANGE", "WHATSAPPCHANGE", "PLCHANGE", "GREENCHANGE", "SHUNTCAPCHANGE", "POSTPRECHANGE", "EDAPPLICABLE"}
    if req_type in valid_types:
        results.append('type: PASS')
    else:
        results.append('type: FAIL')
    
    # Validate effectiveDate
    effective_date = request_data.get('effectiveDate', '')
    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', effective_date):
        results.append('effectiveDate: PASS')
    else:
        results.append('effectiveDate: FAIL')
    
    # Validate accountId
    account_id = request_data.get('accountId', '')
    if re.match(r'^[0-9]+$', account_id):
        results.append('accountId: PASS')
    else:
        results.append('accountId: FAIL')
    
    # Validate changeValue based on type
    change_value = request_data.get('changeValue', '')
    if req_type == "LOADCHANGE":
        if re.match(r'^\d{1,5}(\.\d)?$', change_value):
            results.append('changeValue for LOADCHANGE: PASS')
        else:
            results.append('changeValue for LOADCHANGE: FAIL')
    elif req_type == "TARIFFCHANGE":
        if len(change_value) <= 4:
            results.append('changeValue for TARIFFCHANGE: PASS')
        else:
            results.append('changeValue for TARIFFCHANGE: FAIL')
    elif req_type == "COT":
        if len(change_value) <= 100:
            results.append('changeValue for COT: PASS')
        else:
            results.append('changeValue for COT: FAIL')
    elif req_type == "EMAILCHANGE":
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', change_value):
            results.append('changeValue for EMAILCHANGE: PASS')
        else:
            results.append('changeValue for EMAILCHANGE: FAIL')
    elif req_type == "MOBILECHANGE":
        if re.match(r'^\d{10}$', change_value):
            results.append('changeValue for MOBILECHANGE: PASS')
        else:
            results.append('changeValue for MOBILECHANGE: FAIL')
    elif req_type == "WHATSAPPCHANGE":
        if re.match(r'^\d{10}$', change_value):
            results.append('changeValue for WHATSAPPCHANGE: PASS')
        else:
            results.append('changeValue for WHATSAPPCHANGE: FAIL')
    elif req_type == "PLCHANGE":
        if change_value.isdigit():
            results.append('changeValue for PLCHANGE: PASS')
        else:
            results.append('changeValue for PLCHANGE: FAIL')
    elif req_type == "GREENCHANGE":
        if change_value in {"Y", "N"}:
            results.append('changeValue for GREENCHANGE: PASS')
        else:
            results.append('changeValue for GREENCHANGE: FAIL')
    elif req_type == "SHUNTCAPCHANGE":
        if change_value in {"Y", "N"}:
            results.append('changeValue for SHUNTCAPCHANGE: PASS')
        else:
            results.append('changeValue for SHUNTCAPCHANGE: FAIL')
    elif req_type == "POSTPRECHANGE":
        if change_value in {"1", "2"}:
            results.append('changeValue for POSTPRECHANGE: PASS')
        else:
            results.append('changeValue for POSTPRECHANGE: FAIL')
    elif req_type == "EDAPPLICABLE":
        if change_value in {"0", "1"}:
            results.append('changeValue for EDAPPLICABLE: PASS')
        else:
            results.append('changeValue for EDAPPLICABLE: FAIL')
    else:
        results.append('Unknown type: FAIL')
    
    # Validate meterNumber
    meter_number = request_data.get('meterNumber', '')
    if len(meter_number) <= 16:
        results.append('meterNumber: PASS')
    else:
        results.append('meterNumber: FAIL')
    
    return results

def test_api(request_data):
    response = requests.post(url, headers=headers, data=json.dumps(request_data))
    if response.status_code == 201:
        return 'Success', response.json()
    elif response.status_code == 422:
        return 'Validation Error', response.json()
    else:
        return 'Other Error', response.json()

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

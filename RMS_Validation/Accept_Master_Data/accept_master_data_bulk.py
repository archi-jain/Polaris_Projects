import requests
import csv
import re
from datetime import datetime
from termcolor import colored

url = "https://gateway.test.gomatimvvnl.in/integration/initial_master_sync/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}


def validate_request_data(data):
    test_results = []

    # Validate requestId
    if not (re.match(r'^[0-9]*$', data['requestId']) and len(data['requestId']) <= 20):
        test_results.append((False, 'Request ID', f"Invalid value: {data['requestId']}"))
    else:
        test_results.append((True, 'Request ID', ""))

    # Validate accountId
    if not (data['accountId'].isdigit() and len(data['accountId']) == 10):
        test_results.append((False, 'Account ID', f"Invalid value: {data['accountId']}"))
    else:
        test_results.append((True, 'Account ID', ""))

    # Validate postcode (only digits, length == 6)
    if not (str(data['postcode']).isdigit() and len(str(data['postcode'])) == 6):
        test_results.append((False, 'Postcode', f"Invalid value: {data['postcode']}"))
    else:
        test_results.append((True, 'Postcode', ""))

    # Validate mobileNumber (only digits and length == 10)
    if not (str(data['mobileNumber']).isdigit() and len(str(data['mobileNumber'])) == 10):
        test_results.append((False, 'Mobile Number', f"Invalid value: {data['mobileNumber']}"))
    else:
        test_results.append((True, 'Mobile Number', ""))

    # Validate email
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        test_results.append((False, 'Email', f"Invalid value: {data['email']}"))
    else:
        test_results.append((True, 'Email', ""))

    # Validate badgeNumber (alphanumeric, <= 30 characters)
    if not (re.match(r'^[a-zA-Z0-9]*$', data['badgeNumber']) and len(data['badgeNumber']) <= 30):
        test_results.append((False, 'Badge Number', f"Invalid value: {data['badgeNumber']}"))
    else:
        test_results.append((True, 'Badge Number', ""))

    # Validate supplyTypecode (alphanumeric without spaces)
    if not re.match(r'^[a-zA-Z0-9]+$', data['supplyTypecode']):
        test_results.append((False, 'Supply Typecode', f"Invalid value: {data['supplyTypecode']}"))
    else:
        test_results.append((True, 'Supply Typecode', ""))

    # Validate meterSrno (alphanumeric, <=16 characters)
    if not (re.match(r'^[a-zA-Z0-9]*$', data['meterSrno']) and len(data['meterSrno']) <= 16):
        test_results.append((False, 'Meter Serial Number', f"Invalid value: {data['meterSrno']}"))
    else:
        test_results.append((True, 'Meter Serial Number', ""))

    # Validate sanctionedLoad (float value)
    try:
        if not isinstance(data['sanctionedLoad'], float):
            raise ValueError
        test_results.append((True, 'Sanctioned Load', ""))
    except ValueError:
        test_results.append((False, 'Sanctioned Load', f"Invalid value: {data['sanctionedLoad']}"))

    # Validate meterInstalldate (format yyyy-MM-ddTHH:mm:ss)
    try:
        datetime.strptime(data['meterInstalldate'], '%Y-%m-%dT%H:%M:%S')
        test_results.append((True, 'Meter Install Date', ""))
    except ValueError:
        test_results.append((False, 'Meter Install Date', f"Invalid value: {data['meterInstalldate']}"))

    # Validate prepaidOpeningbalance (float and value >= 0)
    try:
        if not (isinstance(data['prepaidOpeningbalance'], float) and data['prepaidOpeningbalance'] >= 0):
            raise ValueError
        test_results.append((True, 'Prepaid Opening Balance', ""))
    except ValueError:
        test_results.append((False, 'Prepaid Opening Balance', f"Invalid value: {data['prepaidOpeningbalance']}"))

    return test_results

def test_api_with_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            request_data = {
                "requestId": row['requestId'],
                "accountId": row['accountId'],
                "consumerName": row['consumerName'],
                "address1": row['address1'],
                "address2": row['address2'],
                "address3": row['address3'],
                "postcode": int(row['postcode']),
                "mobileNumber": int(row['mobileNumber']),
                "whatsAppnumber": int(row['whatsAppnumber']),
                "email": row['email'],
                "badgeNumber": row['badgeNumber'],
                "supplyTypecode": row['supplyTypecode'],
                "meterSrno": row['meterSrno'],
                "sanctionedLoad": float(row['sanctionedLoad']),
                "loadUnit": row['loadUnit'],
                "meterInstalldate": row['meterInstalldate'],
                "customerEntrydate": row['customerEntrydate'],
                "connectionStatus": row['connectionStatus'],
                "prepaidPostpaidflag": row['prepaidPostpaidflag'],
                "netMeterflag": row['netMeterflag'],
                "shuntCapacitorflag": row['shuntCapacitorflag'],
                "greenEnergyflag": row['greenEnergyflag'],
                "powerLoomcount": int(row['powerLoomcount']),
                "rateSchedule": row['rateSchedule'],
                "meterType": row['meterType'],
                "meterMake": row['meterMake'],
                "multiplyingFactor": float(row['multiplyingFactor']),
                "meterStatus": row['meterStatus'],
                "arrears": float(row['arrears']),
                "prepaidOpeningbalance": float(row['prepaidOpeningbalance']),
                "divisionCode": row['divisionCode'],
                "subDivCode": row['subDivCode'],
                "dtrCode": row['dtrCode'],
                "feederCode": row['feederCode'],
                "substaionCode": row['substaionCode'],
                "serviceAgreementid": row['serviceAgreementid'],
                "billCycle": row['billCycle'],
                "edApplicable": row['edApplicable'],
                "lpsc": row['lpsc'],
                "param1": row['param1'],
                "param2": row['param2'],
                "param3": row['param3'],
                "param4": row['param4'],
                "param5": row['param5']
            }

            # Validate the request data
            validation_results = validate_request_data(request_data)

            # Print validation results
            print(f"Testing row with accountId: {request_data['accountId']}")
            all_passed = True
            for result in validation_results:
                if result[0]:
                    print(colored(f"PASS: {result[1]} is valid.", 'green'))
                else:
                    all_passed = False
                    print(colored(f"FAIL: {result[1]} is invalid. {result[2]}", 'red'))

            # Make the API call
            response = requests.post(url, headers=headers, json=request_data)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Message: {response.json().get('message', 'No message provided')}")

            # Check response status code
            if response.status_code == 201 and not all(result[0] for result in validation_results):
                print(colored("FAIL: Status code should not be 201 if validation fails.", 'red'))
            else:
                print(colored("PASS: Status code is correct and not 201.", 'green'))

            print("\n")

# Call the function with the path to your CSV file
test_api_with_csv('Accept_Master_Data\Master_data.csv')

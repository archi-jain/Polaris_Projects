import csv
import re
import requests
from datetime import datetime
from termcolor import colored

# Sending a request Payload with Auth token
def send_request(payload):
    url = "https://gateway.test.gomatimvvnl.in/integration/prepaid_recharge_sync/"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

# Function to validate and capture test results
def capture_test_results(test_func: callable, description: str, row_number: int, request_data=None) -> str:
    result = f"Row {row_number} : {description}"
    try:
        if request_data:
            test_func(request_data)
        result = colored(f"PASS : {result}", 'green')
    except AssertionError as e:
        result = colored(f"FAIL : {result}\nReason: {str(e)}", 'red')
    return result


def validate_request_id(data: dict) -> None:
    assert re.match(r'^[0-9]*$', data['requestId']) and len(data['requestId']) <= 20, f"Invalid Request ID: {data['requestId']}"

def validate_account_id(data: dict) -> None:
    assert data['accountId'].isdigit() and len(data['accountId']) == 10, f"Invalid Account ID: {data['accountId']}"

def validate_postcode(data: dict) -> None:
    assert str(data['postcode']).isdigit() and len(str(data['postcode'])) == 6, f"Invalid Postcode: {data['postcode']}"

def validate_mobile_number(data: dict) -> None:
    assert str(data['mobileNumber']).isdigit() and len(str(data['mobileNumber'])) == 10, f"Invalid Mobile Number: {data['mobileNumber']}"

def validate_email(data: dict) -> None:
    assert re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']), f"Invalid Email: {data['email']}"

def validate_badge_number(data: dict) -> None:
    assert re.match(r'^[a-zA-Z0-9]*$', data['badgeNumber']) and len(data['badgeNumber']) <= 30, f"Invalid Badge Number: {data['badgeNumber']}"

def validate_supply_type_code(data: dict) -> None:
    assert re.match(r'^[a-zA-Z0-9]+$', data['supplyTypecode']), f"Invalid Supply Typecode: {data['supplyTypecode']}"

def validate_meter_sr_no(data: dict) -> None:
    assert re.match(r'^[a-zA-Z0-9]*$', data['meterSrno']) and len(data['meterSrno']) <= 16, f"Invalid Meter Serial Number: {data['meterSrno']}"

def validate_sanctioned_load(data: dict) -> None:
    assert isinstance(data['sanctionedLoad'], float), f"Invalid Sanctioned Load: {data['sanctionedLoad']}"

def validate_meter_install_date(data: dict) -> None:
    try:
        datetime.strptime(data['meterInstalldate'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise AssertionError(f"Invalid Meter Install Date: {data['meterInstalldate']}")

def validate_prepaid_opening_balance(data: dict) -> None:
    assert isinstance(data['prepaidOpeningbalance'], float) and data['prepaidOpeningbalance'] >= 0, f"Invalid Prepaid Opening Balance: {data['prepaidOpeningbalance']}"

# Add validation functions for other parameters here...
def validate_consumer_name(data: dict) -> None:
    assert isinstance(data['consumerName'], str) and len(data['consumerName']) > 0, f"Invalid Consumer Name: {data['consumerName']}"

def validate_address(data: dict) -> None:
    assert isinstance(data['address1'], str) and len(data['address1']) > 0, f"Invalid Address1: {data['address1']}"
    assert isinstance(data['address2'], str) and len(data['address2']) > 0, f"Invalid Address2: {data['address2']}"
    assert isinstance(data['address3'], str) and len(data['address3']) > 0, f"Invalid Address3: {data['address3']}"

def validate_whatsapp_number(data: dict) -> None:
    assert str(data['whatsAppnumber']).isdigit() and len(str(data['whatsAppnumber'])) == 10, f"Invalid WhatsApp Number: {data['whatsAppnumber']}"

def validate_connection_status(data: dict) -> None:
    assert data['connectionStatus'] in ['C', 'TD', 'PD'], f"Invalid Connection Status: {data['connectionStatus']}"

def validate_flags(data: dict) -> None:
    flags = ['netMeterflag', 'shuntCapacitorflag', 'greenEnergyflag']
    for flag in flags:
        assert data[flag] in ['Y', 'N'], f"Invalid flag value for {flag}: {data[flag]}"

def validate_prepaidPostpaidflag(data: dict) -> None:
    flags = ['prepaidPostpaidflag']
    for flag in flags:
        assert data[flag] in ['0', '1'], f"Invalid flag value for {flag}: {data[flag]}"

def validate_rate_schedule(data: dict) -> None:
    assert re.match(r'^[A-Z0-9]+$', data['rateSchedule']), f"Invalid Rate Schedule: {data['rateSchedule']}"

def validate_meter_type(data: dict) -> None:
    assert isinstance(data['meterType'], str) and len(data['meterType']) > 0, f"Invalid Meter Type: {data['meterType']}"

def validate_meter_make(data: dict) -> None:
    assert isinstance(data['meterMake'], str) and len(data['meterMake']) > 0, f"Invalid Meter Make: {data['meterMake']}"

def validate_multiplying_factor(data: dict) -> None:
    assert isinstance(data['multiplyingFactor'], float) and data['multiplyingFactor'] > 0, f"Invalid Multiplying Factor: {data['multiplyingFactor']}"

def validate_meter_status(data: dict) -> None:
    assert data['meterStatus'] in ['st', 'A','B'], f"Invalid Meter Status: {data['meterStatus']}"

def validate_arrears(data: dict) -> None:
    assert isinstance(data['arrears'], float), f"Invalid Arrears: {data['arrears']}"

def validate_division_code(data: dict) -> None:
    assert re.match(r'^[A-Z0-9]+$', data['divisionCode']), f"Invalid Division Code: {data['divisionCode']}"

def validate_sub_div_code(data: dict) -> None:
    assert isinstance(data['subDivCode'], str), f"Invalid Sub Division Code: {data['subDivCode']}"

def validate_dtr_code(data: dict) -> None:
    assert isinstance(data['dtrCode'], str), f"Invalid DTR Code: {data['dtrCode']}"

def validate_feeder_code(data: dict) -> None:
    assert isinstance(data['feederCode'], str), f"Invalid Feeder Code: {data['feederCode']}"

def validate_substaionCode(data: dict) -> None:
    assert isinstance(data['substaionCode'], str), f"Invalid Substation Code: {data['substaionCode']}"


def validate_service_agreement_id(data: dict) -> None:
    assert isinstance(data['serviceAgreementid'], str) and len(data['serviceAgreementid']) > 0, f"Invalid Service Agreement ID: {data['serviceAgreementid']}"

def validate_bill_cycle(data: dict) -> None:
    assert isinstance(data['billCycle'], str) and len(data['billCycle']) > 0, f"Invalid Bill Cycle: {data['billCycle']}"

def validate_ed_applicable(data: dict) -> None:
    assert data['edApplicable'] in ['0', '1'], f"Invalid ED Applicable: {data['edApplicable']}"

def validate_lpsc(data: dict) -> None:
    assert isinstance(data['lpsc'], str) and len(data['lpsc']) > 0, f"Invalid LPSC: {data['lpsc']}"

def validate_params(data: dict) -> None:
    for i in range(1, 6):
        param_key = f'param{i}'
        assert isinstance(data.get(param_key, ''), str), f"Invalid {param_key}: {data.get(param_key, '')}"


# Function to validate and send API request
def validate_and_test_api(row_number, request_data):
    # Validate fields
    print(capture_test_results(validate_request_id, "Request ID format", row_number, request_data))
    print(capture_test_results(validate_account_id, "Account ID format", row_number, request_data))
    print(capture_test_results(validate_postcode, "Postcode format", row_number, request_data))
    print(capture_test_results(validate_mobile_number, "Mobile Number format", row_number, request_data))
    print(capture_test_results(validate_whatsapp_number, "WhatsApp Number format", row_number, request_data))
    print(capture_test_results(validate_email, "Email format", row_number, request_data))
    print(capture_test_results(validate_badge_number, "Badge Number format", row_number, request_data))
    print(capture_test_results(validate_supply_type_code, "Supply Typecode format", row_number, request_data))
    print(capture_test_results(validate_meter_sr_no, "Meter Serial Number format", row_number, request_data))
    print(capture_test_results(validate_sanctioned_load, "Sanctioned Load format", row_number, request_data))
    print(capture_test_results(validate_meter_install_date, "Meter Install Date format", row_number, request_data))
    print(capture_test_results(validate_prepaid_opening_balance, "Prepaid Opening Balance format", row_number, request_data))
    print(capture_test_results(validate_consumer_name, "Consumer Name format", row_number, request_data))
    print(capture_test_results(validate_address, "Address format", row_number, request_data))
    print(capture_test_results(validate_connection_status, "Connection Status format", row_number, request_data))
    print(capture_test_results(validate_flags, "Flags format", row_number, request_data))
    print(capture_test_results(validate_prepaidPostpaidflag, "PrepaidPostpaidFlag format", row_number, request_data))
    print(capture_test_results(validate_rate_schedule, "Rate Schedule format", row_number, request_data))
    print(capture_test_results(validate_meter_type, "Meter Type format", row_number, request_data))
    print(capture_test_results(validate_meter_make, "Meter Make format", row_number, request_data))
    print(capture_test_results(validate_multiplying_factor, "Multiplying Factor format", row_number, request_data))
    print(capture_test_results(validate_meter_status, "Meter Status format", row_number, request_data))
    print(capture_test_results(validate_arrears, "Arrears format", row_number, request_data))
    print(capture_test_results(validate_division_code, "Division Code format", row_number, request_data))
    print(capture_test_results(validate_sub_div_code, "Sub Division Code format", row_number, request_data))
    print(capture_test_results(validate_dtr_code, "DTR Code format", row_number, request_data))
    print(capture_test_results(validate_feeder_code, "Feeder Code format", row_number, request_data))
    print(capture_test_results(validate_substaionCode, "Substation Code format", row_number, request_data))
    print(capture_test_results(validate_service_agreement_id, "Service Agreement ID format", row_number, request_data))
    print(capture_test_results(validate_bill_cycle, "Bill Cycle format", row_number, request_data))
    print(capture_test_results(validate_ed_applicable, "ED Applicable format", row_number, request_data))
    print(capture_test_results(validate_lpsc, "LPSC format", row_number, request_data))
    print(capture_test_results(validate_params, "Parameters format", row_number, request_data))
    
    # Send the request and validate the response
    response = send_request(request_data)
    print(capture_test_results(lambda: test_status_code(response), "API Response Status Code", row_number))

# Main function to process test cases
def test_api_with_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row_number, row in enumerate(csv_reader, start=1):
            # Convert values to appropriate types
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

            # Validate and test API
            validate_and_test_api(row_number, request_data)
            print("\n")

# Call the function with the path to your CSV file
test_api_with_csv('Accept_Master_Data/Master_data.csv')

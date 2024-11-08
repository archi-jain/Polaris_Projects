import requests
import re
from termcolor import colored

# API endpoint and headers
url = "https://gateway.test.gomatimvvnl.in/integration/initial_master_sync/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}

# Sample request data
request_data = {
    "requestId": "9601",
    "accountId": "5002093601",
    "consumerName": "Mohan",
    "address1": "string",
    "address2": "string",
    "address3": "string",
    "postcode": 123456,
    "mobileNumber": 7777000601,
    "whatsAppnumber": 7777000601,
    "email": "mohanino@gmail.com",
    "badgeNumber": "POL2025601",
    "supplyTypecode": "10",
    "meterSrno": "4001010601",
    "sanctionedLoad": 1.00,
    "loadUnit": "KW",
    "meterInstalldate": "2024-05-07T05:35:23",
    "customerEntrydate": "2024-05-07",
    "connectionStatus": "C",
    "prepaidPostpaidflag": "1",
    "netMeterflag": "Y",
    "shuntCapacitorflag": "Y",
    "greenEnergyflag": "Y",
    "powerLoomcount": 0,
    "rateSchedule": "RS0007",
    "meterType": "NSM1-PH",
    "meterMake": "POLARIS",
    "multiplyingFactor": 1.22,
    "meterStatus": "C",
    "arrears": 0.00,
    "prepaidOpeningbalance": 2000.00,
    "divisionCode": "DIV324611",
    "subDivCode": "SDO3246118",
    "dtrCode": "D202",
    "feederCode": "F22",
    "substaionCode": "C2",
    "serviceAgreementid": "string",
    "billCycle": "Monthly",
    "edApplicable": "1",
    "lpsc": None,
    "param1": "string",
    "param2": "string",
    "param3": "string",
    "param4": "string",
    "param5": "string"
}

# Validation checks for the request parameters
def validate_request_data(data):
    test_results = []

    # Validation checks
    validations = {
        "requestId": (re.fullmatch(r"^\d{1,20}$", data["requestId"]), "Must be <= 20 digits"),
        "accountId": (re.fullmatch(r"^\d{10}$", data["accountId"]), "Must be exactly 10 digits"),
        "postcode": (re.fullmatch(r"^\d{6}$", str(data["postcode"])), "Must be exactly 6 digits"),
        "mobileNumber": (re.fullmatch(r"^\d{10}$", str(data["mobileNumber"])), "Must be exactly 10 digits"),
        "whatsAppnumber": (re.fullmatch(r"^\d{10}$", str(data["whatsAppnumber"])), "Must be exactly 10 digits"),
        "email": (re.fullmatch(r"[^@]+@[^@]+\.[^@]+", data["email"]), "Must be a valid email address"),
        "badgeNumber": (re.fullmatch(r"^[a-zA-Z0-9]{1,30}$", data["badgeNumber"]), "Must be alphanumeric, <= 30 characters"),
        "supplyTypecode": (re.fullmatch(r"^\w+$", data["supplyTypecode"]), "Must be alphanumeric without spaces"),
        "meterSrno": (re.fullmatch(r"^[a-zA-Z0-9]{1,16}$", data["meterSrno"]), "Must be alphanumeric, <= 16 characters"),
        "sanctionedLoad": (isinstance(data["sanctionedLoad"], float), "Must be a float value"),
        "loadUnit": (data["loadUnit"] in {"KW", "KVAH", "BHP"}, "Must be one of {KW, KVAH, BHP}"),
        "meterInstalldate": (re.fullmatch(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", data["meterInstalldate"]), "Must match format yyyy-mm-ddTHH:MM:SS"),
        "customerEntrydate": (re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", data["customerEntrydate"]), "Must match format yyyy-mm-dd"),
        "connectionStatus": (data["connectionStatus"] in {"C", "TD", "PD"} and len(data["connectionStatus"]) <= 2, "Must be <= 2 characters, one of {C, TD, PD}"),
        "prepaidPostpaidflag": (data["prepaidPostpaidflag"] in {"1", "2"}, "Must be one of {1, 2}"),
        "netMeterflag": (data["netMeterflag"] in {"Y", "N", "B"}, "Must be one of {Y, N, B}"),
        "shuntCapacitorflag": (data["shuntCapacitorflag"] in {"Y", "N"}, "Must be one of {Y, N}"),
        "multiplyingFactor": (isinstance(data["multiplyingFactor"], float), "Must be a float value"),
        "prepaidOpeningbalance": (isinstance(data["prepaidOpeningbalance"], float) and data["prepaidOpeningbalance"] >= 0, "Must be a float >= 0"),
        "edApplicable": (data["edApplicable"] in {"0", "1"}, "Must be either 0 or 1")
    }

    for field, (condition, reason) in validations.items():
        if condition:
            test_results.append((field, True, ""))
        else:
            test_results.append((field, False, reason))

    return test_results

# Function to test the API
def test_api(request_data):
    # Validate the request data before sending the request
    validation_errors = validate_request_data(request_data)
    
    # Print test case results for each parameter
    for field, passed, reason in validation_errors:
        if passed:
            print(colored(f"Test Case PASSED for {field}", "green"))
        else:
            print(colored(f"Test Case FAILED for {field}: {reason}", "red"))
    
    # Only proceed if all validations pass
    if all(passed for _, passed, _ in validation_errors):
        # Send POST request to the API
        response = requests.post(url, headers=headers, json=request_data)
        
        # Expected and actual status codes
        expected_status_code = 200  # Assuming successful validation
        actual_status_code = response.status_code
        
        # Print pass or fail for the test case
        if actual_status_code == expected_status_code:
            print(colored("API Test Case PASSED", "green"))
        else:
            print(colored("API Test Case FAILED", "red"))
            print(f"Expected Status Code: {expected_status_code}, Got: {actual_status_code}")
            print(f"Response: {response.json()}")
        
        # Return the response for further validation if needed
        return response.json()
    else:
        print(colored("Skipping API request due to failed validation.", "red"))
        return None

# Function to print all test cases (pass/fail)
def print_test_results():
    print("Testing API with given request data...")
    response_data = test_api(request_data)
    
    if response_data:
        # Print detailed response
        print("Response Data:")
        for key, value in response_data.items():
            print(f"{key}: {value}")

# Run the test
print_test_results()

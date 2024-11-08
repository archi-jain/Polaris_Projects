import json
import re
import requests
import random
import csv
import string
import time


# Function to generate a random transactionId
def generate_random_transaction_id(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Function to read payload data from a CSV file
def read_request_payloads_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        payloads = []
        for row in reader:
            payloads.append(row)
    return payloads


# Sending a request Payload with Auth token
def send_request(payload):
    url = "https://gateway.test.gomatimvvnl.in/integration/prepaid_recharge_sync/"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def run_test(test_func, description, row_number):
    try:
        test_func()
        print(f"PASS : Row {row_number} : {description}")
    except AssertionError as e:
        print(f"FAIL : Row {row_number} : {description}\nReason: {str(e)}")
        # Optionally print the response details for debugging
        if response.status_code != 201:
            print(f"Response Status Code: {response.status_code}")


def test_status_code():
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response body: {response.text}"


def test_response_is_json():
    assert response.headers["Content-Type"] == "application/json", f"Expected content type to be 'application/json', but got '{response.headers['Content-Type']}'"
    assert response_json is not None, "Response JSON is None"


def test_request_payload_is_json():
    try:
        json.dumps(request_payload)  # Attempt to serialize request_payload to JSON
    except (TypeError, ValueError) as e:
        raise AssertionError(f"Request payload is not in valid JSON format. Reason: {str(e)}")


def test_account_no_format_and_type():
    assert "accountNo" in request_payload, "'accountNo' key not found in request payload"
    assert isinstance(request_payload["accountNo"], str), f"'accountNo' should be of type 'string', but got {type(request_payload['accountNo'])}"
    assert len(request_payload["accountNo"]) == 10, f"'accountNo' should be 10 characters long, but got {len(request_payload['accountNo'])}"
    assert re.match(r"^\d+$", request_payload["accountNo"]), "'accountNo' should only contain digits"


def test_amount_format_and_type():
    assert "amount" in request_payload, "'amount' key not found in request payload"
    assert isinstance(request_payload["amount"], float), f"'amount' should be of type 'float', but got {type(request_payload['amount'])}"


def test_meter_number_format_and_type():
    assert "meterNumber" in request_payload, "'meterNumber' key not found in request payload"
    assert isinstance(request_payload["meterNumber"], str), f"'meterNumber' should be of type 'string', but got {type(request_payload['meterNumber'])}"
    assert len(request_payload["meterNumber"]) <= 16, f"'meterNumber' should be at most 16 characters long, but got {len(request_payload['meterNumber'])}"
    assert re.match(r"^[a-zA-Z0-9]+$", request_payload["meterNumber"]), "'meterNumber' should only contain alphanumeric characters (letters and numbers)"


def test_payment_date_format_and_type():
    assert "paymentDate" in request_payload, "'paymentDate' key not found in request payload"
    assert isinstance(request_payload["paymentDate"], str), f"'paymentDate' should be of type 'string', but got {type(request_payload['paymentDate'])}"
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", request_payload["paymentDate"]), "'paymentDate' format should be 'YYYY-MM-DDTHH:MM:SS'"


def test_source_of_recharge_format_and_type():
    assert "sourceOfRecharge" in request_payload, "'sourceOfRecharge' key not found in request payload"
    assert isinstance(request_payload["sourceOfRecharge"], str), f"'sourceOfRecharge' should be of type 'string', but got {type(request_payload['sourceOfRecharge'])}"
    assert request_payload["sourceOfRecharge"] in ["ONLINE", "OFFLINE"], f"'sourceOfRecharge' should be 'ONLINE' or 'OFFLINE', but got {request_payload['sourceOfRecharge']}"


def test_transaction_id_format_and_type():
    assert "transactionId" in request_payload, "'transactionId' key not found in request payload"
    assert isinstance(request_payload["transactionId"], str), f"'transactionId' should be of type 'string', but got {type(request_payload['transactionId'])}"
    assert 1 <= len(request_payload["transactionId"]) <= 12, f"'transactionId' should be between 1 and 12 characters long, but got {len(request_payload['transactionId'])}"
    assert re.match(r"^[a-zA-Z0-9]+$", request_payload["transactionId"]), "'transactionId' should only contain alphanumeric characters"


def test_param1_format_and_type():
    assert "param1" in request_payload, "'param1' key not found in request payload"
    assert isinstance(request_payload["param1"], str), f"'param1' should be of type 'string', but got {type(request_payload['param1'])}"


def test_param2_format_and_type():
    assert "param2" in request_payload, "'param2' key not found in request payload"
    assert isinstance(request_payload["param2"], str), f"'param2' should be of type 'string', but got {type(request_payload['param2'])}"


def test_response_message_and_status_code():
    assert "message" in response_json, f"'message' key not found in response JSON. Response body: {response_json}"
    assert isinstance(response_json["message"], list), f"'message' should be of type 'list', but got {type(response_json['message'])}"
    assert any("Prepaid Recharge Sync successful for Account ID :" in msg['message'] for msg in response_json["message"]), "'message' does not contain the expected text"

    assert "status_code" in response_json, f"'status_code' key not found in response JSON. Response body: {response_json}"
    assert isinstance(response_json["status_code"], int), f"'status_code' should be of type 'int', but got {type(response_json['status_code'])}"
    assert response_json["status_code"] == 201, f"Expected status code 201, but got {response_json['status_code']}"


# Main function to iterate over each row in the CSV
if __name__ == "__main__":
    payloads = read_request_payloads_from_csv('Data.csv')

    for row_number, payload in enumerate(payloads, start=1):
        request_payload = payload
        request_payload["transactionId"] = generate_random_transaction_id()
        
        # Convert amount to float as expected by the API
        request_payload["amount"] = float(request_payload["amount"])
        
        response = send_request(request_payload)
        response_json = response.json()
        
        run_test(test_status_code, "Status code is 201", row_number)
        run_test(test_response_is_json, "Response is in JSON format", row_number)
        run_test(test_request_payload_is_json, "Request payload is in JSON format", row_number)
        run_test(test_account_no_format_and_type, "Validate accountNo format and type", row_number)
        run_test(test_amount_format_and_type, "Validate amount format and type", row_number)
        run_test(test_meter_number_format_and_type, "Validate meterNumber format and type", row_number)
        run_test(test_payment_date_format_and_type, "Validate paymentDate format and type", row_number)
        run_test(test_source_of_recharge_format_and_type, "Validate sourceOfRecharge format and type", row_number)
        run_test(test_transaction_id_format_and_type, "Validate transactionId format and type", row_number)
        run_test(test_param1_format_and_type, "Validate param1 format and type", row_number)
        run_test(test_param2_format_and_type, "Validate param2 format and type", row_number)
        run_test(test_response_message_and_status_code, "Validate response message and status_code", row_number)
        
        time.sleep(1)
        # Add two spaces after each row iteration
        print("\n")

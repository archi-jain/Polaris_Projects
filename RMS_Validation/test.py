import requests
import json

# API endpoint and credentials
url = "https://gateway.test.gomatimvvnl.in/integration/prepaid_recharge_sync/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InZhbGlkYXRpb24tcG9sYXJpcy1hcmNoaSJ9.hvLPQPjrdhWOd2IMnYe57HbI4C7qkY-K-IQov9cTlSY",
    "Content-Type": "application/json"
}

# Sample request payload
payload = {
    "accountNo": "1234567890",
    "amount": "500",
    "meterNumber": "4001010949",
    "paymentDate": "2024-08-27T12:00:00",
    "sourceOfRecharge": "ONLINE",
    "transactionId": "ABC123456789",
    "param1": "SomeValue",
    "param2": "AnotherValue"
}

# Sending the POST request
response = requests.post(url, headers=headers, json=payload)

# Checking and printing the response
if response.status_code == 201:
    print("Success! Response data:", response.json())
else:
    print(f"Request failed with status code {response.status_code}. Response data:", response.text)

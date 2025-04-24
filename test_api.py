import requests  # Import the 'requests' library to make HTTP requests

# This is the local address where your Flask app runs
url = "http://127.0.0.1:5000/classify"  # URL of the Flask API endpoint for email classification

# Test email content to classify
payload = {
    "email": """  # Sample email to test the classification and PII masking
    Dear Team,

This is Sneha Reddy. You can reach me at sneha.reddy22@gmail.com or +91-9876501234.
My birthdate is 05/09/1993. My Aadhaar number is 4567-8901-2345.
I noticed a fraudulent charge on my credit card 1234-5678-9012-3456 (CVV: 789, Expiry: 08/2026).

Please look into this urgently.

Regards,  
Sneha
"""
}

# Make POST request
response = requests.post(url, json=payload)  # Sending a POST request to the Flask API with the payload

# Print response status and content
print("✅ Status Code:", response.status_code)  # Print the status code of the response to check if the request was successful
try:
    print("🔽 Response JSON:")  # Print the JSON response from the API
    print(response.json())  # Parse and print the JSON content of the response
except Exception as e:
    print("⚠️ Could not decode JSON:", str(e))  # In case JSON decoding fails, print the error message
    print("🔽 Raw Response Text:")  # Print the raw response text if JSON parsing fails
    print(response.text)  # Print the raw response text from the server

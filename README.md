# Email-Classifier
Email Classification and PII Masking Application using Flask, Gradio, and Machine Learning

Overview

This project implements an Email Classification and PII Masking system that allows users to classify support emails and mask personal identifiable information (PII) like names, email addresses, phone numbers, Aadhaar numbers, credit card details, etc. The solution uses machine learning for classification and custom regex-based masking for PII entities.

The application is built using:

Flask for API development.

Gradio for creating the user interface.

Scikit-learn for building the classification model.

Regex for identifying and masking PII data.

What’s Included

app.py: The main entry point for the application. It sets up the Gradio interface for email classification and PII masking, enabling users to interact with the model.

requirements.txt: A list of required Python libraries needed to run the application, including flask, gradio, scikit-learn, and more.

models.py: Contains the code for training the machine learning model using labeled email data and saving the model for future use.

utils.py: A utility script responsible for masking PII from emails using regex patterns. It includes definitions for identifying emails, credit cards, phone numbers, and more.

api.py: Contains the Flask API setup for receiving requests, processing emails, and returning classified emails with masked PII.

test_api.py: A script used for testing the Flask API to ensure it’s working as expected. It sends test emails and checks the returned output.

README.md: This file, which explains the project, the folder structure, and how to use the application.

How to Use
Clone the Repository

Clone the repository to your local machine using the following command: git clone <your-repository-link>

Install Dependencies

Navigate to the project folder and install the required dependencies by running: pip install -r requirements.txt

This command installs all the necessary libraries, including Flask, Gradio, Scikit-learn, and others required for the project.

Run the Application

To start the Flask API, use the command: python api.py

This will start a local server accessible at http://127.0.0.1:5000. The API will be ready to receive requests.

If you prefer using the Gradio interface (for a simpler web-based UI), run: python app.py

This will launch the Gradio interface at http://127.0.0.1:7860. You can paste an email into the interface to classify and mask the PII.

Send a Test Email

To test the API, run the test_api.py script: python test_api.py

This will send a test email to the API and print the JSON response, including the classified email and masked PII entities.

Expected Output

The output from the API or Gradio interface will look something like this:

json
Copy
{
    "input_email_body": "Dear Team,\n\nThis is Sneha Reddy. You can reach me at sneha.reddy22@gmail.com or +91-9876501234.\nMy birthdate is 05/09/1993. My Aadhaar number is 4567-8901-2345.\nI noticed a fraudulent charge on my credit card 1234-5678-9123-4567 (CVV: 789, Expiry: 08/2026).\nPlease look into this urgently.\n\nRegards,\nSneha",
    "list_of_masked_entities": [
        {"position": [209, 228], "classification": "credit_debit_no", "entity": "1234-5678-9123-4567"},
        {"position": [145, 159], "classification": "aadhar_num", "entity": "4567-8901-2345"},
        {"position": [53, 76], "classification": "email", "entity": "sneha.reddy22@gmail.com"},
        {"position": [81, 94], "classification": "phone_number", "entity": "91-9876501234"},
        {"position": [112, 122], "classification": "dob", "entity": "05/09/1993"},
        {"position": [235, 238], "classification": "dob", "entity": "789"},
        {"position": [248, 255], "classification": "dob", "entity": "08/2026"},
        {"position": [0, 9], "classification": "full_name", "entity": "Dear Team"},
        {"position": [20, 31], "classification": "full_name", "entity": "Sneha Reddy"},
        {"position": [124, 134], "classification": "full_name", "entity": "My Aadhaar"}
    ],
    "masked_email": "[full_name],\n\nThis i[full_name]dy. You can reach me at [email]                 or +[phone_number].\nMy birthdate is[dob]     [full_name]haar number is [aadhar_num]  .\nI noticed a fraudulent charge on my credit card [credit_debit_no]   (CVV:[dob]9, Expir[dob]  026).\n\nPlease look into this urgently.\n\nRegards,  \nSneha",
    "category_of_the_email": "Incident"
}

Challenges Faced

Regex for Masking PII: Ensuring accurate detection and masking of PII, especially distinguishing between similar entities like "CVV" and "expiry date".

Full Name Classification: Avoiding false positives where phrases like "Dear Support" or "My Aadhaar" were mistakenly identified as full names.

Model Accuracy: Achieving satisfactory classification accuracy, ensuring that the model's predictions are both relevant and meaningful to the user.

Handling Large Texts: Properly handling and classifying long and complex email bodies while ensuring no data loss during the masking process.

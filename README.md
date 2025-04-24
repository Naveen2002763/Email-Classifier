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

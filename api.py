from flask import Flask, request, Response  # Importing necessary modules from Flask
from collections import OrderedDict  # Import OrderedDict to maintain the order of the dictionary
import json  # Import JSON to handle data in JSON format
import pickle  # Import pickle to load pre-trained models
from utils import mask_email  # Import the email masking function from utils.py

# Load trained model and label encoder
with open("email_classifier.pkl", "rb") as f:  # Load the trained model for email classification
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:  # Load the label encoder to decode predicted labels
    label_encoder = pickle.load(f)

app = Flask(__name__)  # Initialize the Flask app

@app.route("/classify", methods=["POST"])  # Define the POST route for email classification
def classify_email():
    data = request.get_json()  # Get the incoming JSON data from the request
    email_text = data.get("email", "").strip()  # Extract the email text from the incoming data

    if not email_text:  # If the email body is empty
        return Response(json.dumps({"error": "Email content is required."}), status=400, mimetype='application/json')  # Return error response if no email content is provided

    # Apply masking
    masked_text, entities = mask_email(email_text)  # Mask the PII in the email text

    # Vectorize and predict
    vectorized_input = model.named_steps['tfidf'].transform([masked_text])  # Vectorize the masked email text
    pred_index = model.named_steps['classifier'].predict(vectorized_input)[0]  # Get the predicted label index
    pred_label = label_encoder.inverse_transform([pred_index])[0]  # Decode the predicted label

    # Prepare strict format output with OrderedDict
    result = OrderedDict()  # Initialize an ordered dictionary to maintain the order
    result["input_email_body"] = email_text  # Store the original email body
    result["list_of_masked_entities"] = [  # Store the list of masked entities (PII data)
        {
            "position": e["position"],  # Position of the entity in the original text
            "classification": e["classification"],  # Classification of the entity (e.g., email, phone number)
            "entity": e["entity"]  # The original value of the entity
        } for e in entities
    ]
    result["masked_email"] = masked_text  # Store the masked email text
    result["category_of_the_email"] = pred_label  # Store the predicted category (type) of the email

    # Return the response as JSON
    return Response(json.dumps(result, ensure_ascii=False), status=200, mimetype='application/json')

if __name__ == "__main__":  # Run the Flask app when this file is executed directly
    app.run(debug=True)  # Start the Flask app in debug mode

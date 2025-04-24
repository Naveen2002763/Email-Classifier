import gradio as gr  # Import Gradio for building the interface
import pickle  # Import pickle to load the saved model and label encoder
from utils import mask_email  # Import the mask_email function from the utils module to mask PII

# Load saved model and label encoder
with open("email_classifier.pkl", "rb") as f:  # Open the saved model file
    model = pickle.load(f)  # Load the model into the 'model' variable

with open("label_encoder.pkl", "rb") as f:  # Open the saved label encoder file
    label_encoder = pickle.load(f)  # Load the label encoder into the 'label_encoder' variable

# Define prediction function
def classify_email(email_text):  # Function to classify the email and mask PII
    if not email_text.strip():  # Check if the email content is empty
        return {  # If email is empty, return an error response
            "input_email_body": "",
            "list_of_masked_entities": [],
            "masked_email": "",
            "category_of_the_email": "Invalid input"  # Set category as "Invalid input" if empty
        }

    # Mask PII
    masked_email, entities = mask_email(email_text)  # Call the mask_email function to mask the PII in the email

    # Predict category
    vectorized = model.named_steps['tfidf'].transform([masked_email])  # Transform the masked email using the TF-IDF vectorizer
    predicted_index = model.named_steps['classifier'].predict(vectorized)[0]  # Predict the email category index
    predicted_category = label_encoder.inverse_transform([predicted_index])[0]  # Decode the predicted index into category name

    # Format output
    return {  # Return the formatted output as a dictionary
        "input_email_body": email_text,  # Return the original email body
        "list_of_masked_entities": [  # List of masked entities in the email
            {
                "position": e["position"],  # Position of the masked entity
                "classification": e["classification"],  # Classification of the entity (email, phone, etc.)
                "entity": e["entity"]  # The original value of the entity
            } for e in entities  # Loop through each entity found by mask_email
        ],
        "masked_email": masked_email,  # Return the masked email text
        "category_of_the_email": predicted_category  # Return the predicted category of the email
    }

# Gradio interface
iface = gr.Interface(  # Create a Gradio interface
    fn=classify_email,  # The function to be called when the user inputs data
    inputs=gr.Textbox(lines=10, label="Paste your email here"),  # Input: textbox for the user to paste the email content
    outputs="json",  # Output: JSON format with the classification and masked entities
    title="Email Classification & PII Masking",  # Title of the app
    description="This tool classifies support emails and masks sensitive PII from the content."  # Description of the app
)

# Launch app
if __name__ == "__main__":  # Check if the script is run directly
    iface.launch()  # Launch the Gradio interface to interact with the app

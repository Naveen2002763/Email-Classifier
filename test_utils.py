from utils import mask_email

# Sample email text for testing
email_text = "Hi, I am Rahul Mehta. My phone is 9876543210 and my email is rahul@example.com. My card number is 1234-5678-9123-4567."

# Call the masking function
masked_email, entities = mask_email(email_text)

# Print the results
print("Original Email:\n", email_text)  # Prints the original email text
print("\nMasked Email:\n", masked_email)  # Prints the masked email text with PII removed

print("\nMasked Entities:")  # Prints details of the entities that were masked
for e in entities:
    print(e)  # Prints each masked entity's position, classification, and original value

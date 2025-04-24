import re

def mask_email(text):
    entities = []

    # Phrases to exclude from being misclassified as full names
    greetings_exclude = {
        "dear support", "hi support", "hello support",
        "dear team", "hi team", "hello team",
        "regards", "thanks", "sincerely", "cheers"
    }

    # Patterns ordered: more specific first
    patterns = {
        "credit_debit_no": r"\b(?:\d{4}[- ]?){3}\d{4}\b",  # Matches card numbers
        "aadhar_num": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",   # Matches Aadhaar numbers
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Matches emails
        "phone_number": r"\+91[-\s]?\d{10}|\b\d{10}\b",  # Matches phone numbers
        "dob": r"\b(?:0?[1-9]|[12][0-9]|3[01])[-/](?:0?[1-9]|1[0-2])[-/](?:19|20)\d{2}\b",  # Matches DOB
        "cvv_no": r"\bCVV[:\s]*\d{3}\b",  # Matches CVV numbers with label
        "expiry_no": r"\bExpiry[:\s]*(0[1-9]|1[0-2])/(?:\d{2}|\d{4})\b",  # Matches expiry date with label
        "full_name": r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"  # Matches full names
    }

    masked = list(text)
    occupied = [False] * len(text)

    # Loop over each regex pattern and apply it to the text
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            value = match.group()  # Extract the matched value
            start = match.start()  # Start position of the match
            end = match.end()      # End position of the match

            # Skip if this portion of the text has already been masked
            if any(occupied[start:end]):
                continue

            # Special rules for the "full_name" entity to prevent misclassification
            if label == "full_name":
                # Skip known greetings
                if value.lower() in greetings_exclude:
                    continue
                # Skip single-word names (likely false positives)
                if len(value.split()) < 2:
                    continue
                # Skip terms like "My Aadhaar", which should not be classified as full name
                if any(word.lower() in value.lower() for word in ["my", "your", "our"]):
                    continue

            # Replace the matched text with the appropriate label
            replacement = f"[{label}]"
            masked[start:end] = list(replacement.ljust(end - start))

            # Mark the masked portion of the text
            for i in range(start, end):
                occupied[i] = True

            # Store the details of the masked entity
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": value
            })

    # Join the masked text into a single string and return it along with the entities
    masked_text = "".join(masked)
    return masked_text, entities

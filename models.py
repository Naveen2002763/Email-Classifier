import pandas as pd  # Importing pandas for data manipulation and handling
import pickle  # Importing pickle for saving and loading the model
from sklearn.feature_extraction.text import TfidfVectorizer  # Importing TF-IDF Vectorizer for text feature extraction
from sklearn.svm import LinearSVC  # Importing Linear Support Vector Classification (SVC) model
from sklearn.preprocessing import LabelEncoder  # Importing LabelEncoder to encode target labels
from sklearn.pipeline import Pipeline  # Importing Pipeline for combining all steps in the workflow
from sklearn.model_selection import train_test_split  # Importing train-test split for splitting dataset
from sklearn.metrics import classification_report, accuracy_score, f1_score  # Importing metrics for evaluation
from utils import mask_email  # Importing mask_email function from utils.py for PII masking

# Load data
df = pd.read_csv("data/combined_emails_with_natural_pii.csv")  # Reading the dataset from a CSV file
df.dropna(subset=['email', 'type'], inplace=True)  # Dropping rows where 'email' or 'type' columns have missing values

# Apply masking
masked_emails = []  # List to store masked emails
for text in df['email']:  # Iterating through each email text
    masked_text, _ = mask_email(text)  # Masking PII using the mask_email function
    masked_emails.append(masked_text)  # Appending masked email to the list
df['masked_email'] = masked_emails  # Adding a new column to the dataframe with masked emails

# Encode labels
label_encoder = LabelEncoder()  # Initialize LabelEncoder for encoding labels
y = label_encoder.fit_transform(df['type'])  # Encode the target labels (email type)

# Save encoder
with open("label_encoder.pkl", "wb") as f:  # Save the label encoder to a file for future use
    pickle.dump(label_encoder, f)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df['masked_email'], y, test_size=0.2, stratify=y, random_state=42
)  # Splitting the data into training and testing sets (80-20 split)

# Optimized SVM pipeline
pipeline = Pipeline([  # Creating a pipeline for text processing and model training
    ('tfidf', TfidfVectorizer(  # Step 1: TF-IDF Vectorizer for feature extraction
        ngram_range=(1, 3),  # Using unigrams, bigrams, and trigrams
        min_df=2,  # Minimum document frequency of 2 for a token to be included
        sublinear_tf=True  # Apply logarithmic scaling to term frequency
    )),
    ('classifier', LinearSVC(  # Step 2: Linear Support Vector Classification model
        C=2.0,  # Regularization strength parameter
        class_weight='balanced',  # Handling class imbalance by assigning weights to each class
        dual=False,  # Faster optimization when the number of samples is greater than the number of features
        max_iter=20000  # Setting a high iteration limit for model convergence
    ))
])

# Train model
pipeline.fit(X_train, y_train)  # Fitting the pipeline on the training data

# Evaluate
y_pred = pipeline.predict(X_test)  # Predicting labels for the test set
acc = accuracy_score(y_test, y_pred)  # Calculating accuracy score
f1 = f1_score(y_test, y_pred, average='weighted')  # Calculating weighted F1-Score

# Print evaluation results
print(f"✅ Final Accuracy: {acc:.4f}")  # Displaying the accuracy score
print(f"📌 Final Weighted F1-Score: {f1:.4f}")  # Displaying the weighted F1-Score
print("\n📊 Final Classification Report:\n")  # Displaying the classification report
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))  # Printing detailed classification metrics

# Save model
with open("email_classifier.pkl", "wb") as f:  # Saving the trained model to a file for future use
    pickle.dump(pipeline, f)

print("\n✅ Final model saved as 'email_classifier.pkl'")  # Confirmation of model saving

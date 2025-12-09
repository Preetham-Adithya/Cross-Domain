import spacy
import pandas as pd
import csv
import os

# --- STEP 1: Example dataset ---
texts = [
    "J.K. Rowling wrote the Harry Potter series.",
    "Microsoft launched Windows 95 in 1995.",
    "Isaac Newton formulated the laws of motion.",
    "Facebook was created by Mark Zuckerberg in 2004."
]

# Save text data to CSV
df_text = pd.DataFrame({'text': texts})
dataset_file = "dataset.csv"
df_text.to_csv(dataset_file, index=False, encoding="utf-8")
print(f"Text data saved to {os.path.abspath(dataset_file)}")

# --- STEP 2: Load spaCy NLP model ---
# Ensure you have run: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


# --- STEP 3: Function to extract triples ---
def extract_relations(doc):
    """
    Extracts a simple Subject-Predicate-Object triple from a spaCy Doc.
    This is a basic heuristic focused on the sentence root (verb).
    """
    for token in doc:
        # Check if the token is the ROOT of the sentence (often the main verb)
        if token.dep_ == 'ROOT':

            subject = ""
            obj = ""
            predicate = token.text  # The root verb

            # Search children of the root token for the Subject and Object
            for child in token.children:

                # Find the nominal subject (nsubj)
                if child.dep_ == 'nsubj' or child.dep_ == 'nsubjpass':
                    # Get the entire subject subtree/phrase
                    subject = ' '.join([t.text for t in child.subtree])

                    # Find the direct object (dobj) or open clausal complement (xcomp)
                if child.dep_ in ('dobj', 'attr', 'oprd'):
                    # Get the entire object subtree/phrase
                    obj = ' '.join([t.text for t in child.subtree])

            # If both subject and object were found, return the triple
            if subject and obj:
                return (subject, predicate, obj)

    return None  # Return None if no simple SPO relation is found


# --- STEP 4: Process each sentence and populate the triples list ---
triples = []

# Loop through each text in the DataFrame
for index, row in df_text.iterrows():
    text = row['text']

    # Process the text with the spaCy model
    doc = nlp(text)

    # Extract the relation (This is the crucial step to get the function's return value)
    relation = extract_relations(doc)

    # If a relation was found, append it as a dictionary to the list
    if relation:
        triples.append({
            'Subject': relation[0],
            'Predicate': relation[1],
            'Object': relation[2]
        })

# Convert the list of dictionaries into a DataFrame for easy saving and printing
df_triples = pd.DataFrame(triples)

# --- STEP 5: Save triples to CSV and Print Output ---
triples_file = "triples.csv"

# Print the extracted triples to the console (Terminal Output)
# This will display the output you were looking for!
print("\n--- Extracted Triples ---")
print(df_triples)
print("-------------------------")

# Save the extracted triples to the CSV file
# Using pandas to_csv, which is simpler than the built-in csv module seen previously
df_triples.to_csv(triples_file, index=False, encoding='utf-8')

# Final confirmation print statement
print(f"\nExtracted {len(triples)} triples and saved to {os.path.abspath(triples_file)}")
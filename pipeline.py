import spacy
import pandas as pd
import csv
import os

#input text -> CSV

texts = [
    "Elon Musk founded SpaceX.",
    "Apple released the iPhone in 2007.",
    "Barack Obama was born in Hawaii.",
    "Tesla produces electric cars."
]

text_csv_file = "dataset.csv"
df_text = pd.DataFrame(texts, columns=["text"])
df_text.to_csv(text_csv_file, index=False, encoding="utf-8")
print(f"Text data saved to {os.path.abspath(text_csv_file)}")

nlp = spacy.load("en_core_web_sm")
df = pd.read_csv(text_csv_file)

triples = []

#extract triples
def extract_relations(doc):
    for sent in doc.sents:
        subject = ""
        obj = ""
        verb = ""
        for token in sent:
            if "subj" in token.dep_:
                subject = token.text
                verb = token.head.text
                for child in token.head.children:
                    if "obj" in child.dep_:
                        obj = child.text
                if subject and verb and obj:
                    triples.append((subject, verb, obj))

#process each sentence
for text in df['text']:
    doc = nlp(str(text))
    extract_relations(doc)

#save triple to CSV

triples_csv_file = "triples.csv"
with open(triples_csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Subject", "Relation", "Object"])
    writer.writerows(triples)

print(f"Extracted {len(triples)} triples and saved to {os.path.abspath(triples_csv_file)}")
print("Triples:",triples)
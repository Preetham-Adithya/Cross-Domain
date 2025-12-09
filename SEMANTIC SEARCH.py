import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load dataset
data = pd.read_csv("KMapFinal.csv")

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode sentences
sentences = data["article"].dropna().tolist()
embeddings = model.encode(sentences, convert_to_tensor=True)

# Query input
query = input("\n Enter a search query (e.g., 'AI technology'): ")
query_embedding = model.encode(query, convert_to_tensor=True)

# Compute similarity
cosine_scores = util.cos_sim(query_embedding, embeddings)
top_results = cosine_scores[0].argsort(descending=True)[:5]

# Display results
print("\n Top 5 Semantic Matches:")
for idx in top_results:
    print(f"➡ {sentences[idx]}  |  Score: {float(cosine_scores[0][idx]):.3f}")

print("\n Semantic search completed successfully!")
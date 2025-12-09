import pandas as pd
import networkx as nx
from pyvis.network import Network  # ✅ Correct import (not "map.network")

# Load triples (update path as needed)
triples = pd.read_csv("C:/Users/preet/Documents/coding/INFO INT/triples.csv")

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in triples.iterrows():
    subj = row["subject"]
    obj = row["object"]
    rel = row["relation"]
    G.add_node(subj)
    G.add_node(obj)
    G.add_edge(subj, obj, label=rel)

print(f"✅ Graph built with {len(G.nodes())} nodes and {len(G.edges())} edges.")

# Example: print connections for one node
print("\n🔗 Relations for 'Musk':")
if "Musk" in G:
    for neighbor in G["Musk"]:
        print("→", neighbor, "| Relation:", G["Musk"][neighbor]["label"])
else:
    print("⚠️ 'Musk' not found in the graph.")

# Create PyVis network visualization
net = Network(height="600px", width="100%", directed=True, bgcolor="#222222", font_color="white")

# Load NetworkX graph into PyVis
net.from_nx(G)

# Customize edges (add relation labels as tooltips)
for e in G.edges(data=True):
    net.add_edge(e[0], e[1], title=e[2]["label"], label=e[2]["label"])

# Save and open in browser
net.write_html("knowledge_graph.html")
print("🌐 Graph saved as 'knowledge_graph.html' — open it in your browser manually.")


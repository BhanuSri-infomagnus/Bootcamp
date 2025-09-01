from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")
text_file_path = "scraped_data/text.txt"

# Read texts and their corresponding URLs
texts = []
links = []
current_url = ""
with open(text_file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("--- TEXT FROM:"):
            current_url = line.replace("--- TEXT FROM:", "").strip().strip("-").strip()
            continue
        if line:
            texts.append(line)
            links.append(current_url)

# Generate embeddings
embeddings = model.encode(texts, convert_to_tensor=True)
print(f"Generated {len(embeddings)} vector embeddings.")
print("First embedding vector:", embeddings[0])

# Convert embeddings to numpy array
embeddings_np = embeddings.cpu().numpy()

# Create a FAISS index (for cosine similarity, use IndexFlatIP and normalize vectors)
faiss.normalize_L2(embeddings_np)
index = faiss.IndexFlatIP(embeddings_np.shape[1])
index.add(embeddings_np)

# Save the index to disk
faiss.write_index(index, "scraped_data/text_embeddings.faiss")

# Example: Search using a query string
query = input("Enter a query to search: ")
query_embedding = model.encode([query], convert_to_tensor=True).cpu().numpy()
faiss.normalize_L2(query_embedding)
D, I = index.search(query_embedding, k=5)  # Top 5 most similar

similarity_threshold = 0.5  # You can adjust this value

shown = set()
count = 0
for rank, idx in enumerate(I[0]):
    text = texts[idx]
    link = links[idx]
    score = D[0][rank]
    key = (text, score)
    if score < similarity_threshold:
        break
    if key not in shown:
        print(f"\nRank {count+1}:")
        print("Text:", text)
        print("Link:", link)
        print("Similarity score:", score)
        shown.add(key)
        count += 1
    if count == 5:
        break

if count == 0:
    print("No relevant results found for your query.")

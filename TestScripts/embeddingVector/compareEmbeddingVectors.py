import numpy as np
from scipy.spatial.distance import cosine

# Example pack of embedding vectors
pack_of_embeddings = []

with open('output.txt', 'r') as file:
    lines = file.readlines()
    for line in lines[:-1]:  # Exclude the last line
        line = line.strip().strip('[]')  # Remove leading and trailing brackets
        embedding = list(map(float, line.split(',')))
        pack_of_embeddings.append(embedding)
    specific_embedding = list(map(float, lines[-1].strip().strip('[]').split(',')))

# Find the nearest embedding vector using cosine similarity
nearest_embedding = None
min_distance = float('inf')

for embedding in pack_of_embeddings:
    distance = cosine(specific_embedding, embedding)
    if distance < min_distance:
        min_distance = distance
        nearest_embedding = embedding

print("Nearest Embedding Vector:", nearest_embedding)

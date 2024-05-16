import json
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

print("Starting to load clustered data...")

# Load the clustered data
with open('clustered_enterprises.json', 'r', encoding='utf-8') as f:
    clustered_data = json.load(f)

print("Clustered data loaded. Printing for verification:")
# Print loaded data for verification
print(json.dumps(clustered_data, indent=4))

print("Finished printing clustered data.")
# Step 2: Extract descriptions and corresponding cluster labels
descriptions = []
labels = []

for cluster in clustered_data:
    cluster_id = cluster["cluster_id"]
    for enterprise in cluster["enterprises"]:
        descriptions.append(enterprise["description"])
        labels.append(cluster_id)

print(f"Extracted {len(descriptions)} descriptions for embedding.")

# Step 3: Convert descriptions to embeddings
print("Loading SentenceTransformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Converting descriptions to embeddings...")
embeddings = model.encode(descriptions)

print(f"Created {len(embeddings)} embeddings.")

# Step 4: Reduce dimensions for visualization
print("Reducing dimensions using PCA...")
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

print("Dimensions reduced. Preparing to plot clusters.")

plt.figure(figsize=(12, 8))
scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap='viridis', alpha=0.6)

# Adding a color bar to indicate the cluster IDs
colorbar = plt.colorbar(scatter, ticks=range(len(clustered_data)), label='Cluster ID')
colorbar.set_label('Cluster ID')

plt.title('Cluster Visualization of Enterprises')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)

# Save plot to file
output_plot_file = 'cluster_visualization.png'
plt.savefig(output_plot_file)
print(f"Plot saved as {output_plot_file}.")

# Show plot
plt.show()

print("Visualization completed.")
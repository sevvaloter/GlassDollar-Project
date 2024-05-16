import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from google.cloud import language_v1


def load_data():
    with open('enterprises.json') as f:
        enterprises = json.load(f)
    return enterprises


def vectorize_data(data):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    descriptions = [enterprise['description'] for enterprise in data if enterprise['description'].strip()]

    # Debug: Print the descriptions to check their contents
    print("Descriptions (preview, max 5):", descriptions[:5])
    print(f"Total valid descriptions found: {len(descriptions)}")

    if not descriptions:
        raise ValueError("No valid descriptions found for vectorization.")

    vectors = vectorizer.fit_transform(descriptions)
    return vectors


def cluster_data(vectors, k=5):
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(vectors)
    return clusters


def llm_generate_description(clusters):
    # This part will use Google Gemini for LLM description generation. Adjust to your setup
    client = language_v1.LanguageServiceClient()
    descriptions = []

    for cluster_index in range(len(clusters)):
        # Create a cluster description request for Google Gemini (if actual implementation)
        # For now, mock the response with a dummy description
        descriptions.append(f"Description for cluster {cluster_index}")

    return descriptions


def analyze():
    enterprises = load_data()
    vectors = vectorize_data(enterprises)
    clusters = cluster_data(vectors)
    descriptions = llm_generate_description(clusters)

    # Add cluster info to enterprises
    for i, cluster in enumerate(clusters):
        enterprises[i]['cluster'] = cluster

    # Combine clustered results with LLM descriptions
    cluster_analysis = []
    for i, desc in enumerate(descriptions):
        cluster_enterprises = [enterprise for enterprise in enterprises if enterprise.get('cluster') == i]
        cluster_analysis.append({
            'cluster': i,
            'description': desc,
            'enterprises': cluster_enterprises
        })

    with open('cluster_analysis.json', 'w') as f:
        json.dump(cluster_analysis, f, indent=4)


if __name__ == "__main__":
    analyze()
from celery import Celery
import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import logging
import os

# Initialize Celery app
app = Celery('tasks')
app.config_from_object('celeryconfig')

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("celery_task.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.task
def finalize_data(json_file_path):
    try:
        logger.info(f"Reading data from {json_file_path}...")

        if not os.path.exists(json_file_path):
            logger.error(f"File {json_file_path} does not exist.")
            return f"File {json_file_path} does not exist."

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Data loaded successfully from {json_file_path}.")

        clustered_data = cluster_companies(data)
        return "Analysis completed and data saved."
    except Exception as e:
        logger.exception(f"An error occurred during analysis: {str(e)}")
        return f"An error occurred during analysis: {str(e)}"


def process_data(data):
    logger.info("Extracting descriptions from data...")
    enterprises = data.get('data', {}).get('topRankedCorporates', [])
    descriptions = [enterprise['description'] for enterprise in enterprises]
    logger.debug(f"Extracted {len(descriptions)} descriptions.")
    return descriptions


def cluster_companies(data):
    logger.info("Processing and clustering companies...")
    try:
        descriptions = process_data(data)
        if not descriptions:
            logger.error("No descriptions to process.")
            return "No descriptions to process."

        logger.debug(f"Descriptions: {descriptions[:5]}...")  # Displaying only first 5 for brevity

        # Initialize SentenceTransformer model
        logger.info("Loading SentenceTransformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(descriptions)
        logger.debug(f"Embeddings created: {embeddings[:5]}...")  # Displaying only first 5 for brevity

        # Perform clustering
        num_clusters = 10
        logger.info("Performing KMeans clustering...")
        clustering_model = KMeans(n_clusters=num_clusters, random_state=42)
        clusters = clustering_model.fit_predict(embeddings)
        logger.debug(f"Clusters assigned: {clusters[:10]}...")  # Displaying only first 10 for brevity

        # Create clustered data structure
        clustered_data = []
        for cluster_id in range(num_clusters):
            cluster_enterprises = [
                enterprise for idx, enterprise in enumerate(data['data']['topRankedCorporates']) if
                clusters[idx] == cluster_id
            ]
            clustered_data.append({
                'cluster_id': cluster_id,
                'enterprises': cluster_enterprises
            })

        # Save clustered data to JSON file
        output_file = 'clustered_enterprises.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(clustered_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Analysis completed and data saved to {output_file}.")
        return clustered_data

    except Exception as e:
        logger.exception(f"An error occurred during analysis: {str(e)}")
        return None


from crawler_tasks import app
from openai_helper import generate_text


@app.task
def analyze_data(json_file_path):
    try:
        logger.info(f"Starting analysis for {json_file_path}...")

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Data loaded successfully from {json_file_path}.")

        clustered_data = cluster_companies(data)

        # Trigger further LLM analysis
        generate_cluster_descriptions_and_titles(clustered_data)

        return "Analysis completed and data saved."
    except Exception as e:
        logger.exception(f"An error occurred during analysis: {str(e)}")
        return f"An error occurred during analysis: {str(e)}"


def generate_cluster_descriptions_and_titles(clustered_data):
    logger.info("Generating cluster descriptions and titles using OpenAI API...")

    for cluster in clustered_data:
        cluster_companies_descriptions = " ".join(enterprise["description"] for enterprise in cluster["enterprises"])
        prompt_title = f"Generate a title for the following cluster of companies: {cluster_companies_descriptions}"
        prompt_description = f"Generate a description for the following cluster of companies: {cluster_companies_descriptions}"

        cluster['title'] = generate_text(prompt_title)
        cluster['description'] = generate_text(prompt_description)
        logger.debug(f"Generated title: {cluster['title']}, description: {cluster['description']}")

    # Save updated data with generated descriptions and titles
    output_file = 'final_clustered_data_with_titles.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(clustered_data, f, ensure_ascii=False, indent=4)

    logger.info("Cluster descriptions and titles generation completed.")
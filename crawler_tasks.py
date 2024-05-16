from celery import Celery, group
import requests
import json
import logging
from bs4 import BeautifulSoup

# Initialize Celery app
app = Celery('crawler_tasks')
app.config_from_object('celeryconfig')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.task
def crawl_enterprise(url):
    logger.info(f"Starting to crawl {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extracting dummy data for demonstration. Modify based on actual website structure.
    name = soup.find('div', class_='enterprise-name').text.strip()
    description = soup.find('div', class_='enterprise-description').text.strip()
    logo_url = soup.find('img', class_='enterprise-logo')['src']
    hq_city = soup.find('div', class_='hq-city').text.strip()
    hq_country = soup.find('div', class_='hq-country').text.strip()
    website_url = soup.find('a', class_='website-url')['href']
    linkedin_url = soup.find('a', class_='linkedin-url')['href']
    twitter_url = soup.find('a', class_='twitter-url')['href']
    startup_partners = []  # Extract the list of startup partners

    enterprise_data = {
        "name": name,
        "description": description,
        "logo_url": logo_url,
        "hq_city": hq_city,
        "hq_country": hq_country,
        "website_url": website_url,
        "linkedin_url": linkedin_url,
        "twitter_url": twitter_url,
        "startup_partners_count": len(startup_partners),
        "startup_partners": startup_partners,
    }

    logger.info(f"Finished crawling {url}")
    return enterprise_data


@app.task
def crawl_all_enterprises():
    # Assume you have a list of enterprise URLs to crawl
    enterprise_urls = [
        'https://ranking.glassdollar.com/enterprise1',
        'https://ranking.glassdollar.com/enterprise2',
        # Add all enterprise URLs here, possibly fetched dynamically
    ]

    # Define a group of tasks to crawl all enterprises in parallel
    job = group(crawl_enterprise.s(url) for url in enterprise_urls)
    results = job.apply_async()

    # Collect results after all tasks are completed
    enterprises_data = results.get()

    # Save the collective data to a JSON file
    with open('all_enterprises.json', 'w') as f:
        json.dump(enterprises_data, f)

    # Triggering the analysis task after crawling is complete
    app.send_task('tasks.analyze_data', args=('all_enterprises.json',))

    return "Crawling and initial data saving completed."
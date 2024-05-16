import requests
import json


# Send request with specified method, URL, headers, and payload
def send_request(url, method, payload):
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request(method, url, headers=headers, json=payload)
    return response

# Parse the response into JSON format
def get_json_response(response):
    try:
        return response.json()
    except ValueError:
        print("Failed to parse JSON response")
        return None

# Fetch data for top-ranked enterprises
def get_top_ranked_enterprises():
    url = "https://ranking.glassdollar.com/graphql"

    query = """
    query TopRankedCorporates {
      topRankedCorporates {
        id
        name
        description
        logo_url
        hq_city
        hq_country
        website_url
        linkedin_url
        twitter_url
        startup_partners_count
        startup_partners {
          company_name
          logo_url: logo
          city
          website
          country
          theme_gd
          __typename
        }
        startup_friendly_badge
        __typename
      }
    }
    """

    payload = {
        "operationName": "TopRankedCorporates",
        "query": query,
        "variables": {}
    }

    try:
        response_object = send_request(url, 'POST', payload)

        if response_object.status_code == 200:
            return get_json_response(response_object)
        else:
            print(f"Failed to retrieve data from GlassDollar GraphQL API. Status code: {response_object.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    data = get_top_ranked_enterprises()
    if data:
        with open('enterprises.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Enterprise data fetched and saved successfully.")
    else:
        print("Data fetch failed.")
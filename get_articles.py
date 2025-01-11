import httpx
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://thelist.vegas'  # Replace with the correct URL of the page you're scraping

# Headers to simulate a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def fetch_articles():
    # Send GET request to fetch the webpage content
    response = httpx.get(url, headers=headers)
    response.raise_for_status()  # Ensure we notice bad responses

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    current_month = datetime.now().month
    current_year = datetime.now().year
    article_urls = []

    # Loop through each article
    for article in soup.find_all('article', class_='gh-card'):
        date_str = article.find('time', class_='gh-card-date').get('datetime')
        article_date = datetime.strptime(date_str, '%Y-%m-%d')

        # Check if the article's date is within the current month
        if article_date.month == current_month and article_date.year == current_year:
            # Extract the URL for the article
            article_link = article.find('a', class_='gh-card-link')['href']
            article_urls.append(f"https://thelist.vegas{article_link}")

    return article_urls

# Fetch articles and build the response to pass to the main function
def main():
    article_urls = fetch_articles()
    response = ''

    # Loop over each URL and fetch the article content
    with httpx.Client() as client:
        for article_url in article_urls:
            response =  response + client.get(article_url)
    
    # Returning the articles_info, which will be passed to the Flask view
    print(response)
    return response

if __name__ == "__main__":
    # Print the articles info as a response (e.g., for Flask)
    print(main())

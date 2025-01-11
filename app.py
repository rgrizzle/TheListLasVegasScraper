from flask import Flask, render_template
import httpx
from bs4 import BeautifulSoup
import get_articles

app = Flask(__name__)

url = 'https://thelist.vegas/crank-therapy-naked-goths-silent-orchestra-winter-weed-lympics-roast-war-mystic-cat-worst-wrestling-2/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def fetch_events():
    # Fetch article URLs (returns a list of URLs)
    article_urls = get_articles.fetch_articles()

    events = []
    for article_url in article_urls:
        # Fetch the content of each article
        response = httpx.get(article_url, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process the content of the article
        for p in soup.find_all('p'):
            if '➤' in p.text:
                # Extract the entire sentence containing the event
                sentence = p.get_text(strip=True)
                # Find all links within the sentence
                for link in p.find_all('a', href=True):
                    event_name = link.get_text(strip=True)
                    event_link = link['href']
                    # Ensure the event name has at least two words
                    if len(event_name.split()) >= 2:
                        date_part = event_name.split()[-2] + ' ' + event_name.split()[-1]
                        events.append({'name': event_name, 'link': event_link, 'date': date_part})
                    else:
                        print(f"Skipping event with insufficient words: {event_name}")

    return events

@app.route('/')
def index():
    events = fetch_events()

    # Group events by date
    events_by_date = {}
    for event in events:
        date = event['date']
        if date not in events_by_date:
            events_by_date[date] = []
        events_by_date[date].append(event)

 # Sort dates in descending order with a try-except block
    sorted_dates = sorted(events_by_date.keys(), key=lambda x: safe_convert_to_int(x.split()[1]), reverse=True)

    return render_template('index.html', events_by_date=events_by_date, sorted_dates=sorted_dates)



def safe_convert_to_int(date_part):
    # Try to convert to an integer, if it fails, return a default value (e.g., 0)
    try:
        return int(date_part)
    except ValueError:
        print(f"Skipping invalid date part: {date_part}")
        return 0

if __name__ == '__main__':
    app.run(debug=True)

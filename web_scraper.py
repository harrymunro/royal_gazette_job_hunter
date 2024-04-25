import requests
from bs4 import BeautifulSoup

def fetch_website_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container of job postings
    jobs_container = soup.find('div', class_="top-level-classifieds-container")
    if not jobs_container:
        print("No job listings found.")
        return

    # Extract and print each job posting
    job_articles = jobs_container.find_all('div', class_='article')
    for job in job_articles:
        headline = job.find('div', class_='headline').text.strip()
        date = job.find('div', class_='date').text.strip()
        print(f"Job Title: {headline}")
        print(f"{date}")
        print('-' * 80)

def job():
    url = "https://www.royalgazette.com/jobs/"  # Replace with the URL you want to monitor
    fetch_website_content(url)

job()

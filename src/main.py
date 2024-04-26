import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_website_content(url):
    """
    Fetches the content of a website and returns the job titles

    Args:
        url (str): The URL of the website to fetch
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs_container = soup.find('div', class_="top-level-classifieds-container")
    if not jobs_container:
        print("No job listings found.")
        return None

    job_titles = []
    job_articles = jobs_container.find_all('div', class_='article')
    for job in job_articles:
        headline = job.find('div', class_='headline').text.strip()
        job_titles.append(headline)
    return job_titles

def save_jobs(jobs):
    """
    Saves the job titles to a JSON file

    Args:
        jobs (list): A list of job titles to save
    """
    with open('job_titles.json', 'w') as file:
        json.dump(jobs, file)

def load_previous_jobs():
    """
    Loads the previously saved job titles from a JSON file

    Returns:
        list: A list of job titles
    """
    if os.path.exists('job_titles.json'):
        with open('job_titles.json', 'r') as file:
            return json.load(file)
    return []

def compare_jobs(current_jobs, previous_jobs):
    """
    Compares the current job titles with the previous job titles

    Args:
        current_jobs (list): A list of current job titles
        previous_jobs (list): A list of previous job titles
    """
    current_set = set(current_jobs)
    previous_set = set(previous_jobs)

    new_jobs = current_set.difference(previous_set)
    removed_jobs = previous_set.difference(current_set)

    if new_jobs:
        print("New jobs found:")
        for job in new_jobs:
            print(job)
        print('-' * 80)
    else:
        print("No new jobs found.\n")

    if removed_jobs:
        print("Jobs removed:")
        for job in removed_jobs:
            print(job)
        print('-' * 80)
    else:
        print("No jobs removed.\n")

    # Print current jobs excluding new jobs
    existing_jobs = current_set.difference(new_jobs)
    if existing_jobs:
        print("Existing jobs:")
        for job in existing_jobs:
            print(job)
        print('-' * 80)

def job(url):
    """
    Main function to fetch, compare, and save job titles
    """

    current_jobs = fetch_website_content(url)
    if current_jobs is None:
        return

    previous_jobs = load_previous_jobs()
    compare_jobs(current_jobs, previous_jobs)
    save_jobs(current_jobs)

if __name__ == '__main__':
    job(url="https://www.royalgazette.com/jobs/")

import json
import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_config(file_path='local_config_private.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.close()

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

    output = ""

    if new_jobs:
        output += "New jobs found:\n"
        for job in new_jobs:
            output += f"{job}\n"
        output += '-' * 80 + '\n'
    else:
        output += "No new jobs found.\n\n"

    if removed_jobs:
        output += "Jobs removed:\n"
        for job in removed_jobs:
            output += f"{job}\n"
        output += '-' * 80 + '\n'
    else:
        output += "No jobs removed.\n\n"

    # Print current jobs excluding new jobs
    existing_jobs = current_set.difference(new_jobs)
    if existing_jobs:
        output += "Existing jobs:\n"
        for job in existing_jobs:
            output += f"{job}\n"
        output += '-' * 80 + '\n'

    # Print the output
    print(output)
    return output

def job(request):
    url=config['url']
    current_jobs = fetch_website_content(url)
    if current_jobs is None:
        return "No job listings found."

    previous_jobs = load_previous_jobs()
    content = compare_jobs(current_jobs, previous_jobs)
    save_jobs(current_jobs)

    subject = "Royal Gazette Daily Job Updates"
    to_email = config['smtp']['to_email']
    from_email = config['smtp']['from_email']
    smtp_server = config['smtp']['smtp_server']
    smtp_port = config['smtp']['smtp_port']
    smtp_user = config['smtp']['smtp_user']
    smtp_password = config['smtp']['smtp_password']

    send_email(subject, content, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password)
    return "Job updates sent."

if __name__ == "__main__":
    result = job(None)
    print(result)

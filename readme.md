# Royal Gazette Job Hunter

## Overview
This script simplifies the process of checking the Royal Gazette job board. It monitors the job listings at https://www.royalgazette.com/jobs/ and notifies the user of any new job postings or if any postings have been removed since the last check.

## Features
- **Automatic Updates:** Detects and reports new or removed job listings.
- **Ease of Use:** Simple command-line interface.

## Prerequisites
The script uses Python with the `requests` and `beautifulsoup4` libraries. Although the script is set up to use Poetry for dependency management, it's optional because the dependencies are minimal.

## Installation

### With Poetry
If you have Poetry installed, you can easily handle dependencies through it:

1. Clone the repository:
   ```bash
   git clone https://github.com/harrymunro/royal_gazette_job_hunter.git
   cd royal_gazette_job_hunter

2. Install dependencies:
   ```bash
   poetry install
   ```

With pip

If you're not using Poetry, you can install the required libraries using pip:
'pip install requests beautifulsoup4'

Usage

To run the script, navigate to the source directory and execute main.py:
'python src/main.py'

How It Works

Upon execution, the script:

    Fetches current job listings from the Royal Gazette job board.
    Compares these listings against previously stored data to identify any additions or deletions.
    Outputs the current job listings, excluding any new additions, to provide a consistent overview of available jobs.
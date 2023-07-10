#!/usr/bin/env python3

import getpass
import sys
import requests
from bs4 import BeautifulSoup

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    session = requests.Session()

    login_url = "https://intranet.alxswe.com/auth/sign_in/"
    try:
        # Send a GET request to the login URL
        response = session.get(login_url)

        # Check if the request was successful
        if response.status_code != 200:
            logging.error("Failed to retrieve the login page.")
            sys.exit(1)

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the authenticity token from the login form
        authenticity_token = soup.select_one('input[name="authenticity_token"]')['value']

        login_data = {
            "authenticity_token": authenticity_token,
            "user[email]": username,
            "user[password]": password,
            "user[remember_me]": "0"
        }

        # Send a POST request to perform login
        response = session.post(login_url, data=login_data)

        # Check if the login was successful
        if response.status_code != 200:
            logging.error("Login failed with status code: %d", response.status_code)
            sys.exit(1)

    except requests.RequestException as e:
        logging.error("Error occurred during login: %s", str(e))
        sys.exit(1)

    print("Successful login.")

    return session

def scrape_projects(session):
    url = "https://intranet.alxswe.com/projects/current"

    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1').text.strip()
        print(title)

        projects_file = "projects.txt"
        with open(projects_file, 'a') as file:
            project_divs = soup.find_all('div', class_='panel-group')
            for div in project_divs:
                project_list = div.find_all('li')
                for li in project_list:
                    a_tag = li.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        project_url = a_tag['href']
                        full_url = f"https://intranet.alxswe.com{project_url}"
                        file.write(full_url + '\n')
                        project_id = project_url.split('/')[-1]
                        print(f"Added project: {project_id}")

        print("Scraping completed, all items saved in 'projects.txt'.")

    except requests.RequestException as e:
        logging.error("Error occurred during scraping: %s", str(e))
        sys.exit(1)


if __name__ == '__main__':
    session = login()
    scrape_projects(session)

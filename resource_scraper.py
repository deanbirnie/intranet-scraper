#!/usr/bin/env python3

import os
import logging
import getpass
import sys
import requests
import json
from bs4 import BeautifulSoup, Tag
# from urllib.parse import urljoin

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

    return session, soup

def save_resource(project_url, session, soup):
    # Send a GET request to the project URL
    response = session.get(project_url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the project page.")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    project_name = soup.find('h1').text.strip()
    print("Project Name:", project_name)

    # Find the panel with the project description
    panel = soup.find('div', id='project-description')

    if not panel:
        print("Failed to find project description.")
        return

    # Find the resources section within the panel
    resources_section = panel.find('h2', string='Resources')

    if not resources_section:
        print("Failed to find resources section.")
        return

    # Find the ul tags within the resources section
    ul_tags = resources_section.find_next('ul')

    if not ul_tags:
        print("No resources found.")
        return

    # Find the tags within the block
    tags_block = soup.find('div', {'data-react-class': 'tags/Tags'})

    if tags_block:
        tags_data = tags_block.get('data-react-props')
        tags_json = json.loads(tags_data)
        tags = [tag['value'] for tag in tags_json['tags']]
        tags_string = ', '.join(tags)
    else:
        tags_string = ''

    print(tags)
    print("Located tags:", tags_string)

    # Open the text file for writing (create if not exist)
    file_path = 'resources.txt'
    with open(file_path, 'a') as file:
        # Iterate over the li tags within the ul tags
        for li in ul_tags:
            # Check if the tag is an element
            if not isinstance(li, Tag):
                continue

            # Find the anchor tag within the li tag
            a_tag = li.find('a')

            # Check if the anchor tag exists and has the necessary attributes
            if a_tag and 'title' in a_tag.attrs and 'href' in a_tag.attrs:
                href_title = a_tag['title'].strip()
                href_url = a_tag['href']

                if href_url.startswith('/'):
                    href_url = f"https://intranet.alxswe.com{href_url}"

                # Follow the forwarded URL and retrieve the real URL
                response = session.get(href_url, allow_redirects=False)

                # Check if the response is a redirect
                if response.status_code == 302 and 'Location' in response.headers:
                    real_url = response.headers['Location']
                else:
                    real_url = href_url

                # Write the resource entry to the text file
                file.write(f"{project_name}, Tags: [{tags_string}], {href_title}, {real_url}\n")

    print("Resources saved to 'resources.txt' file.")

def process_projects(project_urls, session):
    for project_url in project_urls:
        project_url = project_url.strip()
        print(f"Retrieving the project page from URL: {project_url}")
        response = session.get(project_url)
        ...
        ...

        soup = BeautifulSoup(response.text, 'html.parser')

        save_resource(project_url, session, soup)


if __name__ == '__main__':
    # Set up logging config
    logging.basicConfig(
        level=logging.ERROR,
        format="%(levelname)s: %(message)s"
    )

    # Check if the project URL and topic arguments are provided
    if len(sys.argv) != 2:
        print("Please provide the project URL and topic as arguments.")
        print("Usage: ./resource_scraper {PROJECT_URL|PROJECTS_FILE}")
        sys.exit(1)

    # Get the project URL or projects file from the command-line arguments
    input_arg = sys.argv[1]

    session, soup = login()

    # Check if the input argument is a file
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            project_urls = file.readlines()
            process_projects(project_urls, session)
    else:
        project_url = input_arg
        process_projects([project_url], session)

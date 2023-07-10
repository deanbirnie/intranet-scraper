#!/usr/bin/env python3

import getpass
import os
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

def save_text_file(concept_url):
    # Send a GET request to the concept page
    response = session.get(concept_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve concept page: {concept_url}")
        return

    print(f"Successfully retrieved concept page: {concept_url}")

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text.strip()
    print(title)

    # Find the article element containing the concept content
    article = soup.find('article')

    if not article:
        print("Failed to find concept content.")
        return

    # Extract the concept title from the h1 element
    concept_title = article.find('h1').text.strip()
    concept_title = concept_title.strip("'")

    # Generate the text file path
    file_name = f"{concept_title}.txt"
    file_path = os.path.join("concept-files", file_name)

    # Check if the text file already exists
    if os.path.exists(file_path):
        print(f"Skipping concept: {concept_title} - Text file already exists.")
        return

    os.makedirs("concept-files", exist_ok=True)

    # Extract and format the concept content as text
    content = article.get_text("\n").strip()

    # Write the content to the text file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Saved concept: {concept_title} - Text file: {file_name}")


if __name__ == '__main__':
    session = login()
    print("Logged in.")

    concepts_url = "https://intranet.alxswe.com/concepts"

    try:
        response = session.get(concepts_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        ul = soup.find('ul', class_='list-group')
        if not ul:
            print("No concepts found.")
            sys.exit(0)

        # Create 'concept-files' directory if it doesn't exist
        os.makedirs('concept-files', exist_ok=True)

        li_list = ul.find_all('li')
        for li in li_list:
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                concept_url = f"https://intranet.alxswe.com{a_tag['href']}"
                concept_id = concept_url.split('/')[-1]
                text_file = f"concept-files/{concept_id}.txt"

                # Check if the text file already exists
                if os.path.exists(text_file):
                    print(f"Concept '{concept_id}' already processed. Skipping...")
                    continue

                save_text_file(concept_url)

        print("Files saved in the 'concept-files' directory.")

    except requests.RequestException as e:
        print(f"Error occurred during concept page scraping: {str(e)}")

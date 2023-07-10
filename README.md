# ALX Intranet Scraper

This project acts as a "multi-tool" of sorts for ALX students that utilise the ALX Intranet.

There are multiple tools that can be used to retrieve data from various sources on the ALX Intranet. When combined, they create a faster workflow than if you had to do it all manually.

It is important to note that you must be a student of ALX Software Engionnering with valid login credentials for the Intranet.

## Tools:

### Concept Page Scraper:

With the Concept Page Scraper, you can scrape all of the content from the concept pages on the Intranet. The script looks at the Intranet Concepts Page with all available concept pages at runtime. It will then scrape each individual page for relevant content and store it in the sub-directory `concept-files/` with each file being named after the heading of the associated concept page.

#### Usage:

`$ ./concept-page-scraper.py`

You will be prompted for a username and password (the password is private and will not be displayed on the screen). These credentials are never stored for security.

### Projects Scraper:

The Projects Scraper tool is intended to be used before using the Resource Scraper. It will scan all of your completed projects and create a file called `projects.txt` with a unique URL for each project page, each on a new line. This can then be passed directly to our Resource Scraper tool.

#### Usage:

`$ ./projects-scraper.py`

You will be prompted for a username and password (the password is private and will not be displayed on the screen). These credentials are never stored for security.

### Resource Scraper:

The Resource Scraper tool is designed to return URLs for each resource as suggested by each project. The tool will find all relevant information and create/append to a file called `resources.txt`. The information for each project page includes:
 - the project name
 - the project tags (topics)
 - the resource title
 - the URL for the resource

With this information you can easily access previous resources for stdying or note taking or even quick reference.

#### Usage:

`$ ./resource-scraper.py "{PROJECT_URL | PROJECTS_FILE}"`

Example (URL): `$ ./resource-scraper.py "https://url.com/project/id"`

Example (file): `$ ./resource-scraper.py "projects.txt"`

You will be prompted for a username and password (the password is private and will not be displayed on the screen). These credentials are never stored for security.

## Installation:

`git clone https://github.com/deanbirnie/intranet-scraper.git`

Simply clone the repository and start using the scripts.
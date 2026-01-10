# web-content-auditor

A small Python toolkit for crawling websites and locating embedded content (maps, scripts, analytics, etc.). This repository contains utilities such as `locate.py` used to find links and embedded resources on pages.

## Features
- Crawl a site and discover internal links
- Search page content for specific strings or tags (scripts, anchors)
- Export discovered pages/links to CSV

## Prerequisites
- Python 3.8+
- pip

Recommended Python packages (install via `requirements.txt` or `pip`):

- `requests`
- `beautifulsoup4`
- `urllib3`

## Installation

1. Clone the repo or copy the project folder:

```bash
git clone <your-repo-url>
cd web-content-auditor
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install requests beautifulsoup4 urllib3
```

Or create a `requirements.txt` containing:

```
requests
beautifulsoup4
urllib3
```

and run:

```bash
pip install -r requirements.txt
```

## Usage

Typical usage is to run the main script that orchestrates the crawl. Adjust the target sites and search settings inside the script before running.

Example (from project root):

```bash
python main_app.py
```

Notes:
- `locate.py` contains helper functions such as `find_links`, `extract_internal_links`, and `clean_url`. Ensure those functions are present and imported by the main script (for example `from locate import find_links, extract_internal_links, clean_url`).
- Output is written to `links.csv` by default.

## Configuration
- Edit `main_app.py` to change `websites`, `search_string`, and `search_element`.

---

## Author

Will Michel

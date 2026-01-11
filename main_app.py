import time
from collections import deque
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import csv
from locate import find_links, extract_internal_links, clean_url, csv_export

# List of websites to crawl
websites = [
   'https://example.com'
    
    # Add more sites
]

search_string = "tableau"
# Choose which element to search for: 'script', 'anchor', or 'all'
search_element = 'script'
start_time = time.perf_counter()

# Master list of found map links
found_links = []
# for uniqueness
found_links_set = set()

# Crawl each site
for root_url in websites:
    print(f"\nStarting crawl at: {root_url}")
    
    visited = set()
    to_visit = deque([root_url])
    while to_visit:
        current_url = to_visit.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            # if (clean_url(current_url) in visited):
            print(f"Visiting: {current_url}")
            response = requests.get(current_url, timeout=20, verify=True)
            # Suppress the InsecureRequestWarning
            urllib3.disable_warnings(InsecureRequestWarning)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for links (search_element controls where we look)
            embeds = find_links(soup, search_string, search_element, current_url)
            for embed in embeds:
                if current_url not in found_links_set:
                    found_links.append({
                        "page": current_url
                    })
                    found_links_set.add(current_url)


            # Add new internal links to queue
            internal_links = extract_internal_links(soup, root_url)
            for link in internal_links:
                link=clean_url(link)
                if link not in visited:
                    to_visit.append(link)

        except Exception as e:
            print(f"Error fetching {current_url}: {e}")

    # Export results to CSV params (filename, data, csvfieldnames)
    csv_export("links.csv", found_links, ["page"])


end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"The script ran in {(execution_time/60):.4f} minutes")
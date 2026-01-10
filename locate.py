import requests, re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import urllib3
import csv
from collections import deque


# removes hash marks and query params
def clean_url(url):
    # print(url)
    # replaces index.html
    url = url.replace('index.html','')
    # replaces index.php
    url = url.replace('index.php','')
    # replaces http: with https:
    url = url.replace('http:','https:')  
    # replaces all # and anything after it
    url = re.sub('#.*$','',url)
    # replaces all ? and anything after it
    url = re.sub('\?.*$','',url)
    # replaces all / at the end of string
    url = re.sub('/$','',url)
    return url
 
def is_php_html_or_index(url):
    flag = False;
    excludes = ['document-search', 'files', 'node', 'taxonomy','document','content','media','calendar','pdf','.doc','news','xlsx','.txt','.xls']
    for x in excludes:
        if x in url.lower():
            flag = True
    if flag:
        return False
    else:
        return True
  

# Check if link is same domain
def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

# Extract  links
def find_links(soup, search_string, search_element='script', base_url=None):
    """Find matching items based on `search_element`.

    - search_element == 'script': search script[src]
    - search_element == 'anchor': search a[href]
    - search_element == 'all': search entire HTML/text for the string
    """
    if search_element == 'script':
        links = soup.find_all('script', src=True)
        return [link['src'] for link in links if search_string in link['src']]

    if search_element == 'anchor':
        links = soup.find_all('a', href=True)
        results = []
        for a in links:
            href = a['href']
            full = urljoin(base_url, href) if base_url else href
            if search_string in href or search_string in full:
                results.append(full)
        return results

    if search_element == 'all':
        text = soup.get_text() or ''
        if search_string in text or search_string in str(soup):
            return [search_string]
        return []

    return []

# Extract internal a href and form action links
def extract_internal_links(soup, base_url):
    links = set()

    # <a href="">
    for a in soup.find_all('a', href=True):
        url = urljoin(base_url, a['href'])
        if is_same_domain(base_url, url) and is_php_html_or_index(url):
            links.add(url)

    # <form action="">
    for form in soup.find_all('form', action=True):
        url = urljoin(base_url, form['action'])
        if is_same_domain(base_url, url) and is_php_html_or_index(url):
            links.add(url)

    return links

def csv_export(filename, data, fieldnames):
    # Export to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["page"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print("\n Deep crawl complete. Results saved to '"+filename+"'.")

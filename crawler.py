from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

scanned_urls = []
titles = []


def is_outer_url(url, base_url):
    if base_url in url:
        return False
    return True


def prepare_link(url, href):
    return urljoin(url, href)


def scan_page(url, base_url):

    if url in scanned_urls:
        return

    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    if url.endswith(".html") or url == base_url:
        scanned_urls.append(url)
        titles.append(soup.title.string)

    for link in soup.find_all("a"):
        new_link = prepare_link(url, link.get("href"))
        if not is_outer_url(new_link, base_url):
            scan_page(new_link, base_url)
    return scanned_urls

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

scanned_urls = []
titles = []
outer_links = []


def is_outer_url(url, base_url):
    if base_url in url:
        return False
    return True


def prepare_link(url, href):
    return urljoin(url, href)


def scan_page(url, base_url):
    if url in scanned_urls or url in outer_links:
        return

    if "#" in url:
        outer_links.append(url)
        return

    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    print (url)
    if soup.title:
        if url not in scanned_urls:
            scanned_urls.append(url)
            titles.append(soup.title.string)

        for link in soup.find_all("a"):
            new_link = prepare_link(url, link.get("href"))
            if not is_outer_url(new_link, base_url):
                scan_page(new_link, base_url)
            elif is_outer_url(new_link, base_url):
                outer_links.append(new_link)
                scan_page(new_link, base_url)

    return scanned_urls

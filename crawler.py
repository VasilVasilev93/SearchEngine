from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import os

scanned_urls = []
titles = []
outer_links = []


def is_outer_url(url, base_url):
    if base_url in url:
        return False
    return True


def janitor(reqest, html, soup):
    reqest = None
    html = None
    soup = None


def prepare_link(url, href):
    return urljoin(url, href)


def evaluate():
    pass


def security():
    pass


def check_url(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext != "":
        return False

    if url in scanned_urls or url in outer_links:
        return False

    if "#" in url or "share" in url:
        outer_links.append(url)
        return False
    return True


def scan_page(url, base_url):
    if check_url(url) is True:

        request = requests.get(url)
        html = request.text
        soup = BeautifulSoup(html)

        print (url)

        if soup.title:
            if url not in scanned_urls:
                scanned_urls.append(url)
                titles.append(soup.title.string)

            for link in soup.find_all("a"):
                new_link = prepare_link(url, link.get("href"))
                janitor(request, html, soup)
                if not is_outer_url(new_link, base_url):
                    scan_page(new_link, base_url)
                elif is_outer_url(new_link, base_url):
                    outer_links.append(new_link)
                    scan_page(new_link, base_url)
    else:
        return

    return scanned_urls

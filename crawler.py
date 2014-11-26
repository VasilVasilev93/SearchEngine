from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from create_pages import Page
from create_website import Website
from sqlalchemy import update

scanned_urls = []
outer_links = []
titles = []
ID = []
count = 0


def is_outer_url(url, base_url):
    if base_url in url:
        return False
    return True

def prepare_link(url, href):
    return urljoin(url, href)


def get_domain(url):
    url = url.strip("http://www.")
    return url


def scan_page(session, url, base_url, count):
    count += 1
    if url in scanned_urls or url in outer_links or '#' in url:
        if "#" in url:
            outer_links.append(url)

        return

    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    print (url)

    if soup.title is not None:
        if url not in scanned_urls:
            scanned_urls.append(url)
            titles.append(soup.title.string)
            if count == 1:
                domain = get_domain(url)
                session.add(Website(title=soup.title.string, url=url, domain=domain))
                ID1 = session.query(Website.id).filter(Website.title == soup.title.string).one()
                ID1 = ID1[0]
                ID.append(ID1)
                session.commit()
            elif count > 1:
                session.add(Page(title=soup.title.string, url=url, website_id=ID[0]))
                session.commit()

        for link in soup.find_all("a"):
            new_link = prepare_link(url, link.get("href"))
            if not is_outer_url(new_link, base_url):
                scan_page(session, new_link, base_url, count)
            elif is_outer_url(new_link, base_url):
                #print ('out')
                outer_links.append(new_link)
                scan_page(session, new_link, base_url, count)

    session.execute(update(Website).where(Website.id == ID[0]).values(pages_count=len(soup)))
    session.commit()
    print(count)

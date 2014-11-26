import crawler
from create_pages import Page
from create_website import Website
from create_base import Base
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session


def from_file_to_list(file):
    f = open(file, "r")
    websites = f.read().split("\n")
    f.close()
    return websites


def get_domain(url):
    url = url.strip("http://www.")
    return url


def fill_database(session, titles, scanned_urls):
    site_domain = get_domain(scanned_urls[0])
    session.add(Website(title=titles[0], url=scanned_urls[0], domain=site_domain))
    ID = session.query(Website.id).filter(Website.title == titles[0]).one()
    ID = ID[0]
    for count in range(1, len(titles)):
        session.add(Page(title=titles[count], url=scanned_urls[count], website_id=ID))
    p_count = session.query(Page).filter(Website.id == ID).count()
    p_count += 1  # Main page including
    session.execute(update(Website).where(Website.id == ID).values(pages_count=p_count))
    session.commit()


def crawl(session, websites, titles, urls):
    for item in websites:
        base_url = item
        crawler.scan_page(item, base_url)
        fill_database(session, titles, urls)


def main():
    engine = create_engine("sqlite:///crawl_info.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    websites = from_file_to_list("the_internet.txt")
    crawl(session, websites, crawler.titles, crawler.scanned_urls)

    session.commit()

if __name__ == "__main__":
    main()

import crawler
from create_base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def from_file_to_list(file):
    f = open(file, "r")
    websites = f.read().split("\n")
    f.close()
    return websites


def crawl(session, websites):
    count = 0
    for item in websites:
        base_url = item
        crawler.scan_page(session, item, base_url, count)


def main():
    engine = create_engine("sqlite:///crawl_info.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    websites = from_file_to_list("the_internet.txt")
    crawl(session, websites)

    session.commit()

if __name__ == "__main__":
    main()

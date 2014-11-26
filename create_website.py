from sqlalchemy import Column, Integer, String, Float
from create_base import Base


class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    domain = Column(String)
    pages_count = Column(Integer)
    HTML_ver = Column(Float)

    def __str__(self):
        return "{}| {} - {}".format(self.id, self.url, self.title)

    def __repr__(self):
        return self.__str__()

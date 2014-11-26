from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from create_base import Base


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    website_id = Column(Integer, ForeignKey("website.id"))
    website = relationship("Website", backref="pages")
    ads = Column(String)
    SSL = Column(String)
    points = Column(Float)
    multy_lang = Column(Integer)

    def __str__(self):
        return "{}| {} - {}".format(self.id, self.movie_type, self.time)

    def __repr__(self):
        return self.__str__()

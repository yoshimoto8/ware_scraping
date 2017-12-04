import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Database(Base):
    __tablename__ = 'ware_user_database'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    height = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    title = Column(String(255), nullable=True)
    text = Column(String, nullable=True)
    view = Column(Integer, nullable=True)
    fav = Column(Integer, nullable=True)
    data = Column(String, nullable=True)
    item = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    image = Column(String, nullable=True)


    @staticmethod
    def create_dict(height, sex, title, text, view, fav, date, item, tag, image):
        return {'id': self.id,
                'height': self.height,
                'sex': self.sex,
                'title': self.title,
                'text': self.text,
                'view': self.view,
                'fav': self.fav,
                'date': self.date,
                'item': self.item,
                'tag': self.tag,
                'image': self.image,}

engine = create_engine('mysql+pymysql:///test_database', echo=True)
Base.metadata.create_all(engine)

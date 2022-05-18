from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://gen_user:9xki8zogj@176.57.215.178:3306/default_db', echo=True)

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'YoutubeBot'

    chat_id = Column(Integer, primary_key=True)
    types = Column(String)
    state = Column(String)


class Movies(Base):
    __tablename__ = 'Movies_bot_data'
    id = Column(String, primary_key=True)
    code_id = Column(String, unique=True)
    name = Column(String)


async def new_movie_add(id, code_id, name):
    Session = sessionmaker(bind=engine)
    session = Session()
    movie = Movies(
        id=id,
        code_id=code_id,
        name=name
    )
    session.add(movie)
    session.commit()


async def get_movie_code_id(code_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Movies).filter(Movies.code_id == code_id).one()
    return result


async def new_user_add(chat_id, types, state):
    Session = sessionmaker(bind=engine)
    session = Session()
    customer = Customers(
        chat_id=chat_id,
        types=types,
        state=state
    )
    session.add(customer)
    session.commit()


async def getUserList():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Customers).filter(Customers.types == "user")
    return result


async def getGroupList():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Customers).filter(Customers.types == "group").all()
    return result


async def getUsersCount():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Customers).filter(Customers.types == "user").count()
    return result


async def getGroupsCount():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Customers).filter(Customers.types == "group").count()
    return result

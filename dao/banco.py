from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from modelos.modelos import Base

engine = create_engine('sqlite:///usuarios.db', echo=True)
Session = scoped_session(sessionmaker(bind=engine))

def init_db():
    Base.metadata.create_all(engine)
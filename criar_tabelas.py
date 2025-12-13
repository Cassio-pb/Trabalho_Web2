from dao.banco import engine, Base
from modelos.modelos import *

Base.metadata.create_all(bind=engine)
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON

#é um modelo que vai  representar uma tabela no BD
Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'

    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)

    def __repr__(self):
        return f"<Usuario(email='{self.email}', nome='{self.nome}')>"
    
class Hamburguer(Base):

    __tablename__ = 'hamburguer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable = False)
    ingredientes = Column(String, nullable = False)
    Valor = Column(Integer, nullable = False)
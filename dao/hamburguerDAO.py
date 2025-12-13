from modelos.modelos import Hamburguer
from sqlalchemy.orm import scoped_session
from dao.banco import SessionLocal


def criar_hamburguer(nome,ingredientes,valor):

    db = SessionLocal()
    try:
    
        ham = Hamburguer(nome=nome,ingredientes=ingredientes,Valor=valor)
        db.add(ham)
        db.commit()
        return True
    except Exception as e:
        print(f'erro ao adicionar hamburguer:{e}')
        return False
    finally:
        db.close()

def listar_hambuerguer():

    db = SessionLocal()

    hamburgueres = db.query(Hamburguer).all()
    db.close()

    return hamburgueres

def remover_hamburguer(nome):

    db = SessionLocal()

    hamburguer = db.query(Hamburguer).filter(Hamburguer.nome == nome).first()

    if hamburguer:
        try:
            db.delete(hamburguer)
            db.commit()
            return True
        except Exception as erro:
            print(f'erro ao deletar hamburguer:{erro}')
            return False
        finally:
            db.close()
    else:
        print('hamburguer nao encontrado')
        return False


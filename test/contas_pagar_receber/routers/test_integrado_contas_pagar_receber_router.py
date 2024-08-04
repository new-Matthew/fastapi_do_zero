import sys
import os

# Adicionar o caminho correto ao sys.path para que os módulos sejam encontrados corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from shared.database import Base
from shared.dependencies import get_db

client = TestClient(app)

# Definir o caminho absoluto para o banco de dados dentro do diretório test/contas_pagar_receber/routers
db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_directory, 'test.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}" #melhor usar postgres com docker pois sqlite está dando falsos positivos

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_deve_listar_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/contas-pagar-receber', json={'description': "aluguel", 'value': 1000.5, 'type': "PAGAR"})
    client.post('/contas-pagar-receber', json={'description': "salario", 'value': 5000.5, 'type': "RECEBER"})

    response = client.get('/contas-pagar-receber')
    assert response.status_code == 200
    assert response.json() == [{'id':1, 'description': "aluguel", 'value': 1000.5, 'type': "PAGAR"},
                               {'id':2, 'description': "salario", 'value': 5000.5, 'type': "RECEBER"}
                               ]
    
def test_deve_pegar_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-pagar-receber", json={
        "description": "curso de python",
        "value": 333,
        "type": "PAGAR",
    })

    id_conta_pagar_receber = response.json()['id'] # erro de id

    response_get = client.get(f"/contas-pagar-receber/{id_conta_pagar_receber}")

    assert response_get.status_code == 200
    assert response_get.json()['value'] == 333
    assert response_get.json()['type'] == "PAGAR"
    assert response_get.json()['description'] == "curso de python"

def test_deve_criar_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        'description': "ads",
        'value': 500.5,
        'type': "PAGAR"
    }

    nova_conta_copy= nova_conta.copy() # validar se cada value do json é igual value real nova conta, 
    nova_conta_copy['id'] = 1 # validar pelo id

    response = client.post('/contas-pagar-receber', json=nova_conta)
    assert response.status_code == 201

    assert response.json() == nova_conta_copy # o id é estático então se for igual passa pelo teste

def test_deve_atualizar_conta_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-pagar-receber", json={
        "description": "Curso de Python",
        "value": 333,
        "type": "PAGAR",
    })

    id_conta_pagar_receber = response.json()['id']

    response_get = client.put(f"/contas-pagar-receber/{id_conta_pagar_receber}", json={
        "description": "Curso de Python",
        "value": 111,
        "type": "PAGAR",
    })

    assert response_get.status_code == 200
    assert response_get.json()['value'] == 111

def test_deve_remover_conta_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-pagar-receber", json={
        "description": "Curso de Python",
        "value": 333,
        "type": "PAGAR",
    })

    id_conta_pagar_receber = response.json()['id']

    response_get = client.delete(f"/contas-pagar-receber/{id_conta_pagar_receber}")

    assert response_get.status_code == 204

def test_deve_retornar_erro_quando_exceder_a_description():
    response = client.post('/contas-pagar-receber', json={
        "description": "0123456789012345678901234567890",
        "value": 333,
        "type": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "description"]


def test_deve_retornar_erro_quando_a_description_for_menor_do_que_o_necessario():
    response = client.post('/contas-pagar-receber', json={
        "description": "01",
        "value": 333,
        "type": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "description"]


def test_deve_retornar_erro_quando_o_value_for_zero_ou_menor():
    response = client.post('/contas-pagar-receber', json={
        "description": "Test",
        "value": 0,
        "type": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "value"]

    response = client.post('/contas-pagar-receber', json={
        "description": "Test",
        "value": -1,
        "type": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "value"]


def test_deve_retornar_erro_quando_o_type_for_invalido():
    response = client.post('/contas-pagar-receber', json={
        "description": "Test",
        "value": 100,
        "type": "INVALIDO"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "type"]

if __name__ == "__main__":
    # Executar os testes
    test_deve_listar_contas_pagar_receber()
    test_deve_criar_contas_pagar_receber()
    print("Testes executados com sucesso.")

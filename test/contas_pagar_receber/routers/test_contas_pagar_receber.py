from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_deve_listar_contas_pagar_receber():
    response = client.get('/contas-pagar-receber')

    assert response.status_code == 200

    assert response.json() == [{'id':1, 'description': "aluguel", 'value': 1000.5, 'type': "PAGAR"},
                               {'id':2, 'description': "salário", 'value': 5000.5, 'type': "RECEBER"}
                               ]

def test_deve_criar_contas():
    nova_conta = {
        'description': "ads",
        'value': 500.5,
        'type': "PAGAR"
    }

    nova_conta_copy= nova_conta.copy() # validar se cada valor do json é igual valor real nova conta, 
    nova_conta_copy['id'] = 3 # validar pelo id

    response = client.post('/contas-pagar-receber', json=nova_conta)
    assert response.status_code == 201

    assert response.json() == nova_conta_copy # o id é estático então se for igual passa pelo teste

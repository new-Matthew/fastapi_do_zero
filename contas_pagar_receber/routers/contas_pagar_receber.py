from decimal import Decimal
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
router = APIRouter(prefix="/contas-pagar-receber")


class ContaPagarReceberResponse(BaseModel): # retornar um objeto DTO de saída que extende basemodel, 
    id: int
    description: str
    value: Decimal # mudar p float testar   
    type: str # pagar receber

class ContaPagarReceberRequest(BaseModel): # retornar um objeto DTO de saída que extende basemodel, 
    description: str
    value: Decimal # mudar p float testar   
    type: str # pagar receber

@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(): #como é lista é possível retornar mais de um objeto
    return [
        ContaPagarReceberResponse(
            id=1,
            description= "aluguel",
            value= 1000.5,
            type= "PAGAR"
            ),
        ContaPagarReceberResponse(
            id=2    ,
            description= "salário",
            value= 5000.5,
            type= "RECEBER"
            ),
        ]

@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
            id=3    ,
            description= conta.description,
            value= conta.value,
            type= conta.type
    )


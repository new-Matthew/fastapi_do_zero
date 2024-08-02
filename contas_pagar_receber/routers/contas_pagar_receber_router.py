#from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from contas_pagar_receber.models.contas_pagar_receber_model import ContaPagarReceber
from shared.dependencies import get_db

router = APIRouter(prefix="/contas-pagar-receber")


class ContaPagarReceberResponse(BaseModel): # retornar um objeto DTO de saída que extende basemodel, 
    id: int
    description: str
    value: float # mudar p float testar   
    type: str # pagar receber

class ContaPagarReceberRequest(BaseModel): # retornar um objeto DTO de saída que extende basemodel, 
    description: str
    value: float # mudar p float testar   
    type: str # pagar receber

@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(): #como lista possível retornar mais de um objeto
    return [
        ContaPagarReceberResponse(
            id=1,
            description= "aluguel",
            value= 1000.5,
            type= "PAGAR"
            ),
        ContaPagarReceberResponse(
            id=2    ,
            description= "salario",
            value= 5000.5,
            type= "RECEBER"
            ),
        ]

@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_pagar_receber_request: ContaPagarReceberRequest,
                db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    
    contas_pagar_receber = ContaPagarReceber(
        **conta_pagar_receber_request.dict()# parametros roteados
    ) # está fazendo isso description=conta.description, value=conta.value, type=conta.type

    db.add(contas_pagar_receber)
    db.commit()
    db.refresh(contas_pagar_receber)

    return ContaPagarReceberResponse(
        **contas_pagar_receber.__dict__
    )


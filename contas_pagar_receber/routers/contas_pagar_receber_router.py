from decimal import Decimal
from enum import Enum
from pydantic import Field
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
    value: Decimal # mudar p float testar   
    type: str # pagar receber

    class Config:
        orm_mode = True


class ContaPagarRecebertypeEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'

class ContaPagarReceberRequest(BaseModel): # retornar um objeto DTO de saída que extende basemodel, 
    description: str = Field(min_length=3, max_length=30)
    value: Decimal = Field(gt=0) # mudar p float testar   
    type: ContaPagarRecebertypeEnum # pagar receber

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

@router.get("/{id_conta_pagar_receber}", response_model=ContaPagarReceberResponse)
def obter_conta_por_id(id_conta_pagar_receber: int,
                       db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    conta_pagar_receber: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_pagar_receber)
    return conta_pagar_receber

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

@router.put("/{id_conta_pagar_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def atualizar_conta(id_conta_pagar_receber: int,
                    conta_pagar_receber_request: ContaPagarReceberRequest,
                    db: Session = Depends(get_db)) -> ContaPagarReceberResponse:

    conta_pagar_receber: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_pagar_receber)
    conta_pagar_receber.type = conta_pagar_receber_request.type
    conta_pagar_receber.value = conta_pagar_receber_request.value
    conta_pagar_receber.description = conta_pagar_receber_request.description

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)
    return conta_pagar_receber

@router.delete("/{id_conta_pagar_receber}", status_code=204)
def remover_conta(id_conta_pagar_receber: int,
                    db: Session = Depends(get_db)) -> None:

    conta_pagar_receber = db.query(ContaPagarReceber).get(id_conta_pagar_receber)
    db.delete(conta_pagar_receber)
    db.commit()
    
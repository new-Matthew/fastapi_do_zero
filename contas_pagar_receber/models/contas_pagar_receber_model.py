from sqlalchemy import Column, Integer, String, Numeric
from shared.database import Base


class ContaPagarReceber(Base):
    __tablename__ = 'contas_pagar_receber'

    id = Column(Integer, primary_key=True, autoincrement= True)
    description = Column(String(30))
    value = Column(Numeric)
    type = Column(String(30))

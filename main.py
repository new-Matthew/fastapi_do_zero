import uvicorn
from fastapi import FastAPI
from contas_pagar_receber.routers import contas_pagar_receber

app = FastAPI() # a variável app é um objeto do tipo fastApi

@app.get("/")
def sou_programador() -> str:
    return "sou programador"

app.include_router(contas_pagar_receber.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
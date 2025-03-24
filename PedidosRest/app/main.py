from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje":"Bienvenido al servicio de Pedidos"}
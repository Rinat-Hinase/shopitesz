from fastapi import FastAPI, HTTPException
import uvicorn
from DAO.database import Conexion
from router import pedidosRouter, productosRouter, usuariosRouter


app = FastAPI()
app.include_router(pedidosRouter.router)
app.include_router(productosRouter.router)
app.include_router(usuariosRouter.router)

@app.get("/")
async def home():
    salida = {"mensaje": "Bienvenido a PEDIDOSREST"}
    return salida

@app.on_event("startup")
def startup():
    print("Conectando con MongoDB")

    conexion = Conexion()
    app.conexion=conexion
    app.db = conexion.getDB()

@app.on_event("shutdown")
async def shutdown():
    print("Cerrando la conexion")
    app.conexion.cerrar()

if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1',reload=True)
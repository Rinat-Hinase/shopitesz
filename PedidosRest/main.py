from fastapi import FastAPI, HTTPException
import uvicorn
from router import pedidosRouter, productosRouter, usuariosRouter


app = FastAPI()
app.include_router(pedidosRouter.router)
app.include_router(productosRouter.router)
app.include_router(usuariosRouter.router)

@app.get("/")
async def home():
    salida = {"mensaje": "Bienvenido a PEDIDOSREST"}
    return salida

if __name__ == '__main__':
    uvicorn.run("main:app",host='127.0.0.1',reload=True)
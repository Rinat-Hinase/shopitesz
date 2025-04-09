from fastapi import APIRouter,Request
from typing import Any
from DAO.productosDAO import ProductoDAO
from models.productosModel import ProductosSalida

router = APIRouter(prefix="/productos",tags=["Productos"])


@router.get("/",response_model=ProductosSalida)
async def consulta_General(request:Request)-> Any:
    productoDAO = ProductoDAO(request.app.db)
    return productoDAO.consultaGeneral()

@router.get("/{idProducto}")
async def consulta_Individual(idProducto:int):
    return {"mensaje":"Consultando el producto: " + str(idProducto)}

@router.get("/vendedor/{idVendedor}")
async def consulta_Por_Vendedor(idVendedor:str):
    return {"mensaje":"Consultando productos del vendedor: " + idVendedor}

@router.get("/categorias/{idCategoria}")
async def consulta_Por_Categoria(idCategoria:int):
    return {"mensaje":"Consultando productos de la categoria: " + str(idCategoria)}


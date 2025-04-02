from fastapi import APIRouter

router = APIRouter(prefix="/productos",tags=["Productos"])


@router.get("/")
async def consulta_General():
    return {"mensaje":"Consultando productos"}

@router.get("/{idProducto}")
async def consulta_Individual(idProducto:int):
    return {"mensaje":"Consultando el producto: " + str(idProducto)}

@router.get("/vendedor/{idVendedor}")
async def consulta_Por_Vendedor(idVendedor:str):
    return {"mensaje":"Consultando productos del vendedor: " + idVendedor}

@router.get("/categorias/{idCategoria}")
async def consulta_Por_Categoria(idCategoria:int):
    return {"mensaje":"Consultando productos de la categoria: " + str(idCategoria)}


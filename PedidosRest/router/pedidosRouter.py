import datetime
from fastapi import APIRouter, Request
from DAO.pedidosDAO import PedidoDAO
from models.PedidoModel import PedidoInsert, Item, PedidoPagar,Salida,PedidosSalida, Comprador, Vendedor, PedidoSelect

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/",response_model=Salida)
async def crear_Pedido(pedido:PedidoInsert, request:Request)->Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregar(pedido)

@router.put("/")
async def modificar_Pedido():
    return {"mensaje":"Modificando pedido"}

@router.delete("/")
async def borrar_Pedido():
    return {"mensaje":"Borrando pedido"}

@router.get("/",response_model=PedidosSalida)
async def consultar_Pedidos(request:Request)->PedidosSalida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultaGeneral()

@router.get("/{idPedido}")
async def consultar_Pedido(idPedido:str):
    return {"mensaje":"Consultando el pedido : " + idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregar_Producto(idPedido:str, item:Item):
    items = item.dict()
    salida = {"mensaje":"Agregando un producto al pedido: "+ idPedido, "item: ": items}
    return salida

@router.put("/{idPedido}/pagar",response_model=Salida)
async def pagar_Pedido(idPedido,pedidoPagar:PedidoPagar,request:Request)->Salida:
    pedidoDAO=PedidoDAO(request.app.db)
    return pedidoDAO.pagarPedido(idPedido,pedidoPagar)

#try:
#    funcion()
#except Exception as e:
#    print(f"Error:{str(e)}")

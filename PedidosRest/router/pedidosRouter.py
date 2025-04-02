import datetime
from fastapi import APIRouter
from pymongo import MongoClient
from models.PedidoModel import PedidoInsert, Item, PedidoPagar,Salida,PedidosSalida, Comprador, Vendedor, PedidoSelect

client = MongoClient("mongodb://localhost:27017")
db = client.ShopiteszRest
pedidos_collection = db.pedidos

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/",response_model=Salida)
async def crear_Pedido(pedido:PedidoInsert)->Salida:
    try:
        salida = Salida(estatus="OK", mensaje="Pedido creado exitosamente")
    except Exception as e:
        salida = Salida(estatus=f"Error: {str(e)}", mensaje="No se pudo crear el pedido.")
    return salida

@router.put("/")
async def modificar_Pedido():
    return {"mensaje":"Modificando pedido"}

@router.delete("/")
async def borrar_Pedido():
    return {"mensaje":"Borrando pedido"}

@router.get("/",response_model=PedidosSalida)
async def consultar_Pedidos()->PedidosSalida:
    comprador=Comprador(idComprador=1,nombre="Juan")
    vendedor=Vendedor(idVendedor=1,nombre="Walmart")
    pedido = PedidoSelect(idPedido="500",fechaRegistro=datetime.date.today(),fechaConfirmacion=datetime.date.today(),fechaCierre=datetime.date.today(),costosEnvio=100,subtotal=200,totalPagar=300,estatus="Pagado",comprador=comprador,vendedor=vendedor)
    lista = []
    lista.append(pedido)
    salida = PedidosSalida(estatus="OK",mensaje="Consulta de Pedidos",pedidos=lista)
    return salida

@router.get("/{idPedido}")
async def consultar_Pedido(idPedido:str):
    return {"mensaje":"Consultando el pedido : " + idPedido}

@router.put("/{idPedido}/agregarProducto")
async def agregar_Producto(idPedido:str, item:Item):
    items = item.dict()
    salida = {"mensaje":"Agregando un producto al pedido: "+ idPedido, "item: ": items}
    return salida

@router.put("/{idPedido}/pagar")
async def pagar_Pedido(idPedido,pedidoPagar:PedidoPagar):
    salida = {"mensaje":"Pedido pagado exitosamente", "Pago": pedidoPagar.dict()}
    return salida

#try:
#    funcion()
#except Exception as e:
#    print(f"Error:{str(e)}")

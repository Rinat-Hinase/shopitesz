import datetime
from fastapi import APIRouter, Request
from DAO.pedidosDAO import PedidoDAO
from models.PedidoModel import PedidoInsert, Item, PedidoPagar,Salida,PedidosSalida, Comprador, Vendedor, PedidoSelect, PedidoCancelacion, PedidoConfirmar, PedidoRespuestaDetallada, EventoTracking, TrackingRespuesta

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/",response_model=Salida)
async def crear_Pedido(pedido:PedidoInsert, request:Request)->Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregar(pedido)

@router.put("/")
async def modificar_Pedido():
    return {"mensaje":"Modificando pedido"}

@router.delete("/{idPedido}/cancelar", summary="Cancelar pedido", response_model=Salida)
async def cancelar_Pedido(idPedido: str, pedidoCancelacion: PedidoCancelacion, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.cancelarPedido(idPedido, pedidoCancelacion)

@router.get("/",response_model=PedidosSalida)
async def consultar_Pedidos(request:Request)->PedidosSalida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultaGeneral()

@router.get("/{idPedido}", response_model=PedidoRespuestaDetallada)
async def consultar_pedido_por_id(idPedido: str, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.consultarPedidoPorId(idPedido)


@router.put("/{idPedido}/agregarProducto")
async def agregar_Producto(idPedido:str, item:Item):
    items = item.dict()
    salida = {"mensaje":"Agregando un producto al pedido: "+ idPedido, "item: ": items}
    return salida

@router.put("/{idPedido}/pagar",response_model=Salida)
async def pagar_Pedido(idPedido,pedidoPagar:PedidoPagar,request:Request)->Salida:
    pedidoDAO=PedidoDAO(request.app.db)
    return pedidoDAO.pagarPedido(idPedido,pedidoPagar)

@router.put("/{idPedido}/confirmar", summary="Confirmar pedido", response_model=Salida)
async def confirmar_Pedido(idPedido: str, pedidoConf: PedidoConfirmar, request: Request) -> Salida:
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.confirmarPedido(idPedido, pedidoConf)

@router.post("/{idPedido}/tracking", response_model=Salida)
async def registrar_tracking(idPedido: str, evento: EventoTracking, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.agregarEventoTracking(idPedido, evento.dict())

@router.get("/{idPedido}/tracking", response_model=TrackingRespuesta, summary="Consultar historial de tracking")
async def obtener_tracking_pedido(idPedido: str, request: Request):
    pedidoDAO = PedidoDAO(request.app.db)
    return pedidoDAO.obtenerTrackingPedido(idPedido)



#try:
#    funcion()
#except Exception as e:
#    print(f"Error:{str(e)}")

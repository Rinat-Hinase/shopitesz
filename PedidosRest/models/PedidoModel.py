from pydantic import BaseModel
from datetime import datetime, date
from bson import ObjectId
from typing import Optional

class Item(BaseModel):
    idProducto:int
    cantidad: int
    precio: float
    subtotal: float
    costoEnvio: float
    subtotalEnvio: float

class PedidoInsert(BaseModel):
    idComprador:int
    idVendedor:int
    costoEnvio:float
    subtotal:float
    total:float
    estatus:str | None = 'Captura'
    fechaRegistro: datetime | None = datetime.today()
    detalle: list[Item]

class Pago(BaseModel):
    fecha: datetime | None = datetime.today()
    monto: float
    noTarjeta: str
    estatus: str

class PedidoPagar(BaseModel):
    estatus: str
    pago: Pago

class PedidoRespuesta (BaseModel):
    _id:str
    fechaRegistro:datetime
    costoEnvio:float
    subtotal:float
    total:float

class Salida(BaseModel):
    estatus:str
    mensaje:str

class Comprador(BaseModel):
    idComprador:int
    nombre:str

class Vendedor(BaseModel):
    idVendedor:int
    nombre:str

class PedidoSelect(BaseModel):
    idPedido:str
    fechaRegistro:datetime
    fechaConfirmacion:datetime|None=None
    fechaCierre:date|None=None
    costosEnvio:float
    subtotal:float
    totalPagar:float
    estatus:str
    motivoCancelacion:str|None=None
    valoracion:int|None=None
    comprador:Comprador
    vendedor:Vendedor

class PedidosSalida(Salida):
    pedidos:list[PedidoSelect]
    
class PedidoCancelacion(BaseModel):
    motivoCancelacion:str
    
class ProductoEnvio(BaseModel):
    idProducto: int
    cantidadEnviada: int

class Envio(BaseModel):
    fechaSalida: datetime
    fechaEntPlan: datetime
    noGuia: str
    idPaqueteria: int
    detalle: list[ProductoEnvio]

class PedidoConfirmar(BaseModel):
    fechaConfirmacion: datetime | None = datetime.today()
    estatus: str = "Confirmado"
    envio: Envio


class Paqueteria(BaseModel):
    idPaqueteria: int
    nombre: str

class PedidoItemExtendido(BaseModel):
    idProducto: int
    nombreProducto: str
    cantidadEnviada: int
    cantidadRecibida: int
    comentario: str

class EnvioExtendido(Envio):
    fechaRecepcion: datetime
    paqueteria: Paqueteria
    productos: list[PedidoItemExtendido]

class PedidoExtendido(PedidoSelect):
    envio: EnvioExtendido
    
class PedidoRespuestaDetallada(Salida):
    pedido: PedidoExtendido | None = None  # ← Agrega "| None = None"
    
class PedidoFinalizar(BaseModel):
    estatus: str
    fechaCierre: datetime
    
class EventoTracking(BaseModel):
    evento: str
    lugar: str
    fecha: datetime

class EnvioTracking(BaseModel):
    paqueteria: str
    noGuia: str
    tracking: list[EventoTracking]

class PedidoTracking(BaseModel):
    idPedido: str
    envio: EnvioTracking

class TrackingRespuesta(BaseModel):
    estatus: str
    mensaje: str
    pedido: Optional[PedidoTracking] = None  # <- Esto evita errores si es None





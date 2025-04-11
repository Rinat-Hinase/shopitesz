from pydantic import BaseModel
from datetime import datetime, date
from bson import ObjectId

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

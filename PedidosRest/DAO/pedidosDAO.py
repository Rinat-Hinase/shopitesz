from models.PedidoModel import PedidoInsert, Salida, PedidosSalida, PedidoPagar
from datetime import datetime
from DAO.usuariosDAO import UsuarioDAO
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

class PedidoDAO:
    def __init__(self,db):
        self.db = db

    def agregar(self,pedido:PedidoInsert):
        salida = Salida(estatus='',mensaje='')
        try:
            pedido.fechaRegistro = datetime.today()
            if pedido.idVendedor != pedido.idComprador:
                usuarioDAO = UsuarioDAO(self.db)
                if usuarioDAO.comprobarUsuario(pedido.idComprador) and usuarioDAO.comprobarUsuario(pedido.idVendedor):
                    result = self.db.pedidos.insert_one(jsonable_encoder(pedido))
                    salida.estatus="OK"
                    salida.mensaje=f"Pedido agregado con exito con id: {result.inserted_id}"

                else:
                    salida.estatus="ERROR"
                    salida.mensaje="El usuario comprador o vendedor no existen o se encuentran activos."
            else:
                salida.estatus="ERROR"
                salida.mensaje="No se puede agregar el pedido, porque los ids de los usuarios son iguales."
        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al agregar el pedido, consulta al administrador. Error: {e}"
        return salida

    def consultaGeneral(self):
        salida = PedidosSalida(estatus='',mensaje='',pedidos=[])
        try:
            listatmp = []
            listatmp = list(self.db.pedidosView.find())
            lista = []
            for p in listatmp:
                p['idPedido'] == str(p['idPedido'])
                lista.append(p)
            salida.estatus = "OK"
            salida.mensaje = "Listado de pedidos."
            salida.pedidos = lista
        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al consultar los pedidos. Error: {e}"
            salida.pedidos = None
        return salida

    def evaluarPedido(self,idPedido:str):
        pedido=None
        try:
            pedido=self.db.pedidosView.find_one({'idPedido':idPedido,'estatus':'Captura'})
        except Exception as e:
            print(e)
        return pedido


    def pagarPedido(self,idPedido:str,pedidoPay:PedidoPagar):
        pedido=self.evaluarPedido(idPedido)
        salida=Salida(estatus='',mensaje='')
        try:
            if pedido:
                usuarioDAO=UsuarioDAO(self.db)
                if usuarioDAO.comprobarTarjeta(pedido['comprador'].get("idComprador"),pedidoPay.pago.noTarjeta)==1:
                    if pedido['total'] == pedidoPay.pago.monto and pedidoPay.pago.estatus=='Autorizado':
                        pedidoPay.estatus='Pagado'
                        self.db.pedidos.update_one({'_id':ObjectId(idPedido)},{'$set':{'pago':jsonable_encoder(pedidoPay.pago),'estatus':pedidoPay.estatus}})
                        salida.estatus='OK'
                        salida.mensaje=f'El pedido con id: {idPedido} fue pagado con exito'
                    else:
                        salida.estatus = 'ERROR'
                        salida.mensaje = 'El pedido no se puede pagar porque no se cubre el monto total a pagar.'
                else:
                    salida.estatus = 'ERROR'
                    salida.mensaje = 'El pedido no se puede pagar porque la tarjeta no existe o no pertenece al comprador.'
            else:
                salida.estatus = 'ERROR'
                salida.mensaje = 'El pedido no existe o no se encuentra en captura.'
        except Exception as e:
            print(f"Error: {e}")
        return salida

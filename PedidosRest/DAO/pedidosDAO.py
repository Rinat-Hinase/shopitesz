from models.PedidoModel import PedidoInsert, Salida, PedidosSalida, PedidoPagar, PedidoCancelacion, PedidoConfirmar, PedidoRespuesta, EventoTracking, TrackingRespuesta, EnvioTracking, PedidoTracking
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
    def consultarEstatusPedido(self, idPedido:str):
        estatus=None
        try:
            estatus=self.db.pedidosView.find_one({"idPedido":idPedido}, projection={"estatus":1})
        except Exception as e:  
            print(e)
        return estatus
    from bson import ObjectId  # Importar correctamente

    def cancelarPedido(self, idPedido: str, pedidoCancelacion: PedidoCancelacion) -> Salida:
        salida = Salida(estatus="", mensaje="")
        try:
            pedido = self.db.pedidosView.find_one({"idPedido": idPedido})
            if not pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no existe."
                return salida

            filtro_real = {"_id": ObjectId(idPedido)}

            if pedido["estatus"] == "Captura":
                self.db.pedidos.update_one(
                    filtro_real,
                    {
                        "$set": {
                            "estatus": "Cancelado",
                            "motivoCancelacion": pedidoCancelacion.motivoCancelacion
                        }
                    }
                )
                salida.estatus = "OK"
                salida.mensaje = f"Pedido {idPedido} cancelado exitosamente (Captura)."

            elif pedido["estatus"] == "Pagado":
                self.db.pedidos.update_one(
                    filtro_real,
                    {
                        "$set": {
                            "estatus": "Cancelado",
                            "motivoCancelacion": pedidoCancelacion.motivoCancelacion,
                            "pago.estatus": "Devolucion"
                        }
                    }
                )
                salida.estatus = "OK"
                salida.mensaje = f"Pedido {idPedido} cancelado exitosamente (Pagado), pago marcado para devolución."

            else:
                salida.estatus = "ERROR"
                salida.mensaje = f"No se puede cancelar un pedido en estado '{pedido['estatus']}'."

        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al cancelar el pedido: {str(e)}"

        return salida


            
    def confirmarPedido(self, idPedido: str, pedido_confirmar: PedidoConfirmar) -> Salida:
        # 1. Obtener el pedido por ID desde MongoDB
        pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})
        if not pedido:
            return Salida(estatus="ERROR", mensaje="Pedido no encontrado")

        # 2. Validar que el estatus actual sea 'Pagado'
        if pedido.get("estatus") != "Pagado":
            return Salida(estatus="ERROR", mensaje="El pedido debe estar en estado 'Pagado' para confirmar")

        # 3. Validar que el estatus recibido sea 'Confirmado' (según definición de API)
        if pedido_confirmar.estatus != "Confirmado":
            return Salida(estatus="ERROR", mensaje="El estatus enviado debe ser 'Confirmado'")

        # 4. Comparar detalle del pedido con detalle del envío
        detalles_pedido = pedido.get("detalle", [])
        detalles_envio = pedido_confirmar.envio.detalle or []

        # Verificar que cada producto del pedido tenga correspondencia en el envío
        for det in detalles_pedido:
            # Buscar el producto en el detalle del envío
            encontrado = next((e for e in detalles_envio if e.idProducto == det["idProducto"]), None)
            if not encontrado:
                return Salida(
                    estatus="ERROR",
                    mensaje=f"Producto ID {det['idProducto']} del pedido no se encuentra en el detalle de envío"
                )
            # Verificar que la cantidad enviada coincida
            if encontrado.cantidadEnviada != det["cantidad"]:
                return Salida(
                    estatus="ERROR",
                    mensaje=(f"Cantidad enviada ({encontrado.cantidadEnviada}) no coincide "
                             f"con la cantidad del pedido ({det['cantidad']}) para el producto ID {det['idProducto']}")
                )

        # Opción adicional: verificar que no haya productos extra en el envío
        for envio_det in detalles_envio:
            if not any(d["idProducto"] == envio_det.idProducto for d in detalles_pedido):
                return Salida(
                    estatus="ERROR",
                    mensaje=f"Producto ID {envio_det.idProducto} en el envío no corresponde a ningún producto del pedido"
                )

        # 5. Todas las validaciones pasaron: actualizar el pedido en MongoDB
        # Serializar el objeto de envío a JSON compatible
        envio_data = jsonable_encoder(pedido_confirmar.envio)
        update_result = self.db.pedidos.update_one(
            {"_id": ObjectId(idPedido)},
            {"$set": {
                "fechaConfirmacion": pedido_confirmar.fechaConfirmacion,
                "estatus": "Confirmado",
                "envio": envio_data
            }}
        )
        if update_result.modified_count == 0:
            return Salida(estatus="ERROR", mensaje="No se pudo actualizar el pedido")

        # 6. Retornar éxito
        return Salida(estatus="OK", mensaje="Pedido confirmado correctamente")
    def consultarPedidoPorId(self, idPedido: str):
        from models.PedidoModel import PedidoRespuestaDetallada  # Asegúrate de importar bien
        salida = PedidoRespuestaDetallada(estatus="", mensaje="", pedido=None)
        try:
            pedido = self.db.pedidosFullView.find_one({"idPedido": idPedido})
            print(">>>>> Pedido encontrado en la vista:")
            print(pedido)

            if pedido:
                salida.estatus = "OK"
                salida.mensaje = "Pedido consultado correctamente."
                pedido.pop("_id", None)
                salida.pedido = pedido

            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró el pedido con ese ID."
        except Exception as e:
            print("Error grave:", str(e))
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al consultar pedido: {str(e)}"
        return salida

    def agregarEventoTracking(self, idPedido: str, evento: dict):
        salida = Salida(estatus="", mensaje="")

        try:
            pedido = self.db.pedidos.find_one({"_id": ObjectId(idPedido)})

            if not pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontró el pedido."
                return salida

            if pedido.get("estatus") != "Confirmado":
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no está en estado Confirmado."
                return salida

            if "envio" not in pedido:
                salida.estatus = "ERROR"
                salida.mensaje = "El pedido no contiene información de envío."
                return salida

            if "tracking" not in pedido["envio"]:
                pedido["envio"]["tracking"] = []

            pedido["envio"]["tracking"].append(evento)

            self.db.pedidos.update_one(
                {"_id": ObjectId(idPedido)},
                {"$set": {"envio.tracking": pedido["envio"]["tracking"]}}
            )

            salida.estatus = "OK"
            salida.mensaje = "Evento de tracking agregado correctamente."
        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al agregar evento: {str(e)}"
        return salida
    
    def obtenerTrackingPedido(self, idPedido: str):
        salida = TrackingRespuesta(estatus="", mensaje="", pedido=None)
        try:
            pedido = self.db.trackingPedidosView.find_one({"idPedido": idPedido})
            if pedido:
                # Limpiar el _id si existe
                pedido.pop("_id", None)

                envio = pedido.get("envio", {})

                # Transformar los eventos de tracking en objetos EventoTracking
                tracking = []
                for evt in envio.get("tracking", []):
                    tracking.append(EventoTracking(
                        evento=evt.get("evento"),
                        lugar=evt.get("lugar"),
                        fecha=evt.get("fecha")
                    ))

                envio_obj = EnvioTracking(
                    paqueteria=envio.get("paqueteria"),
                    noGuia=envio.get("noGuia"),
                    tracking=tracking
                )

                pedido_resp = PedidoTracking(
                    idPedido=pedido.get("idPedido"),
                    envio=envio_obj
                )

                salida.estatus = "OK"
                salida.mensaje = "Historial de tracking consultado correctamentes."
                salida.pedido = pedido_resp
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "Pedido no encontrado en la vista."
                salida.pedido = None
        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al consultar el historial de tracking: {str(e)}"
        return salida
    

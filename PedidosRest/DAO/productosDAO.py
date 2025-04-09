from models.productosModel import ProductosSalida


class ProductoDAO:
    def __init__(self,db):
        self.db = db

    def consultaGeneral(self):
        salida = ProductosSalida(estatus='',mensaje='',productos=[])
        try:
            lista = []
            lista = list(self.db.productoView.find()) #debe ser productosView
            salida.estatus = "OK"
            salida.mensaje = "Listado de productos"
            salida.productos = lista
        except Exception as e:
            salida.estatus = "ERROR"
            salida.mensaje = f"Error al consultar los productos. Error: {e}"
            salida.productos = None
        return salida
# modelos.py

class Empresa:
    def __init__(self, id, rut, nombre, direccion=None):
        self.id = id
        self.rut = rut
        self.nombre = nombre
        self.direccion = direccion

    def __str__(self):
        return f"Empresa(id={self.id}, rut={self.rut}, nombre={self.nombre}, direccion={self.direccion})"

class Factura:
    def __init__(self, id, numero_factura, fecha_emision, monto, descripcion, archivo_factura, empresa_id):
        self.id = id
        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision
        self.monto = monto
        self.descripcion = descripcion
        self.archivo_factura = archivo_factura
        self.empresa_id = empresa_id

    def __str__(self):
        return f"Factura(id={self.id}, numero_factura={self.numero_factura}, fecha_emision={self.fecha_emision}, empresa_id={self.empresa_id})"
class Pago:
    def __init__(self, id, factura_id, fecha_pago, monto_pagado, metodo_pago_id, archivo_comprobante):
        self.id = id
        self.factura_id = factura_id
        self.fecha_pago = fecha_pago
        self.monto_pagado = monto_pagado
        self.metodo_pago_id = metodo_pago_id
        self.archivo_comprobante = archivo_comprobante

    def __str__(self):
        return f"Pago(id={self.id}, factura_id={self.factura_id}, fecha_pago={self.fecha_pago}, monto_pagado={self.monto_pagado})"

class MetodoPago:
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"MetodoPago(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})"
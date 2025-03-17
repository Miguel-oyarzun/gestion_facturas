# facturas.py
import db
import empresas  # Importamos el módulo empresas
from datetime import datetime

def listar_facturas():
    """Lista todas las facturas, mostrando información relevante."""
    try:
        facturas = db.ejecutar_consulta("""
            SELECT
                f.id,
                f.numero_factura,
                f.fecha_emision,
                f.monto,
                e.nombre AS nombre_empresa
            FROM Facturas f
            JOIN Empresas e ON f.empresa_id = e.id
            ORDER BY f.fecha_emision DESC
        """, fetchall=True)

        if facturas:
            print("\n--- Listado de Facturas ---")
            for factura in facturas:
                print(f"ID: {factura['id']}, Número: {factura['numero_factura']}, Fecha: {factura['fecha_emision']}, Monto: {factura['monto']}, Empresa: {factura['nombre_empresa']}")
        else:
            print("No hay facturas registradas.")

    except Exception as e:
        print(f"Error al listar facturas: {e}")

def consultar_factura(numero_factura):
    """Muestra los detalles de una factura, incluyendo los pagos asociados."""
    try:
        factura = db.ejecutar_consulta("""
            SELECT
                f.numero_factura,
                f.fecha_emision,
                f.monto,
                f.descripcion,
                e.nombre AS nombre_empresa,
                e.rut AS rut_empresa
            FROM Facturas f
            JOIN Empresas e ON f.empresa_id = e.id
            WHERE f.numero_factura = ?
        """, (numero_factura,), fetchone=True)

        if not factura:
            print("Factura no encontrada.")
            return

        print("\n--- Detalles de la Factura ---")
        print(f"Número: {factura['numero_factura']}")
        print(f"Fecha: {factura['fecha_emision']}")
        print(f"Monto: {factura['monto']}")
        print(f"Descripción: {factura['descripcion']}")
        print(f"Empresa: {factura['nombre_empresa']} (RUT: {factura['rut_empresa']})")

        pagos = db.ejecutar_consulta("""
            SELECT
                p.fecha_pago,
                p.monto_pagado,
                mp.nombre AS metodo_pago
            FROM Pagos p
            JOIN MetodosPago mp ON p.metodo_pago_id = mp.id
            WHERE p.factura_id = (SELECT id FROM Facturas WHERE numero_factura = ?)
        """, (numero_factura,), fetchall=True)

        if pagos:
            print("\n--- Pagos Asociados ---")
            for pago in pagos:
                print(f"Fecha: {pago['fecha_pago']}, Monto: {pago['monto_pagado']}, Método: {pago['metodo_pago']}")
        else:
            print("\nNo hay pagos registrados para esta factura.")

        saldo = calcular_saldo_pendiente(numero_factura)
        print(f"\nSaldo Pendiente: {saldo}")

    except Exception as e:
        print(f"Error al consultar la factura: {e}")

def calcular_saldo_pendiente(numero_factura):
    """Calcula el saldo pendiente de una factura."""
    try:
        factura = db.ejecutar_consulta("SELECT monto FROM Facturas WHERE numero_factura = ?", (numero_factura,), fetchone=True)
        if not factura:
            return None

        monto_factura = factura['monto']

        pagos = db.ejecutar_consulta("""
            SELECT SUM(monto_pagado) AS total_pagado
            FROM Pagos
            WHERE factura_id = (SELECT id FROM Facturas WHERE numero_factura = ?)
        """, (numero_factura,), fetchone=True)

        total_pagado = pagos['total_pagado'] if pagos['total_pagado'] else 0
        saldo = monto_factura - total_pagado
        return saldo

    except Exception as e:
        print(f"Error al calcular el saldo: {e}")
        return None

def buscar_facturas_por_empresa(rut_empresa):
    """Busca facturas por RUT de empresa."""
    try:
        if not utils.validar_rut(rut_empresa):
            print("RUT inválido.")
            return

        facturas = db.ejecutar_consulta("""
            SELECT
                f.numero_factura,
                f.fecha_emision,
                f.monto,
                e.nombre AS nombre_empresa
            FROM Facturas f
            JOIN Empresas e ON f.empresa_id = e.id
            WHERE e.rut = ?
            ORDER BY f.fecha_emision DESC
        """, (rut_empresa,), fetchall=True)

        if facturas:
            print("\n--- Facturas Encontradas ---")
            for factura in facturas:
                print(f"Número: {factura['numero_factura']}, Fecha: {factura['fecha_emision']}, Monto: {factura['monto']}, Empresa: {factura['nombre_empresa']}")
        else:
            print("No se encontraron facturas para esa empresa.")

    except Exception as e:
        print(f"Error al buscar facturas por empresa: {e}")

def buscar_facturas_por_fecha(fecha_inicio_str, fecha_fin_str):
    """Busca facturas por rango de fechas."""
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

        facturas = db.ejecutar_consulta("""
            SELECT
                f.numero_factura,
                f.fecha_emision,
                f.monto,
                e.nombre AS nombre_empresa
            FROM Facturas f
            JOIN Empresas e ON f.empresa_id = e.id
            WHERE f.fecha_emision BETWEEN ? AND ?
            ORDER BY f.fecha_emision DESC
        """, (fecha_inicio, fecha_fin), fetchall=True)  # <---  Aquí CIERRAN las triples comillas

        if facturas:
            print("\n--- Facturas Encontradas ---")
            for factura in facturas:
                print(f"Número: {factura['numero_factura']}, Fecha: {factura['fecha_emision']}, Monto: {factura['monto']}, Empresa: {factura['nombre_empresa']}")
        else:
            print("No se encontraron facturas en ese rango de fechas.")

    except ValueError:
        print("Formato de fecha inválido. Use AAAA-MM-DD.")
    except Exception as e:
        print(f"Error al buscar facturas por fecha: {e}")
# pagos.py
import db
from datetime import datetime

def registrar_pago():
    """Registra un pago para una factura."""
    try:
        # 1. Mostrar facturas y seleccionar una
        facturas = db.ejecutar_consulta("SELECT id, numero_factura, fecha_emision FROM Facturas ORDER BY fecha_emision", fetchall=True)
        if not facturas:
            print("No hay facturas registradas. No se pueden registrar pagos.")
            return

        print("\n--- Facturas Disponibles ---")
        for f in facturas:
            print(f"ID: {f['id']}, Número: {f['numero_factura']}, Fecha: {f['fecha_emision']}")
        
        while True:
            try:
                factura_id = int(input("Ingrese el ID de la factura a la que desea registrar un pago (0 para cancelar): "))
                if factura_id == 0:
                    return
                factura = db.ejecutar_consulta("SELECT * FROM Facturas WHERE id=?", (factura_id,), fetchone=True)
                if not factura:
                    print("ID no corresponde a una factura existente")
                    continue
                break
            except ValueError:
                print("ID de factura inválido. Ingrese un número.")

        # 2. Mostrar métodos de pago y seleccionar uno
        metodos_pago = db.ejecutar_consulta("SELECT id, nombre FROM MetodosPago", fetchall=True)
        print("\n--- Métodos de Pago Disponibles ---")
        for mp in metodos_pago:
            print(f"ID: {mp['id']}, Nombre: {mp['nombre']}")

        while True:
            try:
                metodo_pago_id = int(input("Ingrese el ID del método de pago (0 para cancelar): "))
                if metodo_pago_id == 0:
                    return
                metodo_pago = db.ejecutar_consulta("SELECT * FROM MetodosPago WHERE id = ?", (metodo_pago_id,), fetchone= True)
                if not metodo_pago:
                    print("ID no corresponde a un método de pago existente")
                    continue
                break
            except ValueError:
                print("ID de método de pago inválido. Ingrese un número.")

        # 3. Ingresar datos del pago
        while True:
            fecha_pago_str = input("Ingrese la fecha de pago (AAAA-MM-DD): ")
            try:
                fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Formato de fecha inválido. Use AAAA-MM-DD.")

        while True:
            try:
                monto_pagado = float(input("Ingrese el monto pagado: "))
                if monto_pagado <= 0:
                    print("El monto pagado debe ser mayor que cero.")
                    continue
                break
            except ValueError:
                print("Monto inválido. Ingrese un número.")

        archivo_comprobante = input("Ingrese la ruta al archivo del comprobante (opcional): ")

        # 4. Insertar el pago
        db.ejecutar_consulta("""
            INSERT INTO Pagos (factura_id, fecha_pago, monto_pagado, metodo_pago_id, archivo_comprobante)
            VALUES (?, ?, ?, ?, ?)
        """, (factura_id, fecha_pago, monto_pagado, metodo_pago_id, archivo_comprobante), commit=True)

        print("Pago registrado exitosamente.")

    except Exception as e:
        print(f"Error al registrar el pago: {e}")

def consultar_pagos_factura(numero_factura):
    """Muestra los pagos asociados a una factura."""
    try:
        pagos = db.ejecutar_consulta("""
            SELECT p.fecha_pago, p.monto_pagado, mp.nombre AS metodo_pago
            FROM Pagos p
            JOIN MetodosPago mp ON p.metodo_pago_id = mp.id
            JOIN Facturas f ON p.factura_id = f.id
            WHERE f.numero_factura = ?
        """, (numero_factura,), fetchall=True)

        if pagos:
            print(f"\n--- Pagos de la Factura {numero_factura} ---")
            for pago in pagos:
                print(f"  Fecha: {pago['fecha_pago']}, Monto: {pago['monto_pagado']}, Método: {pago['metodo_pago']}")
        else:
            print("No hay pagos registrados para esta factura.")

    except Exception as e:
        print(f"Error al consultar pagos: {e}")
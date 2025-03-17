# facturas.py
import db  # Importamos el módulo db
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

# ... (El resto de las funciones de facturas.py) ...
def ingresar_factura():
    """Ingresa una nueva factura a la base de datos."""
    conn = None
    try:
        conn, cursor = db.conectar_db()

        # --- 1. Seleccionar la empresa ---
        # listar_empresas()  # Mostrar las empresas existentes, se debe importar el modulo empresas
        while True:
            try:
                empresa_id = int(input("Ingrese el ID de la empresa a la que pertenece la factura (o 0 para cancelar): "))
                if empresa_id == 0:
                    return  # Salir
                #verificar que la empresa exista
                empresa = db.ejecutar_consulta("SELECT * FROM Empresas Where id = ?", (empresa_id,), fetchone = True)
                if not empresa:
                    print("Empresa no existe, intente nuevamente")
                    continue
                break
            except ValueError:
                print("ID inválido, intente nuevamente")

        # --- 2. Obtener datos de la factura ---
        while True:
            numero_factura = input("Ingrese el número de factura: ")
            #validar que la factura no exista
            factura_existente = db.ejecutar_consulta("SELECT * FROM Facturas WHERE numero_factura = ?", (numero_factura,), fetchone = True)
            if factura_existente:
                print("Ya existe una factura con ese número")
                continue
            fecha_emision_str = input("Ingrese la fecha de emisión (AAAA-MM-DD): ")
            try:
                fecha_emision = datetime.strptime(fecha_emision_str, "%Y-%m-%d").date()
            except ValueError:
                print("Formato de fecha inválido. Use AAAA-MM-DD.")
                continue

            while True:
                try:
                    monto = float(input("Ingrese el monto total de la factura: "))
                    if monto <= 0:
                        print("El monto debe ser mayor que cero.")
                        continue
                    break
                except ValueError:
                    print("Monto inválido. Ingrese un número.")

            descripcion = input("Ingrese una descripción (opcional): ")
            ruta_archivo = input("Ingrese la ruta al archivo de la factura (opcional): ")

            # --- 3. Insertar la factura ---
            db.ejecutar_consulta("""
                INSERT INTO Facturas (numero_factura, fecha_emision, monto, descripcion, archivo_factura, empresa_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (numero_factura, fecha_emision, monto, descripcion, ruta_archivo, empresa_id), commit=True)

            print("Factura ingresada exitosamente.")
            break  # Salir del bucle de ingreso de datos de factura

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
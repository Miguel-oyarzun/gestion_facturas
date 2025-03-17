# setup_db.py
import sqlite3

DATABASE_PATH = "gestion_facturas.db"

def conectar_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    cursor = conn.cursor()
    return conn, cursor

def ejecutar_consulta(sql, params=None, fetchone=False, fetchall=False, commit=False):
    """Ejecuta una consulta SQL, con manejo de errores y opciones de retorno."""
    conn = None  # Inicializar conn aquí
    try:
        conn, cursor = conectar_db()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if commit:
            conn.commit()

        if fetchone:
            return cursor.fetchone()
        elif fetchall:
            return cursor.fetchall()
        else:
            return None  # Para INSERT, UPDATE, DELETE que no retornan datos

    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return None
    finally:
        if conn:
            conn.close()

def crear_base_de_datos(db_path=DATABASE_PATH):
    """Crea la base de datos SQLite con las tablas definidas."""
    try:
        conn, cursor = conectar_db()  # Usa la función conectar_db

        # Crear tabla Empresas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                direccion TEXT
            )
        """)

        # Crear tabla Facturas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT NOT NULL UNIQUE,
                fecha_emision DATE NOT NULL,
                monto REAL NOT NULL,
                descripcion TEXT,
                archivo_factura TEXT,
                empresa_id INTEGER NOT NULL,
                FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
            )
        """)

        # Crear tabla MetodosPago
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MetodosPago (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
            )
        """)

        # Crear tabla Pagos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                fecha_pago DATE NOT NULL,
                monto_pagado REAL NOT NULL,
                metodo_pago_id INTEGER,
                archivo_comprobante TEXT,
                FOREIGN KEY (factura_id) REFERENCES Facturas(id),
                FOREIGN KEY (metodo_pago_id) REFERENCES MetodosPago(id)
            )
        """)

        conn.commit()
        print(f"Base de datos '{db_path}' creada exitosamente.")


    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        if conn:  # Asegura que conn esté definido antes de intentar cerrarlo
            conn.close()

def inicializar_datos(db_path=DATABASE_PATH):
    """Inserta datos iniciales (métodos de pago) si la tabla está vacía."""
    try:
        conn, cursor = conectar_db()

        # Verificar si la tabla MetodosPago está vacía
        cursor.execute("SELECT COUNT(*) FROM MetodosPago")
        count = cursor.fetchone()[0]

        if count == 0:
            # Insertar métodos de pago por defecto
            metodos_pago = [
                ("Efectivo", "Pago en efectivo"),
                ("Transferencia", "Transferencia bancaria"),
                ("Tarjeta de Débito", "Pago con tarjeta de débito"),
                ("Tarjeta de Crédito", "Pago con tarjeta de crédito"),
                ("Cheque", "Pago con cheque")
            ]
            cursor.executemany("INSERT INTO MetodosPago (nombre, descripcion) VALUES (?, ?)", metodos_pago)
            conn.commit()
            print("Métodos de pago insertados exitosamente.")
        else:
            print("La tabla MetodosPago ya contiene datos. No se insertaron datos nuevos.")

    except sqlite3.Error as e:
        print(f"Error al inicializar datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_base_de_datos()  # Crea la estructura de la base de datos
    inicializar_datos()  # Inserta los datos iniciales
    print("Base de datos creada e inicializada correctamente.")
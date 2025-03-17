# db.py - VERSION MINIMA PARA PRUEBAS
import sqlite3

DATABASE_PATH = "gestion_facturas.db"

import os
DATABASE_PATH = "gestion_facturas.db"
print(f"Ruta absoluta de la base de datos: {os.path.abspath(DATABASE_PATH)}")

def conectar_db():
    print("Conectando a la base de datos...")  # DEPURACIÓN
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print("Conexión exitosa.")  # DEPURACIÓN
    return conn, cursor

def ejecutar_consulta(sql, params=None, fetchone=False, fetchall=False, commit=False):
    print(f"Ejecutando consulta: {sql} con parámetros: {params}")  # DEPURACIÓN
    conn = None  # Inicializar conn
    try:
        conn, cursor = conectar_db()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if commit:
            conn.commit()
            if sql.strip().upper().startswith("DELETE"):
                rowcount = cursor.rowcount  # Obtener rowcount
                print(f"Filas afectadas (rowcount): {rowcount}")  # DEPURACIÓN
                return rowcount

        if fetchone:
            result = cursor.fetchone()
            print(f"Resultado (fetchone): {result}")  # DEPURACIÓN
            return result
        elif fetchall:
            result = cursor.fetchall()
            print(f"Resultado (fetchall): {result}")  # DEPURACIÓN
            return result
        else:
            print("Consulta sin retorno (None)") # DEPURACION
            return None

    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return None
    finally:
        if conn:
            print("Cerrando conexión...")  # DEPURACIÓN
            conn.close()
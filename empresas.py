# empresas.py
import db
import utils
from modelos import Empresa

def listar_empresas():
    # ... (sin cambios) ...
    try:
        return db.ejecutar_consulta("SELECT * FROM Empresas", fetchall=True)
    except Exception as e:
        print(f"Error al listar empresas: {e}")
        return []  # Retorna una lista vacía en caso de error

def ingresar_empresa(rut, nombre, direccion):
    # ... (sin cambios)
    try:
        db.ejecutar_consulta("INSERT INTO Empresas (rut, nombre, direccion) VALUES (?, ?, ?)", (rut, nombre, direccion), commit=True)
        return True
    except db.sqlite3.IntegrityError:
        print("Error: Ya existe una empresa con ese RUT.")
        return False
    except Exception as e:
        print(f"Error al agregar empresa: {e}")
        return False

def obtener_empresa_por_id(empresa_id):
    # ... (sin cambios)
    try:
        empresa = db.ejecutar_consulta("SELECT * FROM Empresas WHERE id = ?", (empresa_id,), fetchone=True)
        if empresa:
             return Empresa(empresa['id'], empresa['rut'], empresa['nombre'], empresa['direccion'])
        else:
            return None  # O puedes lanzar una excepción personalizada

    except Exception as e:
        print(f"Error al obtener empresa: {e}")
        return None

def actualizar_empresa(empresa_id, rut, nombre, direccion):
    # ... (sin cambios)
    try:
        db.ejecutar_consulta("""
            UPDATE Empresas
            SET rut = ?, nombre = ?, direccion = ?
            WHERE id = ?
        """, (rut, nombre, direccion, empresa_id), commit=True)
        return True
    except db.sqlite3.IntegrityError:
        print("Error: Ya existe una empresa con ese RUT.")
        return False
    except Exception as e:
        print(f"Error al actualizar empresa: {e}")
        return False
def eliminar_empresa(empresa_id):
    """
    Elimina una empresa por su ID.
    Retorna True si la eliminación fue exitosa, False en caso contrario.
    """
    print(f"Intentando eliminar empresa con ID: {empresa_id}")
    try:
        # Verificar si la empresa existe
        empresa = db.ejecutar_consulta("SELECT id FROM Empresas WHERE id = ?", (empresa_id,), fetchone=True)
        print(f"Resultado de la consulta de existencia: {empresa}")
        if not empresa:
            print(f"Error: No existe una empresa con ID {empresa_id}.")
            return False

        # Intentar eliminar la empresa
        filas_afectadas = db.ejecutar_consulta("DELETE FROM Empresas WHERE id = ?", (empresa_id,), commit=True)  # Cambiado a usar rowcount
        print(f"Filas afectadas por la eliminación: {filas_afectadas}")


        # Usar rowcount para verificar si la eliminación fue exitosa
        if filas_afectadas > 0:
            return True
        else:
            print(f"Error: No se pudo eliminar la empresa con ID {empresa_id} (ninguna fila afectada).")
            return False

    except Exception as e:
        print(f"Error al eliminar empresa: {e}")
        return False
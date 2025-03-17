import flet
from flet import (IconButton, Page, Row, TextField, icons, Column,
                  Text, ElevatedButton, DataTable, DataColumn,
                  DataRow, DataCell, AlertDialog, TextButton, SnackBar)
import db
import empresas
import utils
import modelos

def main(page: Page):
    page.title = "Gestión de Facturas"
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.window_width = 800
    page.window_height = 600

    # --- Variables de estado ---
    empresa_seleccionada_id = None
    empresas_table = None
    rut_field = None
    nombre_field = None
    direccion_field = None

    # --- Funciones de manejo de eventos (FUERA de build_empresas_ui) ---

    def eliminar_empresa_click(empresa_id):
        print(f"Función eliminar_empresa_click llamada con ID: {empresa_id}")

        def confirmar_eliminacion(e):
            print("Botón 'Sí' presionado.")
            if empresas.eliminar_empresa(empresa_id):
                actualizar_interfaz()
                dialogo_confirmacion.open = False
                mostrar_dialogo_alerta("Éxito", "Empresa eliminada correctamente.")

            else:
                dialogo_confirmacion.open = False
                mostrar_dialogo_alerta("Error", "No se pudo eliminar la empresa.")
            page.update()

        def cancelar_eliminacion(e):
            print("Botón 'No' presionado.")
            dialogo_confirmacion.open = False
            page.update()

        dialogo_confirmacion = AlertDialog(
            modal=True,
            title=Text("Confirmar Eliminación"),
            content=Text("¿Está seguro de que desea eliminar esta empresa?"),
            actions=[
                TextButton("Sí", on_click=confirmar_eliminacion),
                TextButton("No", on_click=cancelar_eliminacion),
            ],
        )
        page.dialog = dialogo_confirmacion
        dialogo_confirmacion.open = True
        page.update()

    def seleccionar_empresa(empresa_id):
        """Carga los datos de la empresa seleccionada en los campos."""
        nonlocal empresa_seleccionada_id
        empresa = empresas.obtener_empresa_por_id(empresa_id)
        if empresa:
            empresa_seleccionada_id = empresa.id
            rut_field.value = empresa.rut
            nombre_field.value = empresa.nombre
            direccion_field.value = empresa.direccion
            set_campos_empresa_enabled(False)
            page.update()
    def set_campos_empresa_enabled(enabled):
        """Habilita o deshabilita los campos de entrada de la empresa."""
        rut_field.disabled = not enabled
    # --- Interfaz para Empresas (función separada) ---

    def build_empresas_ui():
        """Construye la interfaz de usuario para la sección de Empresas."""
        nonlocal empresa_seleccionada_id
        nonlocal empresas_table
        nonlocal rut_field, nombre_field, direccion_field

        # Los campos *dentro* de build_empresas_ui
        rut_field = TextField(label="RUT", width=150)
        nombre_field = TextField(label="Nombre", width=300)
        direccion_field = TextField(label="Dirección", width=300)

        empresas_table = DataTable(
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("RUT")),
                DataColumn(Text("Nombre")),
                DataColumn(Text("Dirección")),
                DataColumn(Text("Acciones")),
            ],
            rows=[],
        )

        def mostrar_dialogo_alerta(titulo, texto):
            dlg = AlertDialog(
                title=Text(titulo),
                content=Text(texto)
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        def agregar_empresa_click(e):
            nonlocal empresa_seleccionada_id
            nonlocal rut_field, nombre_field, direccion_field
            rut = rut_field.value
            nombre = nombre_field.value
            direccion = direccion_field.value

            if not utils.validar_rut(rut):
                mostrar_dialogo_alerta("Error", "RUT inválido.")
                return

            if not nombre:
                mostrar_dialogo_alerta("Error", "El nombre de la empresa es obligatorio.")
                return

            if empresas.ingresar_empresa(rut, nombre, direccion):
                rut_field.value = ""
                nombre_field.value = ""
                direccion_field.value = ""
                empresa_seleccionada_id = None
                actualizar_interfaz()
                mostrar_dialogo_alerta("Éxito", "Empresa agregada correctamente.")
            else:
                mostrar_dialogo_alerta("Error", "Ya existe una empresa con ese RUT.")

        def actualizar_empresa_click(e):
            nonlocal empresa_seleccionada_id
            nonlocal rut_field, nombre_field, direccion_field
            if empresa_seleccionada_id is None:
                mostrar_dialogo_alerta("Error", "Seleccione una empresa de la lista para actualizar.")
                return

            rut = rut_field.value
            nombre = nombre_field.value
            direccion = direccion_field.value

            if not utils.validar_rut(rut):
                mostrar_dialogo_alerta("Error", "RUT inválido.")
                return

            if not nombre:
                mostrar_dialogo_alerta("Error", "El nombre de la empresa es obligatorio.")
                return

            if empresas.actualizar_empresa(empresa_seleccionada_id, rut, nombre, direccion):
                rut_field.value = ""
                nombre_field.value = ""
                direccion_field.value = ""
                empresa_seleccionada_id = None
                set_campos_empresa_enabled(True)
                actualizar_interfaz()
                mostrar_dialogo_alerta("Éxito", "Empresa actualizada correctamente.")
            else:
                mostrar_dialogo_alerta("Error", "Ya existe una empresa con ese RUT.")

        # Botones
        agregar_button = ElevatedButton("Agregar", on_click=agregar_empresa_click)
        actualizar_button = ElevatedButton("Actualizar", on_click=actualizar_empresa_click)

        # Construir y retornar la interfaz de Empresas, *incluyendo* la tabla
        return Column(
            [
                Text("Empresas", size=20),
                Row([rut_field, nombre_field, direccion_field], alignment="start", vertical_alignment="start"),
                Row([agregar_button, actualizar_button], wrap=True),
                empresas_table,  # Retornamos la tabla
            ]
        )

    def listar_empresas():
        """Obtiene las empresas de la BD y las muestra en la tabla."""
        nonlocal empresas_table
        if empresas_table is None:
            return

        #Usar del(del) para eliminar las filas de una en una
        #empresas_table.rows.clear() #Ya no se limpia
        for row in reversed(empresas_table.rows): # Itera en reversa
            del empresas_table.rows[empresas_table.rows.index(row)] # Elimina

        lista_empresas = empresas.listar_empresas()
        for empresa in lista_empresas:
            empresas_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(empresa['id'])),
                        DataCell(Text(empresa['rut'])),
                        DataCell(Text(empresa['nombre'])),
                        DataCell(Text(empresa['direccion'])),
                        DataCell(
                            Row([
                                IconButton(icon=icons.EDIT_OUTLINED, on_click=lambda e, empresa_id=empresa['id']: seleccionar_empresa(empresa_id)),
                                IconButton(icon=icons.DELETE_OUTLINED, on_click=lambda e, empresa_id=empresa['id']: eliminar_empresa_click(empresa_id)),
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def actualizar_interfaz():
        """Actualiza toda la interfaz de la página."""
        page.controls = [build_empresas_ui()]
        listar_empresas()
        page.update()

    # Inicializar la interfaz
    actualizar_interfaz()
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout,
    QLineEdit, QTextEdit, QMessageBox, QTableWidgetItem, QHBoxLayout,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
print(sys.getdefaultencoding())

class MantenedorTiposPago(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mantenedor de Tipos de Pago")
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.cargar_tipos_pago()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabla_tipos_pago = QTableWidget()
        self.tabla_tipos_pago.setColumnCount(2)
        self.tabla_tipos_pago.setHorizontalHeaderLabels(["Nombre", "Descripción"])
        layout.addWidget(self.tabla_tipos_pago)

        # Botones
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_tipo_pago)
        botones_layout.addWidget(btn_agregar)

        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect(self.editar_tipo_pago)
        botones_layout.addWidget(btn_editar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_tipo_pago)
        botones_layout.addWidget(btn_eliminar)

        layout.addLayout(botones_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cargar_tipos_pago(self):
        self.tabla_tipos_pago.setRowCount(0)
        db = QSqlDatabase.database("conexion_tipos_pago")
        if not db.isValid():
            db = QSqlDatabase.addDatabase("QSQLITE", "conexion_tipos_pago")
            db.setDatabaseName("facturas.db")
            if not db.open():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return

        query = QSqlQuery("SELECT nombre, descripcion FROM MetodosPago", db)
        while query.next():
            row_count = self.tabla_tipos_pago.rowCount()
            self.tabla_tipos_pago.insertRow(row_count)
            self.tabla_tipos_pago.setItem(row_count, 0, QTableWidgetItem(query.value(0)))
            self.tabla_tipos_pago.setItem(row_count, 1, QTableWidgetItem(query.value(1)))

    def agregar_tipo_pago(self):
        dialog = DialogoTipoPago()
        if dialog.exec_() == QDialog.Accepted:
            self.cargar_tipos_pago()

    def editar_tipo_pago(self):
        row = self.tabla_tipos_pago.currentRow()
        if row >= 0:
            nombre = self.tabla_tipos_pago.item(row, 0).text()
            descripcion = self.tabla_tipos_pago.item(row, 1).text()
            dialog = DialogoTipoPago(nombre, descripcion)
            if dialog.exec_() == QDialog.Accepted:
                self.cargar_tipos_pago()

    def eliminar_tipo_pago(self):
        row = self.tabla_tipos_pago.currentRow()
        if row >= 0:
            nombre = self.tabla_tipos_pago.item(row, 0).text()
            db = QSqlDatabase.database("conexion_tipos_pago")
            if not db.isValid():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return

            print(f"Eliminando tipo de pago: {nombre}")  # Registro de depuración

            # Cerrar y volver a abrir la conexión a la base de datos
            db.close()
            if not db.open():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return

            query = QSqlQuery(f"DELETE FROM MetodosPago WHERE nombre = '{nombre}'", db)
            if query.exec_():
                # Cerrar y volver a abrir la conexión a la base de datos
                db.close()
                if not db.open():
                    QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                    return

                self.cargar_tipos_pago()
                print(f"Tipo de pago eliminado: {nombre}")  # Registro de depuración
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el tipo de pago.")
                print(f"Error al eliminar tipo de pago: {nombre}")  # Registro de depuración
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un tipo de pago para eliminar.")
            print("No se seleccionó ningún tipo de pago para eliminar")  # Registro de depuración

    def guardar_tipo_pago(self):
        nombre = self.nombre.text()
        descripcion = self.descripcion.toPlainText()

        db = QSqlDatabase.database("conexion_tipos_pago")
        if not db.isValid():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
            return

        if nombre:
            try:
                db.transaction()
                query = QSqlQuery(f"SELECT nombre FROM MetodosPago WHERE nombre = '{nombre}'", db)
                if query.next():
                    query = QSqlQuery(f"UPDATE MetodosPago SET descripcion = '{descripcion}' WHERE nombre = '{nombre}'", db)
                else:
                    query = QSqlQuery(f"INSERT INTO MetodosPago (nombre, descripcion) VALUES ('{nombre}', '{descripcion}')", db)

                if query.exec_():
                    db.commit()
                    self.cargar_tipos_pago()  # Actualizar la tabla
                    self.accept()
                else:
                    db.rollback()
                    QMessageBox.critical(self, "Error", "No se pudo guardar el tipo de pago.")
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")
            finally:
                pass

class DialogoTipoPago(QDialog):
    def __init__(self, nombre="", descripcion=""):
        super().__init__()
        self.setWindowTitle("Agregar/Editar Tipo de Pago")
        layout = QFormLayout()

        self.nombre = QLineEdit(nombre)
        layout.addRow("Nombre:", self.nombre)

        self.descripcion = QTextEdit(descripcion)
        layout.addRow("Descripción:", self.descripcion)

        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_tipo_pago)
        botones_layout.addWidget(btn_guardar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancelar)

        layout.addRow(botones_layout)

        self.setLayout(layout)

    def guardar_tipo_pago(self):
            nombre = self.nombre.text()
            descripcion = self.descripcion.toPlainText()

            db = QSqlDatabase.database("conexion_tipos_pago")
            if not db.isValid():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return

            if nombre:
                try:
                    query = QSqlQuery(f"INSERT OR IGNORE INTO MetodosPago (nombre, descripcion) VALUES ('{nombre}', '{descripcion}')", db)
                    if query.numRowsAffected() > 0:
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Advertencia", "El tipo de pago ya existe en la base de datos.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")
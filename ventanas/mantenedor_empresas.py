from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout,
    QLineEdit, QMessageBox, QTableWidgetItem, QHBoxLayout,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class MantenedorEmpresas(QMainWindow):
    def __init__(self, ventana_principal):
        super().__init__()
        self.setWindowTitle("Mantenedor de Empresas")
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.cargar_empresas()
        self.ventana_principal = ventana_principal

    def initUI(self):
        layout = QVBoxLayout()

        self.tabla_empresas = QTableWidget()
        self.tabla_empresas.setColumnCount(5)
        self.tabla_empresas.setHorizontalHeaderLabels(["RUT", "Nombre", "Dirección", "Teléfono", "Email"])
        layout.addWidget(self.tabla_empresas)

        # Botones
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_empresa)
        botones_layout.addWidget(btn_agregar)

        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect(self.editar_empresa)
        botones_layout.addWidget(btn_editar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_empresa)
        botones_layout.addWidget(btn_eliminar)

        layout.addLayout(botones_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cargar_empresas(self):
        self.tabla_empresas.setRowCount(0)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("facturas.db")
        if not db.open():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
            return

        query = QSqlQuery("SELECT rut, nombre, direccion, telefono, email FROM Empresas")
        while query.next():
            row_count = self.tabla_empresas.rowCount()
            self.tabla_empresas.insertRow(row_count)
            self.tabla_empresas.setItem(row_count, 0, QTableWidgetItem(query.value(0)))
            self.tabla_empresas.setItem(row_count, 1, QTableWidgetItem(query.value(1)))
            self.tabla_empresas.setItem(row_count, 2, QTableWidgetItem(query.value(2)))
            self.tabla_empresas.setItem(row_count, 3, QTableWidgetItem(query.value(3)))
            self.tabla_empresas.setItem(row_count, 4, QTableWidgetItem(query.value(4)))

        db.close()

    def agregar_empresa(self):
        dialog = DialogoEmpresa()
        if dialog.exec_() == QDialog.Accepted:
            self.cargar_empresas()

    def editar_empresa(self):
        row = self.tabla_empresas.currentRow()
        if row >= 0:
            rut = self.tabla_empresas.item(row, 0).text()
            nombre = self.tabla_empresas.item(row, 1).text()
            direccion = self.tabla_empresas.item(row, 2).text()
            telefono = self.tabla_empresas.item(row, 3).text()
            email = self.tabla_empresas.item(row, 4).text()
            dialog = DialogoEmpresa(rut, nombre, direccion, telefono, email)
            if dialog.exec_() == QDialog.Accepted:
                self.cargar_empresas()

    def eliminar_empresa(self):
        row = self.tabla_empresas.currentRow()
        if row >= 0:
            rut = self.tabla_empresas.item(row, 0).text()
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("facturas.db")
            if not db.open():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return

            query = QSqlQuery(f"SELECT id FROM Empresas WHERE rut = '{rut}'")
            query.next()
            empresa_id = query.value(0)

            if empresa_id == self.ventana_principal.empresa_id:
                QMessageBox.warning(self, "Advertencia", "No se puede eliminar la empresa en sesión.")
                return

            query = QSqlQuery(f"SELECT COUNT(*) FROM FacturaEmpresa WHERE empresa_id = {empresa_id}")
            query.next()
            facturas_asociadas = query.value(0)

            if facturas_asociadas > 0:
                QMessageBox.warning(self, "Advertencia", "No se puede eliminar la empresa. Existen facturas asociadas.")
                return

            query = QSqlQuery(f"DELETE FROM Empresas WHERE rut = '{rut}'")
            if query.exec_():
                self.cargar_empresas()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la empresa.")

            db.close()

class DialogoEmpresa(QDialog):
    def __init__(self, rut="", nombre="", direccion="", telefono="", email=""):
        super().__init__()
        self.setWindowTitle("Agregar/Editar Empresa")
        layout = QFormLayout()

        self.rut = QLineEdit(rut)
        layout.addRow("RUT:", self.rut)

        self.nombre = QLineEdit(nombre)
        layout.addRow("Nombre:", self.nombre)

        self.direccion = QLineEdit(direccion)
        layout.addRow("Dirección:", self.direccion)

        self.telefono = QLineEdit(telefono)
        layout.addRow("Teléfono:", self.telefono)

        self.email = QLineEdit(email)
        layout.addRow("Email:", self.email)

        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_empresa)
        botones_layout.addWidget(btn_guardar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancelar)

        layout.addRow(botones_layout)

        self.setLayout(layout)

    def guardar_empresa(self):
        rut = self.rut.text()
        nombre = self.nombre.text()
        direccion = self.direccion.text()
        telefono = self.telefono.text()
        email = self.email.text()

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("facturas.db")
        if not db.open():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
            return

        if rut:
            query = QSqlQuery(f"SELECT rut FROM Empresas WHERE rut = '{rut}'")
            if query.next():
                query = QSqlQuery(f"UPDATE Empresas SET nombre = '{nombre}', direccion = '{direccion}', telefono = '{telefono}', email = '{email}' WHERE rut = '{rut}'")
            else:
                query = QSqlQuery(f"INSERT INTO Empresas (rut, nombre, direccion, telefono, email) VALUES ('{rut}', '{nombre}', '{direccion}', '{telefono}', '{email}')")

            if query.exec_():
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar la empresa.")

        db.close()
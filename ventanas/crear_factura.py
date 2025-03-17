from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox, QPushButton, QTextEdit,
    QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate  # Importar QDate

class CrearFactura(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Factura")
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        # Widgets para los datos de la factura
        self.numero = QLineEdit()
        layout.addRow("Número:", self.numero)

        self.fecha_emision = QDateEdit()
        self.fecha_emision.setCalendarPopup(True)  # Habilitar el calendario emergente
        self.fecha_emision.setDate(QDate.currentDate())
        layout.addRow("Fecha de Emisión:", self.fecha_emision)

        self.empresa_emisora = QComboBox()
        self.cargar_empresas()  # Función para cargar empresas desde la base de datos
        layout.addRow("Empresa Emisora:", self.empresa_emisora)

        self.monto = QLineEdit()
        layout.addRow("Monto:", self.monto)

        self.pdf_adjunto = QPushButton("Seleccionar PDF")
        self.pdf_adjunto.clicked.connect(self.seleccionar_pdf)
        layout.addRow("PDF Adjunto:", self.pdf_adjunto)

        self.observaciones = QTextEdit()
        layout.addRow("Observaciones:", self.observaciones)

        # Botones de guardar y cancelar
        botones_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_factura)
        botones_layout.addWidget(btn_guardar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancelar)

        layout.addRow(botones_layout)

        self.setLayout(layout)

    def cargar_empresas(self):
        db = QSqlDatabase.database("conexion2")  # Asegúrate de que "conexion2" es el nombre correcto de tu conexión
        if not db.isValid():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos de empresas.")
            return

        query = QSqlQuery("SELECT id, nombre FROM Empresas", db)  # Asegúrate de que "Empresas" es el nombre correcto de tu tabla
        while query.next():
            empresa_id = query.value(0)
            empresa_nombre = query.value(1)
            self.empresa_emisora.addItem(empresa_nombre, empresa_id)

    def seleccionar_pdf(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF files (*.pdf)")
        if filename:
            self.pdf_adjunto.setText(filename)

    def guardar_factura(self):
        numero = self.numero.text()
        fecha_emision = self.fecha_emision.date().toString("yyyy-MM-dd")
        empresa_emisora_id = self.empresa_emisora.currentData()
        monto = self.monto.text()
        pdf_adjunto = self.pdf_adjunto.text()
        observaciones = self.observaciones.toPlainText()

        # Validaciones
        if not numero:
            QMessageBox.critical(self, "Error", "El número de factura no puede estar vacío.")
            return
        try:
            monto = float(monto)  # Convertir a float
        except ValueError:
            QMessageBox.critical(self, "Error", "El monto debe ser un número válido.")
            return

        db = QSqlDatabase.database("conexion2")
        if not db.isValid():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos de facturas.")
            return

        # Cerrar y volver a abrir la conexión a la base de datos
        db.close()
        if not db.open():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos de facturas.")
            return

        query = QSqlQuery(db)
        query.prepare("""
            INSERT INTO Facturas (numero_factura, fecha_emision, monto, archivo_factura, descripcion)
            VALUES (:a, :bb, :bc, :bd, :be)
        """)
        query.addBindValue(numero)
        query.addBindValue(fecha_emision)
        query.addBindValue(monto)
        query.addBindValue(pdf_adjunto)
        query.addBindValue(observaciones)

        print(f"Consulta SQL (Facturas): {query.executedQuery()}")
        print(f"Valores de parámetros (Facturas): {[query.boundValue(i) for i in range(5)]}")

        if query.exec_():
            # Obtener el ID de la factura insertada
            factura_id = query.lastInsertId()

            # Insertar en FacturaEmpresa
            query.prepare("""
                INSERT INTO FacturaEmpresa (factura_id, empresa_id)
                VALUES (:factura_id, :empresa_id)
            """)
            query.addBindValue(factura_id)
            query.addBindValue(empresa_emisora_id)

            print(f"Consulta SQL (FacturaEmpresa): {query.executedQuery()}")
            print(f"Valores de parámetros (FacturaEmpresa): {[query.boundValue(i) for i in range(2)]}")

            if query.exec_():
                self.accept()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la relación factura-empresa. Error: {query.lastError().text()}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la factura. Error: {query.lastError().text()}")
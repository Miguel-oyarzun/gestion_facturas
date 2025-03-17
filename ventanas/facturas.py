from PyQt5.QtWidgets import (
    QMainWindow, QTableView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtSql import QSqlTableModel

class VentanaFacturas(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Facturas")
        self.initUI()

    def initUI(self):
        # Tabla de facturas
        self.tabla_facturas = QTableView()
        self.modelo_facturas = QSqlTableModel()
        self.modelo_facturas.setTable("Facturas")  # Asegúrate de que "Facturas" es el nombre correcto de tu tabla
        self.modelo_facturas.select()
        self.tabla_facturas.setModel(self.modelo_facturas)

        # Botones
        self.btn_agregar_pago = QPushButton("Agregar pago")
        self.btn_ver_detalles = QPushButton("Ver detalles")
        self.btn_eliminar_factura = QPushButton("Eliminar factura")

        # Layout
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.btn_agregar_pago)
        botones_layout.addWidget(self.btn_ver_detalles)
        botones_layout.addWidget(self.btn_eliminar_factura)

        layout = QVBoxLayout()
        layout.addWidget(self.tabla_facturas)
        layout.addLayout(botones_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Conectar botones a funciones
        self.btn_agregar_pago.clicked.connect(self.agregar_pago)
        self.btn_ver_detalles.clicked.connect(self.ver_detalles)
        self.btn_eliminar_factura.clicked.connect(self.eliminar_factura)

    def agregar_pago(self):
        # Implementar la lógica para agregar un pago
        pass

    def ver_detalles(self):
        # Implementar la lógica para ver los detalles de la factura
        pass

    def eliminar_factura(self):
        # Implementar la lógica para eliminar la factura
        pass
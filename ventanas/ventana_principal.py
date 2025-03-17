from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QAction, QMenu,
    QMessageBox, QDialog, QToolBar, QStyle, QSpacerItem, QSizePolicy, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from ventanas.mantenedor_empresas import MantenedorEmpresas
from ventanas.mantenedor_tipos_pago import MantenedorTiposPago
from crear_factura import CrearFactura
from ventanas.facturas import VentanaFacturas

class VentanaPrincipal(QMainWindow):
    def __init__(self, empresa_id):
        super().__init__()
        self.setWindowTitle("Gestión de Facturas")
        self.setGeometry(100, 100, 1200, 800)
        self.empresa_id = empresa_id
        self.initUI()
        self.mostrar_nombre_empresa()
        self.setStyleSheet(self.get_style_sheet())

    def initUI(self):
        # Menu
        menu_bar = self.menuBar()
        menu_mantenedores = menu_bar.addMenu("Mantenedores")

        action_empresas = QAction("Empresas", self)
        action_empresas.triggered.connect(self.abrir_mantenedor_empresas)
        menu_mantenedores.addAction(action_empresas)

        action_tipos_pago = QAction("Tipos de Pago", self)
        action_tipos_pago.triggered.connect(self.abrir_mantenedor_tipos_pago)
        menu_mantenedores.addAction(action_tipos_pago)

        # Layout principal
        main_layout = QHBoxLayout()
        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Botón "Facturas"
        self.btn_facturas = QPushButton("Facturas")
        self.btn_facturas.clicked.connect(self.mostrar_facturas)
        self.btn_facturas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sidebar_layout.addWidget(self.btn_facturas)

        # Botón "Pagos"
        btn_pagos = QPushButton("Pagos")
        btn_pagos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sidebar_layout.addWidget(btn_pagos)

        # Botón "Mantenedor Empresas"
        btn_mantenedor_empresas = QPushButton("Mantenedor Empresas")
        btn_mantenedor_empresas.clicked.connect(self.abrir_mantenedor_empresas)
        btn_mantenedor_empresas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sidebar_layout.addWidget(btn_mantenedor_empresas)

        # Botón "Mantenedor Tipos de Pago"
        btn_mantenedor_tipos_pago = QPushButton("Mantenedor Tipos de Pago")
        btn_mantenedor_tipos_pago.clicked.connect(self.abrir_mantenedor_tipos_pago)
        btn_mantenedor_tipos_pago.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sidebar_layout.addWidget(btn_mantenedor_tipos_pago)

        # Botón "Crear Factura"
        self.btn_crear_factura = QPushButton("Crear Factura")
        self.btn_crear_factura.clicked.connect(self.abrir_crear_factura)
        self.btn_crear_factura.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sidebar_layout.addWidget(self.btn_crear_factura)

        sidebar.setLayout(sidebar_layout)
        sidebar.setObjectName("sidebar")

        # Header
        header = QWidget()
        header_layout = QHBoxLayout()
        self.lbl_empresa = QLabel("")
        header_layout.addWidget(self.lbl_empresa)
        header.setLayout(header_layout)
        header.setObjectName("header")

        # Content
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.addWidget(QLabel("Contenido principal"))
        content.setLayout(content_layout)
        content.setObjectName("content")

        # Organización general
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(header)
        central_layout.addLayout(main_layout)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def mostrar_nombre_empresa(self):
        db = QSqlDatabase.addDatabase("QSQLITE", "conexion2")
        db.setDatabaseName("facturas.db")
        if not db.open():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
            return

        query = QSqlQuery(f"SELECT nombre FROM Empresas WHERE id = {self.empresa_id}", db)
        if query.next():
            nombre_empresa = query.value(0)
            self.lbl_empresa.setText(f"Empresa: {nombre_empresa}")

        db.close()

    def abrir_mantenedor_empresas(self):
        self.mantenedor_empresas = MantenedorEmpresas(self)
        self.mantenedor_empresas.show()

    def abrir_mantenedor_tipos_pago(self):
        self.mantenedor_tipos_pago = MantenedorTiposPago()
        self.mantenedor_tipos_pago.show()

    def get_style_sheet(self):
        return """
        #sidebar {
            background-color: #343a40;
            color: white;
            padding: 20px;
            border-right: 1px solid #495057;
        }
        #header {
            background-color: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
        }
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            margin-bottom: 10px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        #content {
            padding: 20px;
        }
        QLabel {
            font-size: 18px;
        }
        """

    def abrir_crear_factura(self):
        dialogo = CrearFactura()
        if dialogo.exec_() == QDialog.Accepted:
            pass

    def mostrar_facturas(self):
        ventana_facturas = VentanaFacturas(self)
        ventana_facturas.show()
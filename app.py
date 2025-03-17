import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QLabel, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class SeleccionEmpresa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Empresa")
        self.setGeometry(300, 300, 400, 200)
        self.initUI()
        self.cargar_empresas()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_empresas = QComboBox()
        layout.addWidget(self.combo_empresas)

        btn_seleccionar = QPushButton("Seleccionar")
        btn_seleccionar.clicked.connect(self.seleccionar_empresa)
        layout.addWidget(btn_seleccionar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cargar_empresas(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("facturas.db")
        if not db.open():
            QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
            return

        query = QSqlQuery("SELECT id, nombre FROM Empresas")
        while query.next():
            empresa_id = query.value(0)
            empresa_nombre = query.value(1)
            self.combo_empresas.addItem(empresa_nombre, empresa_id)

        db.close()

    def seleccionar_empresa(self):
        empresa_id = self.combo_empresas.currentData()
        if empresa_id is None:
            QMessageBox.warning(self, "Advertencia", "Seleccione una empresa.")
            return

        self.ventana_principal = VentanaPrincipal(empresa_id)
        self.ventana_principal.show()
        self.close()

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
        # Layout principal
        main_layout = QHBoxLayout()
        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QPushButton("Facturas"))
        sidebar_layout.addWidget(QPushButton("Pagos"))
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

    def get_style_sheet(self):
        return """
            #sidebar {
                background-color: #343a40;
                color: white;
                padding: 10px;
            }
            #header {
                background-color: #f8f9fa;
                padding: 10px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeleccionEmpresa()
    window.show()
    sys.exit(app.exec_())
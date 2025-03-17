from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from ventanas.ventana_principal import VentanaPrincipal

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
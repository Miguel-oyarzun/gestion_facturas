import sys
import os
from PyQt5.QtWidgets import QApplication

# Obtiene la ruta absoluta del directorio actual (donde se encuentra main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtiene la ruta absoluta del directorio 'ventanas'
ventanas_dir = os.path.join(current_dir, 'ventanas')

# Agrega el directorio 'ventanas' al sys.path
sys.path.append(ventanas_dir)

from seleccion_empresa import SeleccionEmpresa

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeleccionEmpresa()
    window.show()
    sys.exit(app.exec_())
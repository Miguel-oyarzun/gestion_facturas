# main.py
import db  # Importa el módulo de la base de datos
import empresas
import facturas
import pagos
import informes  # Aunque aún no tenga contenido, ya lo importamos
import utils
from datetime import datetime

def main():
    """Función principal que muestra el menú y ejecuta las acciones."""

    # Crea la base de datos si no existe
    if not db.DATABASE_PATH:
        db.crear_base_de_datos()


    while True:
        print("\n--- Sistema de Gestión de Facturas ---")
        print("1. Listar Empresas")
        print("2. Ingresar Empresa")
        print("3. Listar Facturas")
        print("4. Consultar Factura (por número)")
        print("5. Buscar Facturas por Empresa (por RUT)")
        print("6. Buscar Facturas por Fecha")
        print("7. Ingresar Factura")
        print("8. Registrar Pago")
        print("9. Consultar Pagos de Factura")
        print("x. Salir")  # Usamos 'x' para salir, para evitar confusión con números

        opcion = input("Elija una opción: ")

        if opcion == '1':
            empresas.listar_empresas()
        elif opcion == '2':
            empresas.ingresar_empresa()
        elif opcion == '3':
            facturas.listar_facturas()
        elif opcion == '4':
            num_factura = input("Ingrese el número de factura a consultar: ")
            facturas.consultar_factura(num_factura)
        elif opcion == '5':
            rut = input("Ingrese el RUT de la empresa para buscar facturas: ")
            facturas.buscar_facturas_por_empresa(rut)
        elif opcion == '6':
            fecha_inicio = input("Ingrese la fecha de inicio (AAAA-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (AAAA-MM-DD): ")
            facturas.buscar_facturas_por_fecha(fecha_inicio, fecha_fin)
        elif opcion == '7':
            facturas.ingresar_factura()
        elif opcion == '8':
            pagos.registrar_pago()
        elif opcion == '9':
            num_factura = input("Ingrese el número de factura para ver sus pagos: ")
            pagos.consultar_pagos_factura(num_factura)

        elif opcion.lower() == 'x':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
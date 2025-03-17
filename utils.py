# utils.py
from itertools import cycle

def validar_rut(rut):
    """Valida un RUT chileno de forma más robusta."""
    rut = rut.replace(".", "").replace("-", "").upper()
    if not rut[:-1].isdigit():
        return False
    verificador = rut[-1]
    cuerpo = rut[:-1]

    reversed_digits = map(int, reversed(cuerpo))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    dv = str((-s) % 11)
    if dv == '10':
        dv = 'K'
    if dv == '0':
        dv = '0'  # Se considera válido

    return dv == verificador
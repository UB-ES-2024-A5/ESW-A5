from enum import Enum as PyEnum

# Enum para los estados de los libros en la wishlist
class StateEnum(PyEnum):
    PENDIENTE = "Pendiente"
    ADQUIRIDO = "Adquirido"
    LEIDO = "Leido"
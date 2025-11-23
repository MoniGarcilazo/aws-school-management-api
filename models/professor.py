from dataclasses import dataclass

@dataclass
class Professor:
    id: int
    numeroEmpleado: int
    nombres: str
    apellidos: str
    horasClase: int

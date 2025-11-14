from dataclasses import dataclass

@dataclass
class Professor:
    id: int
    numeroEmpleado: str
    nombres: str
    apellidos: str
    horasClase: float

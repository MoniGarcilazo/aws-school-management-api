from dataclasses import dataclass

@dataclass
class Student:
    id: int
    nombres: str
    apellidos: str
    matricula: str
    promedio: float

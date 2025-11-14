from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    nombres: str = Field(..., min_length=1, description="Nombre del alumno")
    apellidos: str = Field(..., min_length=1, description="Apellidos del alumno")
    matricula: str = Field(..., min_length=1, description="Matrícula única del alumno")
    promedio: float = Field(..., ge=0, le=10, description="Promedio del alumno")

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

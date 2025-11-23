from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    nombres: str = Field(..., min_length=1, description="Nombre del alumno")
    apellidos: str = Field(..., min_length=1, description="Apellidos del alumno")
    matricula: str = Field(..., min_length=1, description="Matrícula única del alumno")
    promedio: float = Field(..., ge=0, le=10, description="Promedio del alumno")

class StudentCreate(StudentBase):
    id: int = Field(..., gt=0, description="Identificador único positivo")
    class Config:
        from_attributes = True

class Student(StudentBase):
    id: int
    class Config:
        from_attributes = True

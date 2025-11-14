from pydantic import BaseModel, Field

class ProfessorBase(BaseModel):
    numeroEmpleado: int = Field(..., gt=0, description="Número de empleado positivo")
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    horasClase: int = Field(..., ge=0, le=40, description="Horas de clase por semana")

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int

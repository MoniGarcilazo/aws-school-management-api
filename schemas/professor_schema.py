from typing import Optional
from pydantic import BaseModel, Field, validator


class ProfessorBase(BaseModel):
    numeroEmpleado: int = Field(..., gt=0)
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    horasClase: int = Field(..., ge=0)

class ProfessorCreate(ProfessorBase):
    id: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class ProfessorUpdate(BaseModel):
    numeroEmpleado: Optional[int] = Field(None, gt=0)
    nombres: Optional[str] = Field(None, min_length=1)
    apellidos: Optional[str] = Field(None, min_length=1)
    horasClase: Optional[int] = Field(None, ge=0)

    class Config:
        from_attributes = True

class Professor(ProfessorBase):
    id: int
    class Config:
        from_attributes = True

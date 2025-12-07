from typing import Optional
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    matricula: str = Field(..., min_length=1)
    promedio: float = Field(..., ge=0, le=10)

class StudentCreate(StudentBase):
    password: str = Field(..., min_length=6)
    class Config:
        from_attributes = True

class Student(StudentBase):
    id: int
    fotoPerfilUrl: Optional[str] = Field(...)

    class Config:
        from_attributes = True

class StudentLogin(BaseModel):
    password: str

    class Config:
        from_attributes = True

class ValidateStudent(BaseModel):
    sessionString: str = Field(..., alias="session_string")

    class Config:
        from_attributes = True
        populate_by_name = True

class SessionResponse(BaseModel):
    sessionString: str

    class Config:
        from_attributes = True
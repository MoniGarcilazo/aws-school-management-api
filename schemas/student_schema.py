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

    class Config:
        from_attributes = True

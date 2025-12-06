from sqlalchemy import Column, Integer, String
from db.database import Base

class ProfessorModel(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numeroEmpleado = Column(Integer, unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    horasClase = Column(Integer, nullable=False)

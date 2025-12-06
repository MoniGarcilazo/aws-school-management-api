from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class StudentModel(Base):
    __tablename__ = "alumnos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    matricula = Column(String(50), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    promedio = Column(Float, nullable=False)
    # fotoPerfilUrl = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)

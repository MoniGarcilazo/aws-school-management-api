from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.professor import ProfessorModel
from schemas.professor_schema import (
    ProfessorCreate,
    ProfessorUpdate,
    Professor
)
from db.deps import get_db

router = APIRouter(prefix="/profesores", tags=["Profesores"])


@router.get("", response_model=list[Professor])
def get_profesores(db: Session = Depends(get_db)):
    return db.query(ProfessorModel).all()


@router.get("/{id}", response_model=Professor)
def get_profesor(id: int, db: Session = Depends(get_db)):
    profesor = db.query(ProfessorModel).filter(ProfessorModel.id == id).first()
    if not profesor:
        raise HTTPException(404, "Profesor no encontrado")
    return profesor


@router.post("", response_model=Professor, status_code=201)
def create_profesor(data: ProfessorCreate, db: Session = Depends(get_db)):
    profesor = ProfessorModel(**data.dict())
    db.add(profesor)
    db.commit()
    db.refresh(profesor)
    return profesor


@router.put("/{id}", response_model=Professor)
def update_profesor(id: int, data: ProfessorUpdate, db: Session = Depends(get_db)):
    profesor = db.query(ProfessorModel).filter(ProfessorModel.id == id).first()
    if not profesor:
        raise HTTPException(404, "Profesor no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(profesor, key, value)

    db.commit()
    db.refresh(profesor)
    return profesor


@router.delete("/{id}")
def delete_profesor(id: int, db: Session = Depends(get_db)):
    profesor = db.query(ProfessorModel).filter(ProfessorModel.id == id).first()
    if not profesor:
        raise HTTPException(404, "Profesor no encontrado")

    db.delete(profesor)
    db.commit()

    return {"message": "Profesor eliminado correctamente"}

from fastapi import APIRouter, HTTPException
from typing import List
from schemas.professor_schema import Professor, ProfessorCreate
from storage.professor_data import profesores

router = APIRouter(prefix="/profesores", tags=["Profesores"])

@router.get("/", response_model=List[Professor])
def get_profesores():
    return profesores

@router.get("/{id}", response_model=Professor)
def get_profesor(id: int):
    for profesor in profesores:
        if profesor.id == id:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.post("/", response_model=Professor, status_code=201)
def create_profesor(data: ProfessorCreate):
    new_id = len(profesores) + 1
    nuevo_profesor = Professor(id=new_id, **data.model_dump())
    profesores.append(nuevo_profesor)
    return nuevo_profesor

@router.put("/{id}", response_model=Professor)
def update_profesor(id: int, data: ProfessorCreate):
    for idx, profesor in enumerate(profesores):
        if profesor.id == id:
            actualizado = Professor(id=id, **data.model_dump())
            profesores[idx] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.delete("/{id}", status_code=200)
def delete_profesor(id: int):
    for idx, profesor in enumerate(profesores):
        if profesor.id == id:
            profesores.pop(idx)
            return {"message": "Profesor eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

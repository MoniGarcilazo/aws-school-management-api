from fastapi import APIRouter, HTTPException
from typing import List
from schemas.professor_schema import ProfessorUpdate, Professor, ProfessorCreate
from storage.professor_data import profesores

router = APIRouter(prefix="/profesores", tags=["Profesores"])


@router.get("", response_model=List[Professor])
def get_profesores():
    return profesores


@router.get("/{id}", response_model=Professor)
def get_profesor(id: int):
    for profesor in profesores:
        if profesor.id == id:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")


@router.post("", response_model=Professor, status_code=201)
def create_profesor(data: ProfessorCreate):
    nuevo = Professor(**data.dict())
    profesores.append(nuevo)
    return nuevo


@router.put("/{id}", response_model=Professor)
def update_profesor(id: int, data: ProfessorUpdate):
    for idx, profesor in enumerate(profesores):
        if profesor.id == id:

            if data.nombres is None or data.horasClase is None:
                raise HTTPException(status_code=400, detail="Campos inválidos")

            updated = profesor.copy(update=data.dict(exclude_unset=True))

            try:
                updated = Professor(**updated.dict())
            except:
                raise HTTPException(status_code=400, detail="Datos inválidos")

            profesores[idx] = updated
            return updated

    raise HTTPException(status_code=404, detail="Profesor no encontrado")


@router.delete("/{id}", status_code=200)
def delete_profesor(id: int):
    for idx, profesor in enumerate(profesores):
        if profesor.id == id:
            profesores.pop(idx)
            return {"message": "Profesor eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

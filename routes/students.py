from fastapi import APIRouter, HTTPException
from typing import List
from schemas.student_schema import Student, StudentCreate
from storage.student_data import alumnos

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

@router.get("/", response_model=List[Student])
def get_alumnos():
    return alumnos

@router.get("/{id}", response_model=Student)
def get_alumno(id: int):
    for alumno in alumnos:
        if alumno.id == id:
            return alumno
    raise HTTPException(status_code=404, detail="Alumno no encontrado")

@router.post("/", response_model=Student, status_code=201)
def create_alumno(data: StudentCreate):
    new_id = len(alumnos) + 1
    nuevo_alumno = Student(id=new_id, **data.model_dump())
    alumnos.append(nuevo_alumno)
    return nuevo_alumno

@router.put("/{id}", response_model=Student)
def update_alumno(id: int, data: StudentCreate):
    for idx, alumno in enumerate(alumnos):
        if alumno.id == id:
            actualizado = Student(id=id, **data.model_dump())
            alumnos[idx] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Alumno no encontrado")

@router.delete("/{id}", status_code=204)
def delete_alumno(id: int):
    for idx, alumno in enumerate(alumnos):
        if alumno.id == id:
            alumnos.pop(idx)
            return {"message": "Alumno eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Alumno no encontrado")

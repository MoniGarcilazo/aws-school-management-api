from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from models.student import StudentModel
from schemas.student_schema import StudentCreate, Student
from db.deps import get_db
from utils.security import hash_password
import boto3, os, uuid

from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.get("/", response_model=list[Student])
def get_alumnos(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


@router.get("/{id}", response_model=Student)
def get_alumno(id: int, db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).filter(StudentModel.id == id).first()
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")
    return alumno


@router.post("/", response_model=Student, status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    hashed = hash_password(data.password) 
    
    nuevo_alumno = StudentModel(
        nombres=data.nombres,
        apellidos=data.apellidos,
        matricula=data.matricula,
        promedio=data.promedio,
        password=hashed
    )
    
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)
    return nuevo_alumno

@router.put("/{id}", response_model=Student)
def update_alumno(id: int, data: StudentCreate, db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).filter(StudentModel.id == id).first()
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")

    for key, value in data.model_dump().items():
        setattr(alumno, key, value)

    db.commit()
    db.refresh(alumno)
    return alumno


@router.post("/{id}/fotoPerfil", status_code=200)
def upload_photo(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).get(id)
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")

    s3 = boto3.client("s3",
                      aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                      aws_session_token=os.getenv("AWS_SESSION_TOKEN"))
    bucket = os.getenv("S3_BUCKET")
    ext = file.filename.split(".")[-1]
    key = f"alumnos/{id}/{uuid.uuid4()}.{ext}"
    content = file.file.read()
    s3.put_object(Bucket=bucket, Key=key, Body=content, ACL='public-read', ContentType=file.content_type)
    url = f"https://{bucket}.s3.amazonaws.com/{key}"

    alumno.fotoPerfilUrl = url
    db.commit()
    db.refresh(alumno)
    return {"fotoPerfilUrl": url}

@router.delete("/{id}")
def delete_alumno(id: int, db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).filter(StudentModel.id == id).first()
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")

    db.delete(alumno)
    db.commit()

    return {"message": "Alumno eliminado correctamente"}

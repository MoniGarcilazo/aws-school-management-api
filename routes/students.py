from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from models.student import StudentModel
from schemas.student_schema import SessionResponse, StudentCreate, Student, StudentLogin, ValidateStudent
from db.deps import get_db
from services.session_service import create_session, get_session_by_string, invalidate_session
from services.sns_service import send_student_notification
from utils.security import hash_password, verify_password
import boto3, os, uuid

from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.get("", response_model=list[Student])
def get_alumnos(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


@router.get("/{id}", response_model=Student)
def get_alumno(id: int, db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).filter(StudentModel.id == id).first()
    
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")
    return alumno


@router.post("", response_model=Student, status_code=201)
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
async def upload_photo(id: int, foto: UploadFile = File(...), db: Session = Depends(get_db)):
    alumno = db.query(StudentModel).get(id)
    if not alumno:
        raise HTTPException(404, "Alumno no encontrado")
    
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET = os.getenv("S3_BUCKET")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=AWS_REGION
    )
    
    ext = foto.filename.split(".")[-1]
    key = f"alumnos/{id}/{uuid.uuid4()}.{ext}"

    try:
        content = await foto.read()
    
        s3_client.put_object(
            Bucket=S3_BUCKET, 
            Key=key, 
            Body=content, 
            ACL='public-read', 
            ContentType=foto.content_type
        )
    except Exception as e:
        print(f"Error en S3 (put_object): {e}")
        raise HTTPException(status_code=500, detail=f"Error al subir la foto: {str(e)}")

    url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"

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

@router.post("/{id}/email", summary="Enviar calificaciones del alumno por SNS")
def send_email_notification(
    id: int,
    db: Session = Depends(get_db)
):
    alumno = db.query(StudentModel).filter(StudentModel.id == id).first()

    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    send_student_notification(
        nombres=alumno.nombres,
        apellidos=alumno.apellidos,
        matricula=alumno.matricula,
        promedio=alumno.promedio
    )

    return {"success": True, "message": "Notificación enviada exitosamente"}


@router.post("/{id}/session/login", response_model=SessionResponse)
def login_session(id: int, data: StudentLogin, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == id).first() 

    if not student:
        raise HTTPException(404, "Alumno no encontrado")

    if not verify_password(data.password, student.password): 
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    session_string = create_session(id)

    return SessionResponse(sessionString=session_string)


@router.post("/{id}/session/verify", status_code=200)
def verify_session(id: int, data: ValidateStudent):

    session = get_session_by_string(data.sessionString)

    if not session:
        raise HTTPException(400, "Sesión no encontrada")

    if session["alumnoId"] != id:
        raise HTTPException(400, "La sesión no pertenece a este alumno")

    if not session["active"]:
        raise HTTPException(400, "La sesión está inactiva")

    return {"valid": True}


@router.post("/{id}/session/logout", status_code=200)
def logout_session(id: int, data: ValidateStudent):

    session = get_session_by_string(data.sessionString)

    if not session:
        raise HTTPException(400, "Sesión no encontrada")

    if session["alumnoId"] != id:
        raise HTTPException(400, "La sesión no pertenece a este alumno")

    invalidate_session(session["id"])

    return {"message": "Sesión cerrada correctamente"}
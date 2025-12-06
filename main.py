from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db.database import Base, engine
from routes.professors import router as professor_router
from routes.students import router as student_router

app = FastAPI(
    title="Gestión Escolar",
    description="API para gestionar alumnos y profesores en memoria",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(student_router)
app.include_router(professor_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )
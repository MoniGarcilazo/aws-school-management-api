from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from routes.professors import router as professor_router
from routes.students import router as student_router

app = FastAPI(
    title="Gestión Escolar",
    description="API para gestionar alumnos y profesores en memoria",
    version="1.0.0"
)

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
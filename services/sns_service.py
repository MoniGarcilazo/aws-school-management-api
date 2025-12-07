import boto3
import os

sns = boto3.client(
    "sns",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_REGION")
)

TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

def send_student_notification(nombres: str, apellidos: str, matricula: str, promedio: float):
    message = (
        f"Alumno: {nombres} {apellidos}\n"
        f"Matrícula: {matricula}\n"
        f"Promedio: {promedio}\n"
    )

    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject="Reporte de Calificaciones"
    )

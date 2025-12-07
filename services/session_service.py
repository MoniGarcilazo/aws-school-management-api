import uuid
import time
import secrets
from config.aws_config import sessions_table

def create_session(student_id: int):
    session_id = str(uuid.uuid4())
    now = int(time.time())

    session_string = secrets.token_hex(64)
    
    item = {
        "id": session_id,
        "fecha": now,
        "alumnoId": student_id,
        "active": True,
        "sessionString": session_string
    }

    sessions_table.put_item(Item=item)

    return session_string


def get_session_by_string(session_string: str):
    response = sessions_table.scan(
        FilterExpression="sessionString = :s",
        ExpressionAttributeValues={":s": session_string}
    )
    items = response.get("Items", [])
    return items[0] if items else None


def invalidate_session(session_id: str):
    sessions_table.update_item(
        Key={"id": session_id},
        UpdateExpression="SET active = :a",
        ExpressionAttributeValues={":a": False}
    )

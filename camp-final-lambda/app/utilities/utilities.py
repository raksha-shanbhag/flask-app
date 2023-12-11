import uuid
from datetime import datetime

def get_uuid():
    return str(uuid.uuid4())

def get_datenow_iso():
    return datetime.utcnow().isoformat()

import jwt
from datetime import datetime, timedelta

MASTER_SECRET = "Fx5$5x#45%65sjf$$djk"

def create_scoped_token(server_id: int, expire_minutes: int = 30):
    payload = {
        "server_id": server_id,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
        "scopes": ["modify:server"]
    }
    token = jwt.encode(payload, MASTER_SECRET, algorithm="HS256")
    return token

def verify_scoped_token(token: str, server_id: int):
    try:
        payload = jwt.decode(token, MASTER_SECRET, algorithms=["HS256"])
        return payload.get("server_id") == server_id
    except Exception:
        return False

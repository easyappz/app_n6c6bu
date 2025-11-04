from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def generate_jwt(user, expire_minutes: int = 60) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": exp,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # PyJWT>=2 returns str
    return token


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

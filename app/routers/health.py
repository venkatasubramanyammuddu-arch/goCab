import psycopg
import redis
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config.settings import get_settings

router = APIRouter()


def check_db() -> str:
    # Open a short-lived connection and run the cheapest possible query.
    with psycopg.connect(get_settings().database_url, connect_timeout=2) as conn:
        conn.execute("SELECT 1")
    return "ok"


def check_redis() -> str:
    client = redis.Redis.from_url(
        get_settings().redis_url, socket_connect_timeout=2, socket_timeout=2
    )
    client.ping()
    return "ok"


@router.get("/health")
def health():
    checks = {}
    for name, check in (("db", check_db), ("redis", check_redis)):
        try:
            checks[name] = check()
        except Exception as exc:
            # Report the exception type only; messages may contain connection details.
            checks[name] = f"error: {type(exc).__name__}"

    healthy = all(v == "ok" for v in checks.values())
    body = {"status": "ok" if healthy else "degraded", **checks}
    return JSONResponse(body, status_code=200 if healthy else 503)

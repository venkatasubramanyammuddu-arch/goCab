from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

router = APIRouter()


@router.get("/test")
def test():
    body = {"Mode": "testing"}
    return JSONResponse(body)


@router.get("/hello")
def hello():
    return {"message": "hi"}  # JSON, with no extra work


@router.get("/page", response_class=HTMLResponse)
def page():
    return "<h1>Hello cab app</h1>"  # the browser renders this as a page


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"

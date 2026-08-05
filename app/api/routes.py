from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def root():
    return JSONResponse(
        content = {"message": "fastapi запущен!"},
        media_type = "application/json;charset=utf-8"
    )

@router.get("/hello")
def hello():
    return JSONResponse(
        content = {"message": "fastapi приветствует!"},
        media_type = "application/json;charset=utf-8"
    )

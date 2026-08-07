from fastapi import FastAPI
from app.api.routes import router
from app.database.database import engine , Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
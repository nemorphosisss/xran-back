from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import decode_access_token

barrier_scheme = HTTPBearer()

def current_user(
        credentials: HTTPAuthorizationCredentials = Depends(barrier_scheme),
        db: Session = Depends(get_db)
) -> User:
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен доступа",
        )

    User = db.query(User).filter(User.id == user_id).first()
    if User is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return User
    
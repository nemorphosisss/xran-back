from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas import UserCreate, UserLogin
from app.models.user import User
from app.database.database import get_db
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from app.models.vault_entry import VaultEntry
from app.schemas import VaultEntryCreate, VaultEntryResponse , VaultEntryWithPassword
from app.security import encrypt_password, decrypt_password


router = APIRouter()

@router.get("/")
def root():
    return JSONResponse(
        content = {"message": "fastapi запущен!"},
        media_type = "application/json;charset=utf-8"
    )

@router.post("/register")
def register(user:UserCreate, db: Session = Depends(get_db)):

    if len (user.username) < 3:
        return JSONResponse(
            status_code = 400,
            content = {"message": "Имя пользователя должно быть не менее 3 символов!"},
            media_type = "application/json;charset=utf-8"
        )
    
    if len (user.password) < 8:
        return JSONResponse(
            status_code = 400,
            content = {"message": "Пароль должен быть не менее 8 символов!"},
            media_type = "application/json;charset=utf-8"
        )

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return JSONResponse(
            status_code = 400,
            content={"message": "Это имя пользователя уже занято!"},
            media_type="application/json;charset=utf-8"
        )
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return{
        "message": "Пользователь успешно зарегистрирован!",
        "id": new_user.id,
        "username": new_user.username
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return JSONResponse(
            status_code=401,
            content={"message": "Неверный логин или пароль!"},
            media_type="application/json;charset=utf-8"
        )

    token = create_access_token(db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }

@router.post("/vault", response_model=VaultEntryResponse, status_code = status.HTTP_201_CREATED)
def create_vault_entry(
    entry: VaultEntryCreate,
    db : Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    encrypted_password = encrypt_password(entry.password)

    new_entry = VaultEntry(
        user_id = current_user.id,
        site_name = entry.site_name,
        site_url = entry.site_url,
        login = entry.login,
        encrypted_password = encrypted_password
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@router.get("/vault", response_model=list[VaultEntryResponse])
def list_vault_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entries = db.query(VaultEntry).filter(VaultEntry.user_id == current_user.id).all()
    return entries

@router.get("/vault/{entry_id}", response_model=VaultEntryWithPassword)
def get_vault_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == current_user.id
    ).first()

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена",
        )

    
    descrypted_password = decrypt_password(entry.encrypted_password)


    return VaultEntryWithPassword(
        id = entry.id,
        site_name = entry.site_name,
        site_url = entry.site_url,
        login = entry.login,
        created_at = entry.created_at,
        password = descrypted_password,
    )
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.database import Base


class VaultEntry(Base):
    __tablename__ = "vault_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_name = Column(String, nullable=False)
    site_url = Column(String, nullable=True)
    login = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

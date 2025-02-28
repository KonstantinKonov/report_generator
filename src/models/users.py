from typing import List
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from src.database import Base


class RolesOrm(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    role: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    users: Mapped[List["UsersOrm"]] = relationship("UsersOrm", back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id}, role={self.role})"


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["RolesOrm"] = relationship("RolesOrm", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, role={self.role})"
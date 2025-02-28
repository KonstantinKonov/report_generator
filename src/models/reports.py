from datetime import datetime, date

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ReportTypesOrm(Base):
    __tablename__ = "report_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    reports: Mapped[list["ReportsOrm"]] = relationship(back_populates="type")


class ReportStatusOrm(Base):
    __tablename__ = "report_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    reports: Mapped[list["ReportsOrm"]] = relationship(back_populates="status")


class ReportsOrm(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("report_types.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("report_status.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())
    file_path: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000))  

    type: Mapped["ReportTypesOrm"] = relationship(back_populates="reports")
    status: Mapped["ReportStatusOrm"] = relationship(back_populates="reports") 
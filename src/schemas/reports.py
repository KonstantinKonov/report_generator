from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class ReportAdd(BaseModel):
    title: str
    type_id: int
    status_id: int
    created_at: datetime
    updated_at: datetime
    file_path: str
    description: str


class Report(ReportAdd):
    title: str
    type: str
    status: str
    created_at: datetime
    updated_at: datetime
    file_path: str
    description: str
from src.repository.base_repo import BaseRepo
from src.models import RolesOrm


class RolesRepo(BaseRepo):
    model = RolesOrm
    # mapper
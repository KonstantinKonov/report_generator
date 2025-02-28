from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DBDep, RoleChecker, RolesAdminDep, RolesUserDep, RolesAnalyticDep, RolesHeadAnalyticDep
from src.services import AdminService, RolesService
from src.schemas import UserWithRoleRequestAdd, UserWithRoleRequestPatch, RoleAdd, RolePatch


router = APIRouter(prefix="/admin", tags=["Admin console"])


@router.get("/users/")
async def get_all_users(
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin",]))
):
    return await AdminService(db).get_all_users()


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin",]))
):
    return await AdminService(db).get_one_or_none(user_id)


@router.post("/users")
async def add_user(
    data: UserWithRoleRequestAdd,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await AdminService(db).add_user(data)


@router.patch("/users/{user_id}")
async def edit_user(
    user_id: int,
    data: UserWithRoleRequestPatch,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await AdminService(db).edit_user(user_id, data)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await AdminService(db).delete_user(user_id)


# управление ролями
@router.get("/roles/")
async def get_roles(
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await RolesService(db).get_all_roles()


@router.post("/roles")
async def add_role(
    data: RoleAdd,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await RolesService(db).add_role(data)


@router.patch("/roles/{role_id}")
async def edit_role(
    role_id: int,
    data: RolePatch,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await RolesService(db).edit_role(role_id, data)


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    db: DBDep,
    _: bool = Depends(RoleChecker(["admin", ]))
):
    return await RolesService(db).delete_role(role_id)
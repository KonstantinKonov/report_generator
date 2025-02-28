from fastapi import APIRouter, Depends

from src.api.dependencies import DBDep, RoleChecker, RolesAdminDep, RolesUserDep, RolesAnalyticDep, RolesHeadAnalyticDep, RolesAllDep

router = APIRouter(prefix="/reports", tags="analytics actions")


# доступ к отчетам 
@router.get("/reports")
async def get_reports_all(
    db: DBDep,
    _: RolesAllDep,
):
    ...


@router.post("/reports/{report_id}")
async def get_report(
    report_id: int,
    db: DBDep,
    _: RolesAllDep,
):
    ...


@router.get("reports/export")
async def export_reports(
    report_ids: list[int],
    db: DBDep,
    _: RolesAllDep
):
    ...


@router.post("/reports")
async def add_report(
    db: DBDep,
    _: bool = Depends(RoleChecker(["analytic", "head_analytic", "admin"]))
):
    ...


@router.put("/reports/{report_id}")
async def edit_report(
    db: DBDep,
    _: bool = Depends(RoleChecker(["analytic", "head_analytic", "admin"]))
):
    ...


@router.delete("/reports/{report_id}")
async def delete_report(
    db: DBDep,
    _: bool = Depends(RoleChecker(["head_analytic", "admin"]))
):
    ...


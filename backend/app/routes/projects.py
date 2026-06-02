from fastapi import APIRouter
from services.freelancer_api import get_active_projects

router = APIRouter()

@router.get("/")
def list_projects():
    projects = get_active_projects()
    return {"projects": projects}

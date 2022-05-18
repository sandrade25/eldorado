from app.middleware.database import db_context
from app.models.user import User
from app.postgres_db import DatabaseSession
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    tags=["Users"],
)
async def user_list(
    current_user: User = Depends(get_current_active_user),
):
    # db: DatabaseSession = db_context.get()
    return {"message": "Hello World"}

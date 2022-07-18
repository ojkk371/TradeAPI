from datetime import datetime
from fastapi import APIRouter, Depends
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.database.conn import db, Base
from app.database.schema import Users

router = APIRouter()


@router.get("/")
async def index(session: Session = Depends(db.session)):
    """
    **ELB 상태 체크용 API**\n
    `:return:`
    """
    # db insert test
    # Users.create(session, auto_commit=True, name="테스트")
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
    )

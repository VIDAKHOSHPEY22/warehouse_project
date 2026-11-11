"""
api/routes/missions.py - مدیریت مأموریت/درخواست‌های توزیع
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.mission import Mission
from app.models.enums import UserRole
from app.schemas.mission import MissionCreate, MissionRead, MissionUpdate
from app.api.deps import require_roles, get_current_user

router = APIRouter(prefix="/api/missions", tags=["مأموریت‌ها / درخواست‌ها"])


@router.get("", response_model=list[MissionRead], dependencies=[Depends(get_current_user)])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).order_by(Mission.created_at.desc()).all()


@router.post("", response_model=MissionRead, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    if db.query(Mission).filter(Mission.code == payload.code).first():
        raise HTTPException(status_code=400, detail="کد مأموریت تکراری است")
    mission = Mission(**payload.model_dump())
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.patch("/{mission_id}", response_model=MissionRead,
              dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def update_mission(mission_id: int, payload: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="مأموریت یافت نشد")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(mission, key, value)
    db.commit()
    db.refresh(mission)
    return mission

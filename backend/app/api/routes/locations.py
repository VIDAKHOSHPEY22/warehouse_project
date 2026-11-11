"""
api/routes/locations.py - مدیریت مکان‌های فیزیکی انبار
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.location import Location
from app.models.enums import UserRole
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate
from app.api.deps import require_roles, get_current_user

router = APIRouter(prefix="/api/locations", tags=["مکان‌های انبار"])


@router.get("", response_model=list[LocationRead], dependencies=[Depends(get_current_user)])
def list_locations(db: Session = Depends(get_db)):
    return db.query(Location).order_by(Location.code).all()


@router.post("", response_model=LocationRead, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def create_location(payload: LocationCreate, db: Session = Depends(get_db)):
    if db.query(Location).filter(Location.code == payload.code).first():
        raise HTTPException(status_code=400, detail="کد مکان تکراری است")
    location = Location(**payload.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.patch("/{location_id}", response_model=LocationRead,
              dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))])
def update_location(location_id: int, payload: LocationUpdate, db: Session = Depends(get_db)):
    location = db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="مکان یافت نشد")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(location, key, value)
    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_roles(UserRole.ADMIN))])
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="مکان یافت نشد")
    db.delete(location)
    db.commit()

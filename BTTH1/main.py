from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

import models
from database import engine, get_db
from schemas import ParkingSlotCreate, StandardResponse, ParkingSlotResponse
from service import ParkingSlotService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def make_standard_response(status_code: int, message: str, data: any, path: str, error: str = None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now().isoformat() 
    }

# 1. API Thêm vị trí đỗ xe mới (POST)
@app.post("/parking-slots", response_model=StandardResponse, status_code=201)
def create_parking_slot(request: Request, slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    new_slot = ParkingSlotService.create_slot(db, slot)
    data_res = ParkingSlotResponse.from_orm(new_slot).dict()
    return make_standard_response(
        status_code=201,
        message="Thêm vị trí đỗ xe thành công",
        data=data_res,
        path=str(request.url.path)
    )

@app.get("/parking-slots", response_model=StandardResponse)
def get_all_parking_slots(request: Request, db: Session = Depends(get_db)):
    slots = ParkingSlotService.get_all_slots(db)
    data_res = [ParkingSlotResponse.from_orm(s).dict() for s in slots]
    return make_standard_response(
        status_code=200,
        message="Lấy danh sách vị trí đỗ xe thành công",
        data=data_res,
        path=str(request.url.path)
    )

@app.get("/parking-slots/{slot_id}", response_model=StandardResponse)
def get_parking_slot_detail(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        slot = ParkingSlotService.get_slot_by_id(db, slot_id)
        data_res = ParkingSlotResponse.from_orm(slot).dict()
        return make_standard_response(
            status_code=200,
            message="Lấy chi tiết vị trí đỗ xe thành công",
            data=data_res,
            path=str(request.url.path)
        )
    except HTTPException as ex:
        return JSONResponse(
            status_code=ex.status_code,
            content=make_standard_response(
                status_code=ex.status_code,
                message=ex.detail,
                error="Not Found" if ex.status_code == 404 else "Bad Request",
                data=None,
                path=str(request.url.path)
            )
        )
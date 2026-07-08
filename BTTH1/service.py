from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import ParkingSlotModel
from schemas import ParkingSlotCreate

class ParkingSlotService:
    
    @staticmethod
    def create_slot(db: Session, slot_data: ParkingSlotCreate):
        existing_slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.slot_code == slot_data.slot_code).first()
        if existing_slot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã vị trí đỗ xe đã tồn tại trên hệ thống"
            )
            
        db_slot = ParkingSlotModel(
            slot_code=slot_data.slot_code,
            zone_name=slot_data.zone_name,
            max_weight=slot_data.max_weight,
            is_available=slot_data.is_available
        )
        
        try:
            db.add(db_slot)
            db.commit()
            db.refresh(db_slot)
            return db_slot
        except Exception as e:
            db.rollback()  
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi hệ thống cơ sở dữ liệu: {str(e)}"
            )

    @staticmethod
    def get_all_slots(db: Session):
        return db.query(ParkingSlotModel).all()

    @staticmethod
    def get_slot_by_id(db: Session, slot_id: int):
        slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking slot not found"
            )
        return slot
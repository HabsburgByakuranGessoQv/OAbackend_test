from typing import Any, Dict, Generic, TypeVar, Union, Optional, List
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    """    
    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
    """
    def get(
        self,
        db: Session,
        id: int,
        options: Optional[List] = None
    ) -> Optional[ModelType]:
        query = db.query(self.model).filter(self.model.id == id)
        if options:
            query = query.options(*options)
        return query.first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        # 将输入转换为字典
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # 更新对象属性
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        db.commit()
        return db_obj
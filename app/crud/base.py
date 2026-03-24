from typing import TypeVar, Generic, Type, Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session, Query
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _apply_filters(self, query):
        """默认不添加任何过滤，子类可重写添加 is_deleted 等"""
        return query

    def get(self, db: Session, id: int, options: Optional[List[Any]] = None) -> Optional[ModelType]:
        query = db.query(self.model).filter(self.model.id == id)
        query = self._apply_filters(query)
        if options:
            query = query.options(*options)
        return query.first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = db.query(self.model)
        query = self._apply_filters(query)
        return query.order_by(self.model.id).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
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
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
            self,
            db: Session,
            *,
            id: Optional[int] = None,
            db_obj: Optional[ModelType] = None
    ) -> Optional[ModelType]:
        if db_obj is None and id is None:
            raise ValueError("Either id or db_obj must be provided")
        if db_obj is None:
            db_obj = self.get(db, id=id)
            if not db_obj:
                return None
        db.delete(db_obj)
        db.commit()
        return db_obj
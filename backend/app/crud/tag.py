from app.crud.base import CRUDBase
from app.models import Tag


class CRUDTag(CRUDBase):
    pass


tag_crud = CRUDTag(Tag)

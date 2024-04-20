from app.crud.base import CRUDBase
from app.models import Sleep


class CRUDSleep(CRUDBase):
    pass


sleep_crud = CRUDSleep(Sleep)

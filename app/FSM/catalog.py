from aiogram.fsm.state import State, StatesGroup

class CatalogStates(StatesGroup):
    WAITING_CATEGORY = State()
    WAITING_DRIVE_TYPE = State()
    WAITING_FUEL_TYPE = State()
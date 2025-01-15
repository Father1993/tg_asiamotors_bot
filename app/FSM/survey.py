from aiogram.fsm.state import State, StatesGroup

class SurveyStates(StatesGroup):
    WAITING_NAME = State()
    WAITING_PHONE = State()
    WAITING_BUDGET = State()
    WAITING_TIMEFRAME = State()
    WAITING_CURRENT_CAR = State()
    WAITING_FEATURES = State()
    WAITING_PURPOSE = State()
    WAITING_CONCERNS = State()
    WAITING_CONTACT_TIME = State()
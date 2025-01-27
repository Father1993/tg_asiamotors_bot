from aiogram.fsm.state import State, StatesGroup

class CalculatorStates(StatesGroup):
    """Состояния FSM для калькулятора"""
    WAITING_YEAR = State()
    WAITING_PRICE = State()
    WAITING_ENGINE = State()
    WAITING_POWER = State() 
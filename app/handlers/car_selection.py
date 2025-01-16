from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.base  import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.SELECT_CAR)
async def show_car_selection(message: Message, state: FSMContext):
    """Показать подбор автомобиля"""
    await message.answer(
        "🔍 Подбор автомобиля\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков подбора автомобиля"""
    dp.include_router(router) 
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.base import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.CALCULATOR)
async def show_calculator(message: Message, state: FSMContext):
    """Показать калькулятор стоимости"""
    await message.answer(
        "🧮 Калькулятор стоимости\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков калькулятора"""
    dp.include_router(router) 
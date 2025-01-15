from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.config import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.CATALOG)
async def show_catalog(message: Message, state: FSMContext):
    """Показать каталог автомобилей"""
    await message.answer(
        "🚗 Каталог автомобилей\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков каталога"""
    dp.include_router(router) 
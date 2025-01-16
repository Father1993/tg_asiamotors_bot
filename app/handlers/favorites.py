from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.base import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.FAVORITES)
async def show_favorites(message: Message, state: FSMContext):
    """Показать избранное"""
    await message.answer(
        "⭐️ Избранное\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков избранного"""
    dp.include_router(router) 
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.config import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.SURVEY)
async def show_survey(message: Message, state: FSMContext):
    """Показать опрос"""
    await message.answer(
        "🎁 Опрос за подарок\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков опроса"""
    dp.include_router(router) 
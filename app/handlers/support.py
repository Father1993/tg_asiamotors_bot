from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.base  import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.SUPPORT)
async def show_support(message: Message, state: FSMContext):
    """Показать поддержку"""
    await message.answer(
        "👨‍💼 Связаться с менеджером\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков поддержки"""
    dp.include_router(router) 
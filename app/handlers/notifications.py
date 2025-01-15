from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.config import KeyboardButtons as kb

router = Router()

@router.message(F.text == kb.NOTIFICATIONS)
async def show_notifications(message: Message, state: FSMContext):
    """Показать уведомления"""
    await message.answer(
        "🔔 Уведомления\n\n"
        "В разработке..."
    )

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков уведомлений"""
    dp.include_router(router) 
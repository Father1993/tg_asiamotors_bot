from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()
    await message.answer(
        "👋 Добро пожаловать в бот по подбору автомобилей!\n\n"
        "🚗 Здесь вы можете:\n"
        "• Посмотреть каталог автомобилей\n"
        "• Подобрать автомобиль по параметрам\n"
        "• Рассчитать стоимость\n"
        "• Добавить авто в избранное\n"
        "• Получать уведомления о новых предложениях\n"
        "• Участвовать в опросе и выиграть приз\n"
        "• Связаться с менеджером\n"
        "• Получить ответы на частые вопросы\n\n"
        "Выберите интересующий вас раздел в меню 👇",
        reply_markup=get_main_keyboard()
    )

def register_handlers(dp: Router) -> None:
    """Регистрация базовых обработчиков"""
    dp.include_router(router) 
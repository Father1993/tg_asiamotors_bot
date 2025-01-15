from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import re
from datetime import datetime

from app.config import KeyboardButtons as kb, ADMIN_IDS
from app.FSM.survey import SurveyStates
from app.keyboards import get_main_keyboard
logger = logging.getLogger(__name__)

router = Router()

# Клавиатуры для опроса
budget_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="До 2 млн ₽"), KeyboardButton(text="2-3 млн ₽")],
        [KeyboardButton(text="3-4 млн ₽"), KeyboardButton(text="4-5 млн ₽")],
        [KeyboardButton(text="Более 5 млн ₽")]
    ],
    resize_keyboard=True
)

timeframe_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="В ближайший месяц")],
        [KeyboardButton(text="В течение 3 месяцев")],
        [KeyboardButton(text="В течение 6 месяцев")],
        [KeyboardButton(text="Просто интересуюсь")]
    ],
    resize_keyboard=True
)

features_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Комфорт"), KeyboardButton(text="Безопасность")],
        [KeyboardButton(text="Экономичность"), KeyboardButton(text="Престиж")],
        [KeyboardButton(text="Технологичность"), KeyboardButton(text="Надежность")]
    ],
    resize_keyboard=True
)

purpose_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Для города"), KeyboardButton(text="Для семьи")],
        [KeyboardButton(text="Для бизнеса"), KeyboardButton(text="Для путешествий")],
        [KeyboardButton(text="Как второй автомобиль")]
    ],
    resize_keyboard=True
)

concerns_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Качество сборки"), KeyboardButton(text="Надёжность")],
        [KeyboardButton(text="Наличие запчастей"), KeyboardButton(text="Стоимость обслуживания")],
        [KeyboardButton(text="Остаточная стоимость"), KeyboardButton(text="Безопасность")],
        [KeyboardButton(text="Нет сомнений")]
    ],
    resize_keyboard=True
)

contact_time_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Утро (9:00-12:00)")],
        [KeyboardButton(text="День (12:00-17:00)")],
        [KeyboardButton(text="Вечер (17:00-20:00)")]
    ],
    resize_keyboard=True
)

@router.message(F.text == kb.SURVEY)
async def start_survey(message: Message, state: FSMContext):
    """Начало опроса"""
    await state.set_state(SurveyStates.WAITING_NAME)
    await message.answer(
        "🎁 Добро пожаловать в наш опрос!\n\n"
        "Пройдите короткий опрос и получите гарантированную скидку 10 000₽ "
        "на покупку автомобиля в нашей компании!\n\n"
        "👤 Как мы можем к вам обращаться? Введите ваше имя:"
    )

@router.message(SurveyStates.WAITING_NAME)
async def process_name(message: Message, state: FSMContext):
    """Обработка имени"""
    await state.update_data(name=message.text)
    await state.set_state(SurveyStates.WAITING_PHONE)
    await message.answer(
        "📱 Спасибо! Для получения скидки, оставьте ваш номер телефона:\n"
        "Формат: +7XXXXXXXXXX"
    )

@router.message(SurveyStates.WAITING_PHONE)
async def process_phone(message: Message, state: FSMContext):
    """Обработка номера телефона"""
    phone = message.text
    if not re.match(r'^\+7\d{10}$', phone):
        await message.answer("❌ Неверный формат номера. Пожалуйста, используйте формат: +7XXXXXXXXXX")
        return

    await state.update_data(phone=phone)
    await state.set_state(SurveyStates.WAITING_BUDGET)
    await message.answer(
        "💰 Какой бюджет вы рассматриваете для покупки автомобиля?",
        reply_markup=budget_kb
    )

@router.message(SurveyStates.WAITING_BUDGET)
async def process_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await state.set_state(SurveyStates.WAITING_TIMEFRAME)
    await message.answer(
        "🕒 Когда планируете приобретение автомобиля?",
        reply_markup=timeframe_kb
    )

@router.message(SurveyStates.WAITING_TIMEFRAME)
async def process_timeframe(message: Message, state: FSMContext):
    await state.update_data(timeframe=message.text)
    await state.set_state(SurveyStates.WAITING_CURRENT_CAR)
    await message.answer(
        "🚗 Какой автомобиль вы используете сейчас?\n"
        "Укажите марку и модель:"
    )

@router.message(SurveyStates.WAITING_CURRENT_CAR)
async def process_current_car(message: Message, state: FSMContext):
    await state.update_data(current_car=message.text)
    await state.set_state(SurveyStates.WAITING_FEATURES)
    await message.answer(
        "⭐️ Какие характеристики автомобиля для вас наиболее важны?",
        reply_markup=features_kb
    )

@router.message(SurveyStates.WAITING_FEATURES)
async def process_features(message: Message, state: FSMContext):
    await state.update_data(features=message.text)
    await state.set_state(SurveyStates.WAITING_PURPOSE)
    await message.answer(
        "🎯 Для каких целей вы планируете использовать новый автомобиль?",
        reply_markup=purpose_kb
    )

@router.message(SurveyStates.WAITING_PURPOSE)
async def process_purpose(message: Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await state.set_state(SurveyStates.WAITING_CONCERNS)
    await message.answer(
        "❓ Что вас больше всего беспокоит при выборе автомобиля из Китая?",
        reply_markup=concerns_kb
    )

@router.message(SurveyStates.WAITING_CONCERNS)
async def process_concerns(message: Message, state: FSMContext):
    await state.update_data(concerns=message.text)
    await state.set_state(SurveyStates.WAITING_CONTACT_TIME)
    await message.answer(
        "📞 В какое время вам удобнее получить консультацию нашего специалиста?",
        reply_markup=contact_time_kb
    )

@router.message(SurveyStates.WAITING_CONTACT_TIME)
async def process_contact_time(message: Message, state: FSMContext):
    """Завершение опроса и отправка результатов"""
    await state.update_data(contact_time=message.text)
    
    # Получаем все данные опроса
    data = await state.get_data()
    
    # Формируем уникальный код скидки
    discount_code = f"ASIA{message.from_user.id}{datetime.now().strftime('%d%m')}"
    
    # Отправляем сообщение пользователю
    await message.answer(
        f"🎉 Поздравляем! Вы успешно прошли опрос!\n\n"
        f"Ваш промокод на скидку 10 000₽: `{discount_code}`\n\n"
        f"💡 Наш менеджер свяжется с вами в указанное время: {data['contact_time']}\n\n"
        f"Спасибо за участие в опросе! Ждем вас в нашем офисе!",
        reply_markup=get_main_keyboard()
    )
    
    # Отправляем результаты администратору
    admin_message = (
        f"📊 Новый результат опроса!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"💰 Бюджет: {data['budget']}\n"
        f"🕒 Сроки покупки: {data['timeframe']}\n"
        f"🚗 Текущий автомобиль: {data['current_car']}\n"
        f"⭐️ Важные характеристики: {data['features']}\n"
        f"🎯 Цель использования: {data['purpose']}\n"
        f"❓ Сомнения/вопросы: {data['concerns']}\n"
        f"📞 Удобное время для связи: {data['contact_time']}\n"
        f"🎁 Промокод: {discount_code}"
    )
    
    # Отправляем результаты всем администраторам
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_message)
        except Exception as e:
            logger.error(f"Ошибка отправки результатов админу {admin_id}: {e}")
    
    await state.clear()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков опроса"""
    dp.include_router(router)
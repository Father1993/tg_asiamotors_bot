import asyncio
import logging
from app.bot import create_bot, create_dispatcher

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Создаем бота и диспетчер
    bot = await create_bot()
    dp = await create_dispatcher(bot)
    
    try:
        # Удаляем все обновления и запускаем бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")

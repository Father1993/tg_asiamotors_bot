import asyncio
import logging
from aiohttp import web
from app.bot import create_bot, create_dispatcher

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text='OK', status=200)

async def setup_health_check():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    return runner

async def main():
    # Создаем бота и диспетчер
    bot = await create_bot()
    dp = await create_dispatcher(bot)
    
    # Запускаем health check сервер
    health_runner = await setup_health_check()
    
    try:
        # Удаляем все обновления и запускаем бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await health_runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")

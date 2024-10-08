import asyncio
from aiohttp import web
from aiogram import Bot, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from telegram_bot import BOT
from command.basic.logger_config import logger
from command.basic.ascii import art
from command.basic.db import Database
from command.basic.instance import bot
from command.bot_action import BotCommand
from command.basic.config import BASE_WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SECRET, WEB_SERVER_HOST, WEB_SERVER_PORT

process = True
my_bot = BOT()

async def on_startup(bot: Bot) -> None:
    print(f"{art}")
    Database().create_table()
    await bot.delete_webhook()
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def on_shutdown():
    await bot.delete_webhook()

async def main():
    try:
        my_bot.dp.startup.register(on_startup)
        my_bot.dp.include_router(my_bot.router)

        command = BotCommand()
        asyncio.create_task(command.post_programmed())
        asyncio.create_task(command.send_post_link())
        
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=my_bot.dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        webhook_requests_handler.register(my_bot.app, path=WEBHOOK_PATH)

        setup_application(my_bot.app, my_bot.dp, bot=bot)

        runner = web.AppRunner(my_bot.app)
        await runner.setup()
        site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
        await site.start()
        
        asyncio.create_task(command.time_check())
        print(f"Server running at http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
        while True:
            await asyncio.sleep(3600)
    except Exception as ex:
        logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
    except KeyboardInterrupt:
        print("Interrotto dall'utente")
    finally:
        await on_shutdown()

if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

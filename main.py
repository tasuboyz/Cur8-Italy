from bot import BOT

import asyncio
from command.basic.logger_config import logger
from command.basic.ascii import art
from command.basic.db import Database
from command.basic.instance import bot
from command.user_commands import User_Commands

async def on_start():
    print(f"{art}")
    Database().create_table()

async def on_stop():
    print("Bot stoped")

async def main():
    try:       
        my_bot = BOT()
        command = User_Commands()
        await on_start()
        asyncio.create_task(command.send_post_link())
        await my_bot.dp.start_polling(bot)
    except Exception as ex:
        logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
    except KeyboardInterrupt:
        print("Interrotto dall'utente")
    finally:
        await on_stop()
        
if __name__ == '__main__':   
    asyncio.run(main())

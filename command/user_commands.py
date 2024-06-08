from .basic.user import UserInfo
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from .basic.memory import Form
import asyncio
from .basic.logger_config import logger
from datetime import datetime, timedelta
from .basic.db import Database
from .basic.chat_keyboards import Keyboard_Manager
from .basic.steem_request import Blockchain
from .basic.instance import bot
from .basic.config import admin_id, cur8_channel

class User_Commands:
    def __init__(self):
        self.db = Database()
        self.keyboards = Keyboard_Manager()
        self.steem = Blockchain()

    async def command_start_handler(self, message: Message):
            info = UserInfo(message)
            chat_id = info.chat_id
            user_id = info.user_id
            username = info.username
            try:           
                self.db.insert_user_data(user_id=user_id, username=username)
                keyboard = self.keyboards.create_start_inline_keyboard()
                await message.answer("bot started", reply_markup=keyboard)
            except Exception as ex:
                logger.error(ex, exc_info=True)
                await message.reply(str(ex))

    async def wait_username(self, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Form.set_username)
        info = UserInfo(callback_query)
        await callback_query.message.reply("Send me username:")

    async def recive_username(self, message: Message, state: FSMContext):
        await state.clear()
        info = UserInfo(message)
        user_id = info.user_id
        steem_username = message.text
        try:
            profile_info = self.steem.get_profile_info(steem_username)          
            self.db.insert_steem_username(steem_username)         
            await message.reply(f"{steem_username}: saved!")
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await message.reply(str(ex))

    async def send_post_link(self):
        while True:
            async for steem_username in self.db.steem_usernames():
                post_info = self.steem.get_steem_posts(steem_username)
                link = post_info['result'][0]['url']
                permlink = post_info['result'][0]['permlink']
                created = post_info['result'][0]['created']
                created_time = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S")
                last_post = self.db.get_user_steem_post(steem_username)
                if last_post != permlink:
                    category = post_info['result'][0]['category']
                    #url = f'https://steemit.com/{category}/@{steem_username}/{permlink}'
                    url = f'https://steemit.com{link}'
                    print(f"{steem_username}: {url}")
                    #await bot.send_message(cur8_channel, url)
                    self.db.update_steem_post_and_date(steem_username, permlink, created_time)
            await asyncio.sleep(60)
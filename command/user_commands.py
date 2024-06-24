from .basic.user import UserInfo
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated, InlineQuery
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
from .basic import inline
import json

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
            #text1, text2, text3 = self.format_message()
            self.db.insert_user_data(user_id=user_id, username=username)
            keyboard = self.keyboards.create_start_reply_keyboard()
            await message.answer(f"bot started", reply_markup=keyboard)
            # await message.answer(f"{text1}", reply_markup=keyboard)
            # await message.answer(f"{text2}")
            # await message.answer(f"{text3}")
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await message.reply(str(ex))

    async def search_community(self, message: Message, state: FSMContext):        
        await state.set_state(Form.set_community)
        keyboard = self.keyboards.search_community()
        await message.reply("Click filter community:", reply_markup=keyboard)

    async def view_selected_community(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        await state.clear()
        community = message.text
        
        keyboard = self.keyboards.view_community_post(community)
        await message.send_copy(user_id, reply_markup=keyboard)

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
        try:
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
                        await bot.send_message(cur8_channel, url)
                        self.db.update_steem_post_and_date(steem_username, permlink, created_time)
                await asyncio.sleep(60)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
            await bot.send_message(admin_id, ex)

    async def recive_web_data(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        message_id = info.message_id 
        chat_id = info.chat_id
        language_code = info.language
        data = json.loads(message.web_app_data.data) ##get data responce
        await message.answer(data)

    async def bot_added(self, chatmember: ChatMemberUpdated):
        new_members = chatmember.new_chat_member
        chat_info = chatmember.chat
        channel_id = chat_info.id
        try:
            result = await bot.get_chat_administrators(channel_id)
            for user in result:
                user_info = user.user
                if not user_info.is_bot:
                    admin_user_id = user.user.id
                    self.db.insert_user_channel(channel_id, admin_user_id)
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await bot.send_message(admin_id, ex)

    async def bot_leaved(self, chatmember: ChatMemberUpdated):
        new_members = chatmember.new_chat_member
        chat_info = chatmember.chat
        channel_id = chat_info.id
        self.db.delate_channel_id(channel_id)

    async def inline_query_handler(self, query: InlineQuery):
        await asyncio.sleep(2)
        inline_results = []
        user_id = query.from_user.id
        result = query.query
        try:
            if result.startswith('community'):
                result = result.split(':')[1]
                offset = int(query.offset or "0")
                inline_results, next_offset = inline.search_steem_community(result, offset)               
                await query.answer(inline_results, next_offset=next_offset)
            elif result.startswith('view post'):
                result = result.split(':')[1]
                offset = int(query.offset or "0")
                inline_results, next_offset = inline.view_steem_communit_post(result, offset)
                await query.answer(inline_results, next_offset=next_offset)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

    async def send_report(self):
        channel_username = '@cur8earn'
        text1, text2, text3 = self.format_message()
        await bot.send_message(channel_username, text1)
        await asyncio.sleep(1)
        await bot.send_message(channel_username, text2)
        await bot.send_message(channel_username, text3)

    async def time_check(self):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if current_time[:2] == '18':
                await self.send_report()
            await asyncio.sleep(3600)

    def format_message(self):
        steem_cur8_result = self.steem.get_steem_cur8_info()
        current_sp = steem_cur8_result['current_sp']
        steem_daily_apr = steem_cur8_result['daily_APR']
        hive_cur8_result = self.steem.get_hive_cur8_info()
        current_hp = hive_cur8_result['current_hp']
        hive_daily_apr = hive_cur8_result['daily_APR']
        current_price_result = self.steem.get_steem_hive_price()
        top_10_steem_delegator = self.steem.get_steem_top_delegators()
        top_10_hive_delegator = self.steem.get_hive_top_delegators()
        current_steem_price = current_price_result['STEEM']
        current_hive_price = current_price_result['HIVE']
        total_sp_value = current_sp * current_steem_price
        total_hp_value = current_hp * current_hive_price

        message1 = f"""
    📊 *Report Giornaliero Cur8* 📊
    ------------------------------
    🚀 *Steem*
    ▫️ *Steem Power Corrente:* **{current_sp} SP**
    ▫️ *Valore Totale SP:* **${total_sp_value:.2f}**
    ▫️ *APR Giornaliero:* **{steem_daily_apr:.2f}%**
    ▫️ *Prezzo Corrente Steem:* **${current_steem_price:.2f}**

    🚀 *Hive*
    ▫️ *Hive Power Corrente:* **{current_hp} HP**
    ▫️ *Valore Totale HP:* **${total_hp_value:.2f}**
    ▫️ *APR Giornaliero:* **{hive_daily_apr:.2f}%**
    ▫️ *Prezzo Corrente Hive:* **${current_hive_price:.2f}**
    """
        message2 = "🏆 *Top 10 Delegatori Steem*\n"
        for delegator, total_amount in top_10_steem_delegator:
            message2 += f"▫️ {delegator}: **{total_amount:.2f} HP**\n"

        message3 = "🏆 *Top 10 Delegatori Hive*\n"
        for delegator, total_amount in top_10_hive_delegator:
            message3 += f"▫️ {delegator}: **{total_amount:.2f} HP**\n"

        return message1, message2, message3


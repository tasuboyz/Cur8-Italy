from aiogram.types import Message, CallbackQuery
import asyncio
from .basic.db import Database
from .basic.chat_keyboards import Keyboard_Manager
from .basic.instance import bot
from .basic.user import UserInfo
from .basic.logger_config import logger
from .basic import instance
from .basic import config
from aiogram.fsm.context import FSMContext
from .basic.memory import Form
import json

class Admin_Commands:
    def __init__(self):
        self.example_url = 'https://github.com/tasuboyz/aiogram-bot-example'
        self.db = Database()
        self.keyboards = Keyboard_Manager()
        self.bot = instance.bot
        self.admin_id = config.admin_id

    async def admin_panel_commands(self, message: Message):
        keyboard = self.keyboards.admin_keyboards()
        await message.answer("choose commands:", reply_markup=keyboard)
        return

    async def process_callback_view_users(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        user_id = info.user_id
        question = info.user_data
        message_id = info.message_id
        try:
            results = self.db.get_all_users()
            self.write_ids(results)
            count_users = Database().count_users()
            await self.bot.delete_message(chat_id, message_id)
            await self.bot.send_message(self.admin_id, f"👤 The number of users are {count_users}")  
        except Exception as ex:
            logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")

    async def process_callback_view_steem_users(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        user_id = info.user_id
        question = info.user_data
        message_id = info.message_id
        try:
            count_users = Database().count_steem_users()
            await self.bot.delete_message(chat_id, message_id)
            await self.bot.send_message(self.admin_id, f"👤 The steem number of users are {count_users}")  
        except Exception as ex:
            logger.error(f"{ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")
    
    def write_ids(self, results):
          info = UserInfo(None)
          with open('ids.txt', 'w') as file:
            for result in results:
                # status = info.get_vip_member(result[0])
                # if status != 'member':
                file.write(str(result[0]) + '\n')

    async def clean_inactive_users(self, callback_query: CallbackQuery):       
        count = 0
        id_to_delate = []
        try:
            counter = await callback_query.message.answer(f"{count}")
            async for user_id in self.db.users_ids():
                try:
                    await self.bot.send_chat_action(user_id[0], "typing")

                    #logger.error(f"{user_id[0]} Sended! {count}")
                    
                    count += 1
                    await self.bot.edit_message_text(chat_id=self.admin_id, text=f"{count}", message_id=counter.message_id)
                except Exception as e:     
                    logger.error(f"{e}")         
                    #logger.error(f"{user_id[0]}, delated \n{e}") 
                    id_to_delate.append(user_id[0])
        finally:
            for ids in id_to_delate:
                self.db.delate_ids(ids)      
                await self.bot.send_message(self.admin_id, "Completed!")
                #logger.error(f"Completed!")        

    async def wait_document(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Send file txt:")
        await state.set_state(Form.set_repair)

    async def repair_user_id(self, message: Message, state: FSMContext):
        await state.clear()
        try:
            _, file_path = await self.image.recive_image(message, False)
            self.db.insert_all_users(file_path)
            await message.reply("Repair succesful!")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")
    
    async def recive_ads(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        await state.set_state(Form.set_ads)  
        await self.bot.send_message(self.admin_id, "Ads:")
    
    async def send_ads(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        ads = message.text
        await state.clear()
        count = 0
        #id_da_escludere = self.estrai_id("send file.txt")
        id_to_delate = []
        try:
            counter = await message.answer(f"{count}")
            async for user_id in Database().users_ids():
                #if user_id[0] in id_da_escludere:
                #    continue
                #if count == 5111:
                #    logger.error(f"Completed!")
                #    break
                try:
                    await message.send_copy(user_id[0])
                    #logger.error(f"{user_id[0]} Sended! {count}")
                    count += 1
                    if count % 100 == 0:
                        await self.bot.edit_message_text(chat_id=self.admin_id, text=f"{count}", message_id=counter.message_id)
                except Exception as e:             
                    # logger.error(f"{user_id[0]}, delated \n{e}") 
                    id_to_delate.append(user_id[0])
        finally:
            for ids in id_to_delate:
                Database().delate_ids(ids)          
            await self.bot.edit_message_text(chat_id=self.admin_id, text=f"finished!", message_id=counter.message_id)

    async def set_key(self, callback_query: CallbackQuery, state: FSMContext):
        data = callback_query.data  
        info = UserInfo(callback_query)
        admin_id = info.user_id
        admin_username = info.username
        response = data.split(':')[1]
        user_id = response.split(' ')[0]
        status = response.split(' ')[1]       
        try:
            await callback_query.message.edit_text(f"impostato da @{admin_username}")
            if status == '✅':
                keyboard = self.keyboards.account_info()
                self.db.insert_temp_user_data(user_id, None)       
                await bot.send_message(admin_id, "Invia le chiavi all'utente:", reply_markup=keyboard)
            else:
                await bot.send_message(user_id, "Your account non è stato creato")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")
            
    async def webapp_recive_keys(self, message: Message, state: FSMContext):
        user_id = self.db.get_temp_user_data()
        try:
            result = json.loads(message.web_app_data.data)
            account = result['account']
            master_key = result['master']
            active_key = result['active']
            posting_key = result['posting']
            format = (f"account: <pre language='c++'>{account}</pre>\n"
            f"master_key: <pre language='c++'>{master_key}</pre>\n"
            f"active_key: <pre language='c++'>{active_key}</pre>\n"
            f"posting_key: <pre language='c++'>{posting_key}</pre>")
            await bot.send_message(user_id, format)
            self.db.delate_temp_user(user_id)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")

    async def recive_keys(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = data[0]
        try:
            await message.send_copy(user_id)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{ex}")
        
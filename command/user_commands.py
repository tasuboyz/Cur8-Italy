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
from .basic.config import admin_id, cur8_channel, report_channel, account_creation_channel
from .basic import inline
import json
from aiogram.enums import ParseMode
from .basic.image import FileManager, FileInfo
from .basic.language import Language
from .admin_panel import Admin_Commands
from .basic.limiter import RateLimiter
import os

class User_Commands:
    def __init__(self):
        self.db = Database()
        self.keyboards = Keyboard_Manager()
        self.steem = Blockchain()
        self.image = FileManager()
        self.language = Language()
        self.admin_command = Admin_Commands()
        self.limiter = RateLimiter()

    async def command_start_handler(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        user_id = info.user_id
        username = info.username
        language_code = info.language
        first_name = info.first_name
        try:
            welcame_text = self.language.welcome_message(first_name, language_code)
            self.db.insert_user_data(user_id=user_id, username=username)
            #keyboard = self.keyboards.create_start_reply_keyboard(message)
            keyboard = self.keyboards.open_web_app()
            await message.answer(welcame_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await message.reply(str(ex))

    async def search_community(self, message: Message, state: FSMContext):        
        # await state.set_state(Form.set_community)
        info = UserInfo(message)
        language_code = info.language
        try:
            filter_text = self.language.click_filter_community(language_code)
            keyboard = self.keyboards.search_community(message)
            await message.reply(filter_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await message.reply(str(ex))

    async def view_selected_community(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        await state.clear()
        community = message.text
        await state.set_data(data=[community])
        result = self.db.get_user_account(user_id)
        if result:
            account = result[0]
            account_sub = self.steem.get_account_sub(account)
        else:
            account_sub = None        
        keyboard = self.keyboards.view_community_post(community, language_code, account_sub)
        await message.send_copy(user_id, reply_markup=keyboard)    

    async def recive_web_data(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        message_id = info.message_id 
        chat_id = info.chat_id
        language_code = info.language
        state_data = await state.get_data()     
        try:
            data = json.loads(message.web_app_data.data) ##get data responce
            if len(state_data) > 0 and 'title' in data:
                community = state_data[0] 
                result = self.db.get_user_account(user_id)
                
                title = data['title']
                body = data['description']
                tags = data['tag']
                date_time = data['dateTime']
                if result:
                    wif = result[1]
                    author = result[0]
                    if date_time == '':                        
                        result = self.steem.pubblica_post(language_code, title=title, body=body, tags=tags, wif=wif, author=author, community=community)
                        await message.answer(result)
                        await asyncio.sleep(20)
                        post_info = self.steem.get_steem_posts(author)
                        link = post_info['result'][0]['url']
                        url = f'https://steemit.com{link}'
                        vote_keyboard = self.keyboards.vote_post(link)
                        
                        channel_message = await bot.send_message(cur8_channel, url, reply_markup=vote_keyboard)
                        await asyncio.sleep(3)
                        cur8_channel_name = cur8_channel.replace('@', '')
                        await message.reply(f'https://t.me/{cur8_channel_name}/{channel_message.message_id}')
                    else:
                        self.db.insert_program_post_data(user_id, date_time, author, title, body, tags, community)
                        post_saved_message_text = self.language.post_saved_message(language_code, date_time)
                        await message.answer(post_saved_message_text)
                else:
                    set_account_text = self.language.set_account_password(language_code)
                    await message.answer(set_account_text)
            elif 'wif' in data:                
                author = data['account'].lower()
                wif = data['wif']
                result = self.steem.steem_logging(language_code, user_id, author, wif)
                account_logged_text = self.language.login_successful(language_code)
                if result == account_logged_text:
                    keyboard = self.keyboards.create_start_reply_keyboard(message)
                else:                   
                    keyboard = None
                await message.reply(result, reply_markup=keyboard)
            elif 'master' in data:
                await self.admin_command.webapp_recive_keys(message, state)
            else:
                choose_community_text = self.language.choose_community(language_code)
                keyboard = self.keyboards.search_community(message)
                await state.set_state(Form.set_community)
                await message.answer(choose_community_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await message.answer(str(ex))
            await bot.send_message(admin_id, str(ex))
        finally:
            await state.clear()

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

    async def inline_query_handler(self, query: InlineQuery, state: FSMContext):
        await asyncio.sleep(2)
        inline_results = []
        user_id = query.from_user.id
        result = query.query
        try:
            if result.startswith('community'):
                result = result.split(':')[1]               
                offset = int(query.offset or "0")
                await state.set_state(Form.set_community)
                inline_results, next_offset = inline.search_steem_community(result.strip(), offset)               
                await query.answer(inline_results, next_offset=next_offset)
            elif result.startswith('view post'):
                result = result.split(':')[1]
                offset = int(query.offset or "0")
                inline_results, next_offset = inline.view_steem_communit_post(result.strip(), offset)
                await query.answer(inline_results, next_offset=next_offset)
        except Exception as ex:
            await bot.send_message(admin_id, ex)
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)    
    
    async def recive_istruction(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        user_id = info.user_id
        language_code = info.language
        keyboard = self.keyboards.create_post(language_code)       
        send_post_text = self.language.send_post(language_code)
        try:
            await callback_query.message.answer(send_post_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def recive_image(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        try:                       
            result = self.db.get_user_account(user_id)
            if result:
                waiting_text = self.language.waiting(language_code)
                wait_message = await message.answer(waiting_text)
                download_path, file_name = await self.image.recive_image(message)
                #await self.image.check_image(download_path, message)
                file_info = FileInfo(file_name)
                extention = file_info.extention
                account = result[0]
                wif = result[1]
                link = self.steem.steem_upload_image(download_path, account, wif)
                image_url = f"{link['url']}.{extention}"
                format = f"<a href='{image_url}'>🔗 link</a> <pre language='c++'>{image_url}</pre>"
                await bot.delete_message(user_id, wait_message.message_id)
                await message.answer(format)
                os.remove(download_path)  # Elimina il file
            else:
                login_to_save_text = self.language.login_for_save_document(language_code)
                await message.reply(login_to_save_text)
        except Exception as ex:
            await bot.send_message(admin_id, ex)
            await message.answer(str(ex))
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

    async def set_language(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        set_language_text = self.language.language_setting(language_code)
        keyboard = self.keyboards.language_setting()        
        try:
            await message.reply(set_language_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def language_settend(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        user_id = info.user_id
        message_id = info.message_id
        data = info.user_data       
        try:
            language_code = data.split(':')[1].strip()
            self.db.insert_language(user_id, language_code)
            language_choosed = self.language.language_setted(language_code)
            await callback_query.message.edit_text(language_choosed)
            keyboard = self.keyboards.create_start_reply_keyboard(callback_query)
            await callback_query.message.answer("🚀🚀🚀", reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def cancel_operation(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        user_id = info.user_id
        language_code = info.language
        try:
            cancel_text = self.language.operation_deleted(language_code)
            await callback_query.message.edit_text(cancel_text)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def recive_post_link(self, message: Message):
        info = UserInfo(message)
        user_id = info.chat_id
        message_id = message.message_id
        url = message.text
        try:
            keyboard = self.keyboards.post_link(url)
            await bot.delete_message(user_id, message_id)
            await message.send_copy(user_id, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def settings_list(self, message: Message):
        info = UserInfo(message)
        user_id = info.chat_id
        language_code = info.language
        keyboard = self.keyboards.setting_list(message)
        choose_text = self.language.choose_option(language_code)      
        try:
            await message.reply(choose_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")   

    async def recive_username(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        await state.set_state(Form.set_username)
        try:
            send_me_username = self.language.send_me_username(language_code)
            await message.answer(send_me_username)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")     

    async def notify_new_account(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        username = info.username
        new_account_name = message.text
        keyboard = self.keyboards.new_account_inline(user_id, username)
        wait_for_account_text = self.language.wait_for_account(language_code)
        await state.clear()
        try:
            await message.answer(wait_for_account_text)            
            await bot.send_message(account_creation_channel, f"rispondi a @{username} account: {new_account_name}", reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")        

    async def back(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        keyboard = self.keyboards.create_start_reply_keyboard(message)
        back_text = self.language.back(language_code)
        try:
            await message.answer(back_text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}") 

    async def send_tutorial(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        url = 'https://telegra.ph/Bot-Tutorial-07-27'
        recive_url_tutorial = 'https://cdn.steemitimages.com/DQme5voqKuhNu9aJGuVRuvZwztgFRniKUcgAJS3EA6ECJNC/image.mp4'
        fromat = f"<a href='{url}'>View tutorial 👨‍🏫</a>"
        video_tutorial = f"<a href='{recive_url_tutorial}'>View tutorial 👨‍🏫</a>"
        keyboard = self.keyboards.open_copilot(language_code)
        try:
            await message.answer(fromat)
            await message.answer(video_tutorial)
            await message.answer("ask to copilot", reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}") 

    async def sub_unsub(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        user_id = info.user_id
        data = callback_query.data
        language_code = info.language
        message_id = info.message_id
        community = callback_query.message.html_text      
        try:
            if self.limiter.is_limited(user_id, message_id, max_actions=1, period=60):
                wait_sub_unsub_text = self.language.wait_sub_unsub(language_code)
                await callback_query.answer(wait_sub_unsub_text)
                return         
            result = self.db.get_user_account(user_id)
            account = result[0]
            wif = result[1]
            status = data.split(':')[1]
            account_sub = self.steem.get_account_sub(account)
            subscribed_text = self.language.subscribed_message(language_code)
            unsubscribed_text = self.language.unsubscribed_message(language_code)
            if status == 'sub':
                self.steem.subscribe_community(community, account, wif)
                await callback_query.answer(subscribed_text)
                account_sub.append(community)
            elif status == 'unsub':
                self.steem.unsubscribe_community(community, account, wif)
                await callback_query.answer(unsubscribed_text)                
                account_sub.remove(community)
            keyboard = self.keyboards.view_community_post(community, language_code, account_sub)
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def curation_vote(self, callback_query: CallbackQuery):
        data = callback_query.data
        info = UserInfo(callback_query)
        user_id = info.user_id
        result = self.db.get_user_account(user_id)
        account = result[0]
        wif = result[1]
        try:
            link = data.split(':')[1]
            permlink = link.split('@')[1]
            v = self.steem.vote_post(f"@{permlink}", account, wif)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

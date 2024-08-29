from .basic.db import Database
from aiohttp import web
from .basic.instance import bot
from .basic.steem_request import Blockchain
from .basic.image import FileManager, FileInfo
from .basic.logger_config import logger
import os
from .basic.config import admin_id
import json
from .basic.config import BASE_WEBHOOK_URL, TEST, cur8_channel
from .basic.language import Language
import asyncio
from datetime import datetime
from .basic.chat_keyboards import Keyboard_Manager

class Router_Requests:
    def __init__(self):
        self.db = Database()
        self.connected_clients = set()
        self.steem = Blockchain()
        self.image = FileManager()
        self.language = Language()
        self.keyboards = Keyboard_Manager()

    async def handle(self, request):
        return web.FileResponse('./dist/index.html')
    
    async def recive_base64_image(self, request: web.Request):
        try:
            data = await request.json()
            data = json.loads(data)
            userId = data.get('userId')
            base64_string = data.get('imageBase64')
            image_path = self.image.decode_and_save_image(base64_string)
            file_info = FileInfo(image_path)
            extention = file_info.extention
            result = self.db.get_user_account(userId)
            account = result[0]
            wif = result[1]
            link = self.steem.steem_upload_image(image_path, account, wif)
            
            os.remove(image_path)           
            if 'url' in link:
                image_url = f"{link['url']}.{extention}"
                return web.json_response(image_url)
            else:
                await bot.send_message(userId, link)
                return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
    
        except Exception as e:
            await bot.send_message(userId, str(e))
            await bot.send_message(admin_id, str(e))
            logger.error(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
    
    async def send_logged_data(self, request: web.Request):
        try:
            data = await request.json()
            userId = data.get('userId')
            result = self.db.get_user_account(userId)
            if result:
                return web.json_response({'status': 'success', 'message': 'Login effettuato'})
        except Exception as e:
            await bot.send_message(userId, str(e))
            await bot.send_message(admin_id, str(e))
            logger.error(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
        
    async def send_community_data(self, request: web.Request):
        inline_results = []
        data = await request.json()
        # data = json.loads(data)
        community_name = data.get('community')
        community = self.steem.get_steem_community(community_name)
        for result in community:
            name = result['name']
            title = result['title']
            description = result['about']
            inline_results.append(f"{name},{title}")
        return web.json_response({'status': 'success', 'message': 'Dati ricevuti con successo', 'data': inline_results})

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self.connected_clients.add(ws)
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    # Gestione dei messaggi ricevuti se necessario
                    pass
        finally:
            self.connected_clients.remove(ws)
        
        return ws

    async def handle_post(self, request: web.Request):
        try:
            data = await request.json()
            data = json.loads(data)
            userId = data.get('userId')
            title = data.get('title')
            body = data.get('description')
            tags = data.get('tag')
            dateTime = data.get('dateTime')
            communityId = data.get('communityId')
            result = self.db.get_user_account(userId)
            wif = result[1]
            author = result[0]
            language_code = self.db.get_language_code(userId)

            # Check if dateTime is earlier than the current time
            if dateTime and datetime.fromisoformat(dateTime) < datetime.now():
                date_time_error_message = self.language.date_time_error_message(language_code)
                await bot.send_message(userId, date_time_error_message)
                return web.json_response({'status': 'error', 'message': 'dateTime cannot be earlier than the current time'}, status=399)

            if dateTime == '':      
                if TEST:                  
                    text = f"Title: {title}, Description: {body}, Tag: {tags}, DateTime: {dateTime}, communityId: {communityId}"
                    await bot.send_message(userId, text)
                else:
                    result = self.steem.pubblica_post(language_code, title=title, body=body, tags=tags, wif=wif, author=author, community=communityId)
                    await bot.send_message(userId, result)
                    await asyncio.sleep(20)
                    post_info = self.steem.get_steem_posts(author)
                    link = post_info['result'][0]['url']
                    url = f'https://steemit.com{link}'
                    # vote_keyboard = self.keyboards.vote_post(link)
                    vote_keyboard = None
                    
                    channel_message = await bot.send_message(cur8_channel, url, reply_markup=vote_keyboard)
                    await asyncio.sleep(3)
                    cur8_channel_name = cur8_channel.replace('@', '')
                    await bot.send_message(userId, f'https://t.me/{cur8_channel_name}/{channel_message.message_id}')
            else:
                self.db.insert_program_post_data(userId, dateTime, author, title, body, tags, communityId)
                post_saved_message_text = self.language.post_saved_message(language_code, dateTime)
                await bot.send_message(userId, post_saved_message_text)               
            return web.json_response({'status': 'success', 'message': 'Dati ricevuti con successo'})
        except Exception as e:
            print(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)

    async def handle_login(self, request: web.Request):
        try:
            data = await request.json()
            data = json.loads(data)
            userId = data.get('userId')
            account = data.get('account')
            wif = data.get('wif')
            language_code = self.db.get_language_code(userId)
            if language_code == None:
                language_code = 'en'
            
            result = self.steem.steem_logging(language_code, userId, account, wif)
            account_logged_text = self.language.login_successful(language_code)
            if result == account_logged_text:
                self.db.insert_user_account(userId, account, wif)
                text = f"account: {account}, wif: {wif}"
                await bot.send_message(userId, result)
                return web.json_response({'status': 'success', 'message': 'Login effettuato con successo'})
            else:
                await bot.send_message(userId, result)
                return web.json_response({'status': 'error', 'message': 'Login fallito'}, status=401)
        except Exception as e:
            print(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
    
    def get_assets_url(self, request: web.Request):
        assets_url = os.getenv(BASE_WEBHOOK_URL, '/assets/')
        return web.json_response({'assets_url': BASE_WEBHOOK_URL})
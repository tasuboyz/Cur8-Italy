from .basic.db import Database
from aiohttp import web
from .basic.instance import bot
from .basic.steem_request import Blockchain
from .basic.image import FileManager, FileInfo
from .basic.logger_config import logger
import os

class Router_Requests:
    def __init__(self):
        self.db = Database()
        self.connected_clients = set()
        self.steem = Blockchain()
        self.image = FileManager()

    async def handle(self, request):
        return web.FileResponse('./dist/index.html')
    
    async def recive_base64_image(self, request: web.Request):
        try:
            data = await request.json()
            userId = data.get('userId')
            base64_string = data.get('image')
            image_path = self.image.decode_and_save_image(base64_string)
            file_info = FileInfo(image_path)
            extention = file_info.extention
            result = self.db.get_user_account(userId)
            account = result[0]
            wif = result[1]
            link = self.steem.steem_upload_image(image_path, account, wif)
            image_url = f"{link['url']}.{extention}"
            os.remove(image_path)
            return web.json_response(image_url)
        except Exception as e:
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
            logger.error(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
        
    async def send_community_data(self, request: web.Request):
        inline_results = []
        community = self.steem.get_steem_community()
        for result in community:
            name = result['name']
            title = result['title']
            description = result['about']
            inline_results.append(f"{name},{title}")
        if self.connected_clients:
            for client in self.connected_clients:
                await client.send_json(inline_results)
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
            userId = data.get('userId')
            title = data.get('title')
            description = data.get('description')
            tag = data.get('tag')
            dateTime = data.get('dateTime')
            
            text = f"Title: {title}, Description: {description}, Tag: {tag}, DateTime: {dateTime}"
            await bot.send_message(userId, text)
            #print(f"user_id: {userId}, Title: {title}, Description: {description}, Tag: {tag}, DateTime: {dateTime}")
            
            return web.json_response({'status': 'success', 'message': 'Dati ricevuti con successo'})
        except Exception as e:
            print(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)

    async def handle_login(self, request: web.Request):
        try:
            data = await request.json()
            userId = data.get('userId')
            account = data.get('account')
            wif = data.get('wif')
            language_code = self.db.get_language_code(userId)
            if language_code == None:
                language_code = 'en'
            
            result = self.steem.steem_logging(language_code, userId, account, wif)
            self.db.insert_user_account(userId, account, wif)
            text = f"account: {account}, wif: {wif}"
            await bot.send_message(userId, result)

            return web.json_response({'status': 'success', 'message': 'Login effettuato con successo'})
        except Exception as e:
            print(f"Errore durante la gestione della richiesta POST: {e}")
            return web.json_response({'status': 'error', 'message': 'Errore durante la gestione della richiesta POST'}, status=500)
        
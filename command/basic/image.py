import os
import base64
from io import BytesIO
import uuid
import glob
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from .logger_config import logger
from . import instance
from . import config
import requests
from .user import UserInfo
from PIL import Image
from .language import Language
from . import process

class FileManager:
    def __init__(self):
        self.bot = instance.bot
        self.admin_id = config.admin_id
        self.lang = Language()
        self.directory_path = f"UserImage"

    def check_file_exists(self, file_path):
        while os.path.exists(file_path):
            file_path = file_path
        return file_path

    async def recive_image(self, message: Message, is_gif=False):
        chat_id = message.chat.id
        info = UserInfo(message)
        language_code = info.language
        try:
            if message.document or message.photo or message.animation or message.video:
                if message.video:
                    file = message.video
                elif message.animation:
                    file = message.animation
                    is_gif = True  # Imposta is_gif su True se il file è un'animazione
                else:
                    file = message.document or message.photo[-1]
                file_info = await self.bot.get_file(file.file_id)
                file_path = file_info.file_path                

                uid = uuid.uuid4()               
                file_extension = file_path.split(".")[-1]    
                file_name = f"{uid}.{file_extension}"  

                if not os.path.exists(self.directory_path):
                    os.makedirs(self.directory_path)

                download_path = os.path.join(self.directory_path, file_name)
                file_path = self.check_file_exists(file_path)

                await self.bot.download_file(file_path, download_path)
                max_size = 0.4
                if is_gif: 
                    file_extension = file_path.split(".")[-1]
                    if file_extension == 'mp4':
                        file_size = os.path.getsize(download_path) / (1024 * 1024)  # Dimensione del file in MB:
                        if file_size > 0.1:  # Se la dimensione del file è superiore a 4 MB
                            os.remove(download_path)  # Elimina il file
                            max_size_text = self.lang.gif_size_exceeded(language_code, max_size)
                            return max_size_text, None
                        await process.process_convert_mp4(download_path) # Converte il file in gif
                        file_name = os.path.splitext(file_name)[0] + '.gif'
                        download_path = r"UserImage/"f"{file_name}"

                return download_path, file_name
            return None
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{chat_id}:{ex}")              

    def remove_file_if_exists(self, file):    
        for file in glob.glob(file + ".*"):
            if os.path.exists(file):
                os.remove(file)     

    async def check_image(self, file_name, message: Message):
        info = UserInfo(message)
        language_code = info.language
        file_not_valid = self.lang.file_not_valid(language_code)
        try:
            Image.open(file_name)
        except IOError:
            await message.reply(file_not_valid)                    
            os.remove(file_name)
            return True

    def imgur_upload(self, download_path):
        file_info = FileInfo(download_path)
        file_name = file_info.nome_completo
        extention = file_info.extention
        url = "https://api.imgur.com/3/image"
        payload={'type': 'image'}
        files=[
        ('image',(f'{file_name}.{extention}',open(f'{download_path}','rb'),f'image/{extention}'))
        ]
        headers = {
        'Authorization': 'Client-ID {{454d4868a5293d3}}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            data = response.json()
            link = data['link']
            return link
        else:
            raise Exception(response.reason)
        
    def decode_and_save_image(self, base64_string: str):
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        image_data = base64.b64decode(base64_string)
        image = BytesIO(image_data)
        img = Image.open(image)
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
        image_name = self.directory_path + r"/" + f"{uuid.uuid4()}.png"
        img.save(image_name)
        return image_name
    
class FileInfo: # crea una classe per gestire i colori e le impostazioni del QR
    def __init__(self, file_name):
        self.nome_completo = os.path.basename(file_name).split(".")[0]
        self.percorso = os.path.dirname(os.path.abspath(file_name)) #visualizza percorso file
        self.file = file_name.split(".")[0]
        self.extention = file_name.split(".")[-1]
            

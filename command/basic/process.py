from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

import asyncio 

from multiprocessing import Process
import os
from moviepy.editor import VideoFileClip

async def process_convert_mp4(file_name):
    convert_process = Process(target=convert_mp4, args=(file_name,))
    convert_process.start()
    while convert_process.is_alive():
        await asyncio.sleep(1)
    
def convert_mp4(file_mp4):
    clip = VideoFileClip(file_mp4)
    file_gif = os.path.splitext(file_mp4)[0] + '.gif'
    clip.write_gif(file_gif)
    os.remove(file_mp4)
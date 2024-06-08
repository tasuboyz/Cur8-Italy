from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from command.admin_panel import Admin_Commands
from command.user_commands import User_Commands

import asyncio
from datetime import datetime
from command.basic.memory import Form


class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.admin_command = Admin_Commands()
        self.command = User_Commands()
        
        #command
        self.dp.message(CommandStart())(self.command.command_start_handler)   
        self.dp.message(Command('user'))(self.admin_command.admin_panel_commands)  
        self.dp.callback_query(F.data == "users")(self.admin_command.process_callback_view_users) 
        self.dp.callback_query(F.data == "steem_user")(self.admin_command.process_callback_view_steem_users) 
        self.dp.callback_query(F.data == "clean")(self.admin_command.clean_inactive_users) 
        self.dp.callback_query(lambda c: c.data == 'ads')(self.admin_command.recive_ads)
        self.dp.callback_query(F.data == "save_steem_username")(self.command.wait_username) 
        self.dp.message(Form.set_ads)(self.admin_command.send_ads)
        self.dp.message(Form.set_username, F.text)(self.command.recive_username)
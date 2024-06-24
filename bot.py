from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types

from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN
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
        self.dp.message(F.web_app_data)(self.command.recive_web_data)
        
        #serch community
        self.dp.inline_query()(self.command.inline_query_handler)
        self.dp.message(F.text == 'Search community')(self.command.search_community)
        self.dp.message(Form.set_community, F.text)(self.command.view_selected_community)

        #manage channel
        self.dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_ADMIN))(self.command.bot_added)
        self.dp.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))(self.command.bot_leaved)

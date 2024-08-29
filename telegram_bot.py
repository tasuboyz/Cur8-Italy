from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types

from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN
from command.admin_panel import Admin_Commands
from command.user_commands import User_Commands

import asyncio
from datetime import datetime
from command.basic.memory import Form
from command.basic.language import Language
from command.router_requests import Router_Requests
from aiohttp import web
from command.basic.config import BASE_WEBHOOK_URL
import os
from command.basic import config

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.admin_command = Admin_Commands()
        self.command = User_Commands()
        self.language = Language()
        self.router = Router()
        self.app = web.Application(client_max_size=1024**2*10) 
        self.request_hendle = Router_Requests()
        self.assets_url = os.getenv(config.url_ngrok, '/assets/')     

        #app route
        self.app.router.add_get('/', self.request_hendle.handle)
        self.app.router.add_get('/post', self.request_hendle.handle)
        self.app.router.add_get('/community-page', self.request_hendle.handle)
        self.app.router.add_static(prefix=self.assets_url, path='./dist/assets', name='assets')
        self.app.router.add_get('/config', self.request_hendle.get_assets_url)
        self.app.router.add_post('/post', self.request_hendle.handle_post)
        self.app.router.add_post('/image', self.request_hendle.recive_base64_image)
        self.app.router.add_post('/logged', self.request_hendle.send_logged_data)
        self.app.router.add_post('/login', self.request_hendle.handle_login)
        self.app.router.add_post('/community', self.request_hendle.send_community_data)
        self.app.router.add_get('/ws', self.request_hendle.websocket_handler)

        #admin command
        self.router.message(Command('user'))(self.admin_command.admin_panel_commands)  
        self.router.callback_query(F.data == "users")(self.admin_command.process_callback_view_users) 
        self.router.callback_query(F.data == "steem_user")(self.admin_command.process_callback_view_steem_users) 
        self.router.callback_query(F.data == "clean")(self.admin_command.clean_inactive_users) 
        self.router.callback_query(lambda c: c.data == 'ads')(self.admin_command.recive_ads)
        self.router.message(Form.set_ads)(self.admin_command.send_ads)
        self.router.message(Form.set_username)(self.command.notify_new_account)
        self.router.callback_query(F.data.startswith('respond'))(self.admin_command.set_key)       
        self.router.message(Form.set_keys, F.text)(self.admin_command.recive_keys)
        
        self.router.message(Form.set_keys, F.web_app_data)(self.admin_command.webapp_recive_keys)
        
        #command
        self.router.message(CommandStart())(self.command.command_start_handler)   
        self.router.message(Command('help'))(self.command.send_tutorial)
        self.router.callback_query(lambda c: c.data == 'instruction')(self.command.recive_istruction)       
        self.router.message(F.web_app_data)(self.command.recive_web_data)
        self.router.message(F.photo | F.animation | F.video)(self.command.recive_image)
        self.router.callback_query(F.data.startswith('community'))(self.command.sub_unsub)
        
        self.router.callback_query(F.data == 'cancel')(self.command.cancel_operation)
        self.router.callback_query(F.data.startswith('code'))(self.command.language_settend)
        self.router.message(F.text.startswith('https'))(self.command.recive_post_link)
        self.router.callback_query(F.data.startswith('vote'))(self.command.curation_vote)

        #reply command
        self.router.message(F.text.in_(self.language.get_language_list()))(self.command.set_language)
        self.router.message(F.text.in_(self.language.get_setting_list()))(self.command.settings_list)
        self.router.message(F.text.in_(self.language.get_create_account_list()))(self.command.recive_username)
        self.router.message(F.text.in_(self.language.get_back_list()))(self.command.back)

        #serch community
        self.router.inline_query()(self.command.inline_query_handler)
        self.router.message(F.text.in_(self.language.get_community_search_list()))(self.command.search_community)
        self.router.message(F.text.startswith('hive'))(self.command.view_selected_community)

        #manage channel
        self.router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_ADMIN))(self.command.bot_added)
        self.router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))(self.command.bot_leaved)       
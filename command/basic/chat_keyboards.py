from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import os
from .user import UserInfo
from aiogram import Bot

class Keyboard_Manager:
    def __init__(self):
        self.postpage_url = 'https://tasuboyz.github.io/Posting-Web-App/'

    def search_community(self, message=None):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="Search community", switch_inline_query_current_chat="community:")])
        # keyboard.append([InlineKeyboardButton(text=text, web_app=WebAppInfo(url=self.example_url))])
        # keyboard.append([InlineKeyboardButton(text=text, url=self.example_url)])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def admin_keyboards(self, message=None):
        keyboard = []
        text = "Open Link"
        keyboard.append([InlineKeyboardButton(text="View Users", callback_data="users")])
        keyboard.append([InlineKeyboardButton(text="View Steem Users", callback_data="steem_user")])
        keyboard.append([InlineKeyboardButton(text="Send Ads", callback_data="ads")])
        keyboard.append([InlineKeyboardButton(text="Clean Users", callback_data="clean")])
        keyboard.append([InlineKeyboardButton(text="Save steem username", callback_data="save_steem_username")])
        keyboard.append([InlineKeyboardButton(text="view channel", callback_data="view channel")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    async def channel_list(self, channel_ids, bot: Bot):
        keyboard = []
        text = "Open Link"
        for channel_id in channel_ids:
            result = await bot.get_chat(channel_id)
            keyboard.append([InlineKeyboardButton(text=channel_id, callback_data=f"channel:{channel_id}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def create_start_reply_keyboard(self, message=None):
        keyboard = []
        text = "Open Interface"
        keyboard.append([KeyboardButton(text=text, web_app=WebAppInfo(url=self.postpage_url))])
        keyboard.append([KeyboardButton(text="Search community")])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard
    
    def view_community_post(self, community):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="View community post", switch_inline_query_current_chat=f"view post:{community}")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
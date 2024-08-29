from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import os
from .user import UserInfo
from aiogram import Bot
from .db import Database
from .language import Language
from .config import url_ngrok

class Keyboard_Manager:
    def __init__(self):
        self.db = Database()
        #self.postpage_url = 'https://tasuboyz.github.io/Posting-Web-App/'
        self.postpage_url = url_ngrok
        self.loginpage_url = 'https://tasuboyz.github.io/login-page/'      
        self.SignIn_url = 'https://tasuboyz.github.io/Sign-In/'
        self.Account_Set_Url = 'https://tasuboyz.github.io/Account-Info/'
        self.language = Language()

    def search_community(self, message=None):
        info = UserInfo(message)
        language_code = info.language
        keyboard = []
        search_community_text = self.language.search_community(language_code)
        keyboard.append([InlineKeyboardButton(text=search_community_text, switch_inline_query_current_chat="community: ")])
        # keyboard.append([InlineKeyboardButton(text=text, web_app=WebAppInfo(url=self.example_url))])
        # keyboard.append([InlineKeyboardButton(text=text, url=self.example_url)])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def post_link(self, url):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="link", web_app=WebAppInfo(url=url))])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def admin_keyboards(self, message=None):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="View Users", callback_data="users")])
        keyboard.append([InlineKeyboardButton(text="View Steem Users", callback_data="steem_user")])
        keyboard.append([InlineKeyboardButton(text="Send Ads", callback_data="ads")])
        keyboard.append([InlineKeyboardButton(text="Clean Users", callback_data="clean")])
        keyboard.append([InlineKeyboardButton(text="Save steem username", callback_data="save_steem_username")])
        keyboard.append([InlineKeyboardButton(text="view channel", callback_data="view channel")])
        keyboard.append([InlineKeyboardButton(text="Cancel ❌", callback_data="cancel")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    async def channel_list(self, channel_ids, bot: Bot):
        keyboard = []
        for channel_id in channel_ids:
            result = await bot.get_chat(channel_id)
            keyboard.append([InlineKeyboardButton(text=channel_id, callback_data=f"channel:{channel_id}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def create_start_reply_keyboard(self, user_id=None, language_code=None):
        keyboard = []
        # info = UserInfo(message)
        # user_id = info.user_id
        # language_code = info.language
        set_setting_text = self.language.setting(language_code)
        ask_copilot_text= self.language.ask_copilot(language_code)
        steemit_query_copilot_text = self.language.steemit_query_copilot(language_code)  
        
        search_community_text = self.language.search_community(language_code)
        login_text = self.language.login_text(language_code)
        
        send_post_text = self.language.send_post(language_code)
        result = self.db.get_user_account(user_id)
        if result:
            keyboard.append([KeyboardButton(text=send_post_text, web_app=WebAppInfo(url=self.postpage_url))])
        else:
            keyboard.append([KeyboardButton(text=login_text, web_app=WebAppInfo(url=self.SignIn_url))])
        keyboard.append([KeyboardButton(text=search_community_text)])
        keyboard.append([KeyboardButton(text=set_setting_text), KeyboardButton(text=ask_copilot_text, web_app=WebAppInfo(url=steemit_query_copilot_text))])
        #keyboard.append([KeyboardButton(text=ask_copilot_text, web_app=WebAppInfo(url=steemit_query_copilot_text))])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard
    
    def create_post(self, language_code):
        keyboard = []
        send_post_text = self.language.send_post(language_code)
        keyboard.append([KeyboardButton(text=send_post_text, web_app=WebAppInfo(url=self.postpage_url))])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard

    def setting_list(self, data):
        keyboard = []
        info = UserInfo(data)
        user_id = info.chat_id
        language_code = info.language
        back_text = self.language.back(language_code)
        change_account_text = self.language.change_account(language_code)
        set_lang_text = self.language.language_setting(language_code)
        create_account_text = self.language.create_account(language_code)
        result = self.db.get_user_account(user_id)  
        if result:  
            username = result[0]                        
            url = f'https://steemit.com/@{username}'
            keyboard.append([KeyboardButton(text="User Info ℹ️", web_app=WebAppInfo(url=url))])
        keyboard.append([KeyboardButton(text=change_account_text, web_app=WebAppInfo(url=self.SignIn_url)), KeyboardButton(text=create_account_text)])
        keyboard.append([KeyboardButton(text=set_lang_text)])
        keyboard.append([KeyboardButton(text=back_text)])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard

    def view_community_post(self, community, language_code, username_sub=[]):
        community_post_text = self.language.view_community_post(language_code)
        public_post_text = self.language.public_post_on_community(language_code)
        unsubscribe_text = self.language.unsubscribe_message(language_code)
        subscribe_text = self.language.subscribe_message(language_code)
        keyboard = []
        if username_sub:
            if community in username_sub:
                keyboard.append([InlineKeyboardButton(text=unsubscribe_text, callback_data="community:unsub")])
            else:
                keyboard.append([InlineKeyboardButton(text=subscribe_text, callback_data="community:sub")])
        keyboard.append([InlineKeyboardButton(text=community_post_text, switch_inline_query_current_chat=f"view post:{community}")])
        keyboard.append([InlineKeyboardButton(text=public_post_text, callback_data="instruction")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def language_setting(self):
        keyboard_buttons = []
        keyboard_buttons.append([InlineKeyboardButton(text="Italiano 🇮🇹", callback_data="code:it"),
                                 InlineKeyboardButton(text="Spanish 🇪🇦", callback_data="code:es"),
                                 InlineKeyboardButton(text="भारतीय 🇮🇳", callback_data="code:hi")])
        keyboard_buttons.append([InlineKeyboardButton(text="English 🇬🇧", callback_data="code:en"),
                                 InlineKeyboardButton(text="Français 🇫🇷", callback_data="code:fr"),
                                 InlineKeyboardButton(text="Deutsch 🇩🇪", callback_data="code:de")])
        keyboard_buttons.append([InlineKeyboardButton(text="Русский 🇷🇺", callback_data="code:ru"),
                                 InlineKeyboardButton(text="Українська 🇺🇦", callback_data="code:uk"),
                                 InlineKeyboardButton(text="中文 🇨🇳", callback_data="code:zh")])
        keyboard_buttons.append([InlineKeyboardButton(text="العربية🇸🇦", callback_data="code:ar")])
        keyboard_buttons.append([InlineKeyboardButton(text="Cancel ❌", callback_data="cancel")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard
    
    def new_account_inline(self, user_id, username):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text=f"rispondi a:{username},{user_id}", callback_data=f"respond:{user_id} ✅")])
        keyboard.append([InlineKeyboardButton(text=f"non approvare ❌", callback_data=f"respond:{user_id} ❌")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def account_info(self):
        keyboard = []
        keyboard.append([KeyboardButton(text="Invia Account Creato", web_app=WebAppInfo(url=self.Account_Set_Url))])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
        return keyboard
    
    def open_copilot(self, language_code):
        keyboard = []
        ask_copilot_text= self.language.ask_copilot(language_code)
        steemit_query_copilot_text = self.language.steemit_query_copilot(language_code)  
        keyboard.append([InlineKeyboardButton(text=ask_copilot_text, web_app=WebAppInfo(url=steemit_query_copilot_text))])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    def vote_post(self, permlink):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text=f"❤️", callback_data=f"vote:{permlink}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def open_web_app(self):
        keyboard = []
        keyboard.append([InlineKeyboardButton(text="Open", web_app=WebAppInfo(url=self.postpage_url))])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
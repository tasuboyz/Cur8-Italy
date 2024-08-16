from .basic.db import Database
from .basic.chat_keyboards import Keyboard_Manager
from .basic.instance import bot
from .basic.config import admin_id, cur8_channel, report_channel
from .basic.language import Language
from aiogram.enums import ParseMode
import asyncio
from datetime import datetime
from .basic.steem_request import Blockchain
from .basic.logger_config import logger

class BotCommand:
    def __init__(self):
        self.db = Database()
        self.keyboards = Keyboard_Manager()
        self.steem = Blockchain()

    async def send_post_link(self):
        try:
            while True:
                async for steem_username in self.db.steem_usernames():
                    post_info = self.steem.get_steem_posts(steem_username)
                    link = post_info['result'][0]['url']
                    permlink = post_info['result'][0]['permlink']
                    created = post_info['result'][0]['created']
                    created_time = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S")
                    last_post = self.db.get_user_steem_post(steem_username)
                    if last_post != permlink:
                        category = post_info['result'][0]['category']
                        #url = f'https://steemit.com/{category}/@{steem_username}/{permlink}'
                        url = f'https://steemit.com{link}'
                        await bot.send_message(cur8_channel, url)
                        self.db.update_steem_post_and_date(steem_username, permlink, created_time)
                await asyncio.sleep(60)
        except Exception as ex:
            logger.error(ex, exc_info=True)
            await bot.send_message(admin_id, str(ex))

    async def send_report(self):                
        text1, text2, text3 = self.format_message()
        await bot.send_message(report_channel, text1, parse_mode=ParseMode.MARKDOWN_V2)
        await asyncio.sleep(1)
        await bot.send_message(report_channel, text2, parse_mode=ParseMode.MARKDOWN_V2)
        await bot.send_message(report_channel, text3, parse_mode=ParseMode.MARKDOWN_V2)

    async def time_check(self):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if current_time[:2] == '17':
                await self.send_report()
            await asyncio.sleep(3600)

    def format_message(self):
        steem_cur8_result = self.steem.get_steem_cur8_info()
        current_sp = steem_cur8_result['current_sp']
        steem_daily_apr = steem_cur8_result['daily_APR']
        hive_cur8_result = self.steem.get_hive_cur8_info()
        current_hp = hive_cur8_result['current_hp']
        hive_daily_apr = hive_cur8_result['daily_APR']
        current_price_result = self.steem.get_steem_hive_price()
        top_10_steem_delegator = self.steem.get_steem_top_delegators()
        top_10_hive_delegator = self.steem.get_hive_top_delegators()
        current_steem_price = current_price_result['STEEM']
        current_hive_price = current_price_result['HIVE']
        total_sp_value = current_sp * current_steem_price
        total_hp_value = current_hp * current_hive_price

        old_data = self.db.get_blockchain_data()
        if old_data:
            #old_data = old_data[0]
            old_hp = float((str(old_data['current_hp'])).replace(',', '.'))
            old_hive_price = float(str(old_data['current_hive_price']).replace(',', '.'))
            old_sp = float((str(old_data['current_sp'])).replace(',', '.'))
            old_steem_price = float(str(old_data['current_steem_price']).replace(',', '.'))
            old_steem_daily_apr = old_data['steem_daily_apr']
            old_hive_daily_apr = old_data['hive_daily_apr']
            steem_price_change = ((current_steem_price - old_steem_price) / old_steem_price) * 100
            sp_change = ((current_sp - old_sp) / old_sp) * 100
            hive_price_change = ((current_hive_price - old_hive_price) / old_hive_price) * 100
            hp_change = ((current_hp - old_hp) / old_hp) * 100
            steem_daily_apr_diff = steem_daily_apr - float(str(old_steem_daily_apr).replace(',', '.'))
            hive_daily_apr_diff = hive_daily_apr - float(str(old_hive_daily_apr).replace(',', '.'))
        else:
            steem_price_change = 0
            sp_change = 0
            hive_price_change = 0
            hp_change = 0
            steem_daily_apr_diff = 0
            hive_daily_apr_diff = 0

        current_sp = str(current_sp).replace('.', ',')
        total_sp_value = f"{total_sp_value:.3f}".replace('.', ',')
        steem_daily_apr = f"{steem_daily_apr:.3f}".replace('.', ',')
        current_steem_price = f"{current_steem_price:.3f}".replace('.', ',')
        current_hp = str(current_hp).replace('.', ',')
        total_hp_value = f"{total_hp_value:.3f}".replace('.', ',')
        hive_daily_apr = f"{hive_daily_apr:.3f}".replace('.', ',')
        current_hive_price = f"{current_hive_price:.3f}".replace('.', ',')    

        steem_symbol = '📈' if steem_price_change > 0 else '📉'
        hive_symbol = '📈' if hive_price_change > 0 else '📉'
        sp_symbol = '📈' if sp_change > 0 else '📉'
        hp_symbol = '📈' if hp_change > 0 else '📉'
        hive_daily_symbol = '📈' if hive_daily_apr_diff > 0 else '📉'
        steem_daily_symbol = '📈' if steem_daily_apr_diff > 0 else '📉'

        steem_price_change = f"{steem_price_change:.2f}".replace('-', '\\-').replace('.', ',')
        hive_price_change = f"{hive_price_change:.2f}".replace('-', '\\-').replace('.', ',')
        message1 = f"""
        📊 *Cur8 Daily Report* 📊
        \\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-
🐳 *Steem* 💲*{current_steem_price} \\({steem_price_change}% {steem_symbol}\\)*
▫️ **Steem Power live\\:** {sp_symbol} *{current_sp}* SP
▫️ **Value Tot SP:\\:**💰 *{total_sp_value}*$
▫️ **APR daily\\:** {steem_daily_symbol} *{steem_daily_apr}*%

🏴‍☠️ *Hive* 💲 *{current_hive_price} \\({hive_price_change}% {hive_symbol}\\)*
▫️ **Hive Power live\\:** {hp_symbol} *{current_hp}* HP
▫️ **Valore Tot HP\\:** 💰 *{total_hp_value}*$
▫️ **APR daily\\:** {hive_daily_symbol} *{hive_daily_apr}*%
"""
        message2 = "🏆 *Top 10 Steem Delegator*\n"
        for delegator, total_amount in top_10_steem_delegator:
            total_amount = f"{total_amount:.3f}".replace('.', ',')
            delegator = f"{delegator}".replace('.', '\\.')
            message2 += f"▫️ **{delegator}\\:** 🟢 *{total_amount}* SP\n"

        message3 = "🏆 *Top 10 Hive Delegator*\n"
        for delegator, total_amount in top_10_hive_delegator:
            total_amount = f"{total_amount:.3f}".replace('.', ',')
            delegator = f"{delegator}".replace('.', '\\.')
            message3 += f"▫️ **{delegator}\\:** 🟢 *{total_amount}* HP\n"

        data = {
        'current_steem_price': current_steem_price,
        'current_sp': current_sp,
        'total_sp_value': total_sp_value,
        'steem_daily_apr': steem_daily_apr,
        'current_hive_price': current_hive_price,
        'current_hp': current_hp,
        'total_hp_value': total_hp_value,
        'hive_daily_apr': hive_daily_apr}

        self.db.delete_all_blockchain_data()
        self.db.insert_blockchain_data(data)
        return message1, message2, message3
    
    async def post_programmed(self):
        while True:
            now = datetime.now().strftime("%Y-%m-%dT%H:%M")
            post_info = self.db.get_program_post_data(now)
            if post_info:
                user_id = post_info[0]
                steem_info = self.db.get_user_account(user_id)
                wif = steem_info[1]
                author = post_info[2]
                title = post_info[3]
                body = post_info[4]
                tags = post_info[5]
                community = post_info[6]
                language_code = self.db.get_language_code(user_id)
                result = self.steem.pubblica_post(language_code, title=title, body=body, tags=tags, wif=wif, author=author, community=community)
                await bot.send_message(user_id, result)
                await asyncio.sleep(20)
                post_info = self.steem.get_steem_posts(author)
                link = post_info['result'][0]['url']
                url = f'https://steemit.com{link}'
                await bot.send_message(user_id, url)
                await bot.send_message(cur8_channel, url)
                self.db.delete_program_post_data(user_id, now)
            await asyncio.sleep(30)

    
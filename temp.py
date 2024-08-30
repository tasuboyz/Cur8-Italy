async def notify_new_account(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        new_account_name = message.text
        keyboard = self.keyboards.new_account_inline(user_id, new_account_name)
        wait_for_account_text = self.language.wait_for_account(language_code)
        await state.clear()
        try:
            result = self.steem.create_account(new_account_name)
            if 'keys' in result:
                keys = result['keys']

                text = (
                f"{str(result['message'])}\n\n"
                "Keys:\n"
                f'Active Key: <code>{keys["active_key"]}</code>\n'
                f'Master Key: <code>{keys["master_key"]}</code>\n'
                f'Memo Key: <code>{keys["memo_key"]}</code>\n'
                f'Owner Key: <code>{keys["owner_key"]}</code>\n'
                f'Posting Key: <code>{keys["posting_key"]}</code>\n'
                f"Status: {result['status']}"
            )
            else:
                result = {(result['message'])}
                text= str(result)
            await message.answer(text)            
            # await bot.send_message(admin_id, new_account_name, reply_markup=keyboard)
            # await bot.send_message(account_creator, new_account_name, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

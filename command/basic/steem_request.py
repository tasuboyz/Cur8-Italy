from beem import Steem, Hive
from beem.account import Account
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.community import Communities, Community
import requests
import json
from beem.nodelist import NodeList
from beem.exceptions import WrongMasterPasswordException, AccountExistsException
from beem.imageuploader import ImageUploader
from .db import Database
from .instance import bot
from .config import admin_id
from .language import Language
from beem.vote import Vote

class Blockchain:
    def __init__(self, mode='irreversible'):
        self.mode = mode
        self.steem_node = "https://api.moecki.online"
        self.hive_node = 'https://api.deathwing.me'
        self.nodelist = NodeList()
        #self.hive = Hive(node=self.nodelist.get_steem_nodes())
        self.stm = Steem(node=self.steem_node)
        self.hive = Hive(node=self.hive_node)
        self.community = Communities(blockchain_instance=self.stm)
        self.db = Database()
        self.language = Language()

    def get_profile_info(self, username):  
        data = {
        "jsonrpc": "2.0",
        "method": "condenser_api.get_accounts",
        "params": [[username]],
        "id": 1
        }
        response = requests.post(self.steem_node, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            if len(data['result']) > 0:
                return data
            else:
                raise Exception("user not exist")
        else:
            raise Exception(response.reason)
            
    def get_steem_posts(self, username):
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "condenser_api.get_discussions_by_blog",
            "params": [{"tag": username, "limit": 1}],
            "id": 1
        }
        response = requests.post(self.steem_node, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)    
    
    def get_steem_dynamic_global_properties(self):
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "condenser_api.get_dynamic_global_properties",
            "params": [],
            "id": 1
        }
        response = requests.post(self.steem_node, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)
        
    def get_hive_dynamic_global_properties(self):
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "condenser_api.get_dynamic_global_properties",
            "params": [],
            "id": 1
        }
        response = requests.post(self.hive_node, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)    
    
    def get_steem_cur8_info(self):
        steem_url = 'https://imridd.eu.pythonanywhere.com/api/steem'
        response = requests.get(steem_url)
        if response.status_code == 200:
            data = response.json()
            return data[0]
        else:
            raise Exception(response.reason)
        
    def get_hive_cur8_info(self):
        hive_url = 'https://imridd.eu.pythonanywhere.com/api/hive'
        response = requests.get(hive_url)
        if response.status_code == 200:
            data = response.json()
            return data[0]
        else:
            raise Exception(response.reason)
        
    def get_steem_hive_price(self):
        url = 'https://imridd.eu.pythonanywhere.com/api/prices'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)
        
    def get_cur8_history(self):        
        url = 'https://imridd.eu.pythonanywhere.com/api/steem/history/cur8'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)
        
    def get_steem_transaction_cur8(self):
        account = Account("cur8", steem_instance=self.stm)
        history = account.get_account_history(-1, limit=1000)
        transactions = []
        for operation in history:
            op_type = operation['type']
            if op_type == 'transfer':
                account_to = operation['to']
                amount = operation['amount']['amount']
                transactions.append((account_to, amount.strip()))
        return transactions
    
    def get_top_20_steem_transactions(self):
        transactions = self.get_steem_transaction_cur8()
        account_transactions = {}

        for account_to, amount in transactions:
            if account_to not in account_transactions:
                account_transactions[account_to] = 0
            account_transactions[account_to] += float(amount)

        sorted_transactions = sorted(account_transactions.items(), key=lambda item: item[1], reverse=True)

        top_transactions = sorted_transactions[:20]
        return top_transactions
    
    def get_hive_transaction_cur8(self):
        account = Account("cur8", steem_instance=self.hive)
        history = account.get_account_history(-1, limit=1000)
        transactions = []
        for operation in history:
            op_type = operation['type']
            if op_type == 'transfer':
                account_to = operation['to']
                amount = operation['amount']['amount']
                transactions.append((account_to, amount.strip()))
        return transactions
    
    def get_top_20_hive_transactions(self):
        transactions = self.get_hive_transaction_cur8()
        account_transactions = {}

        for account_to, amount in transactions:
            if account_to not in account_transactions:
                account_transactions[account_to] = 0
            account_transactions[account_to] += float(amount)

        sorted_transactions = sorted(account_transactions.items(), key=lambda item: item[1], reverse=True)

        top_transactions = sorted_transactions[:20]
        return top_transactions
    
    def get_steem_top_delegators(self):
        top_10_delegator = []
        url = 'https://imridd.eu.pythonanywhere.com//api/steem/delegators/cur8'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)
        
    def get_hive_top_delegators(self):
        top_10_delegator = []
        url = 'https://imridd.eu.pythonanywhere.com//api/hive/delegators/cur8'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)
        
##################################################################################### Vote

    def vote_post(self, permlink, username, wif):
        stm = Steem(keys=[wif], node=self.steem_node, rpcuser=username)  
        account = Account(username, steem_instance=stm)
        vote = Vote(account, permlink, weight=100, blockchain_instance=stm)        
        return vote
        
##################################################################################### Community command
        
    def get_steem_community(self, community_name=''):
        result = self.community.search_title(community_name)
        return result
    
    def get_steem_community_post(self, community):
        community = Community(community, blockchain_instance=self.stm)
        result = community.get_ranked_posts(limit=100)
        return result
    
    def subscribe_community(self, community, username, wif):   
        stm = Steem(keys=[wif], node=self.steem_node)  
        community = Community(community, blockchain_instance=stm)
        result = community.subscribe(username)
        return True

    def unsubscribe_community(self, community, username, wif):        
        stm = Steem(keys=[wif], node=self.steem_node)  
        community = Community(community, blockchain_instance=stm)
        result = community.unsubscribe(username)
        return True

    def get_account_sub(self, username):
        community = []
        account = Account(username, steem_instance=self.stm)
        results = account.list_all_subscriptions()
        for result in results:
            community.append(result[0])
        return community
    
    def get_list_sub(self, username):
        account = Account(username, steem_instance=self.stm)
        results = account.list_all_subscriptions()
        return results

    ##########################################################################################
    ##########################################################################################
    
    def pubblica_post(self, language_code, title="", body="", author="", tags="", community='', wif=''):
        beneficiario = [{"account": "micro.cur8", "weight": 500}]
        result = self.get_profile_info(author)   
        stm = Steem(keys=[wif], node=self.steem_node, rpcuser=author)  
        try:
            account = Account(author, steem_instance=stm)
        except Exception as ex:            
            user_not_exist_text = self.language.username_not_exist(language_code)
            return user_not_exist_text
        try:
            posting_key = stm.wallet.getPostingKeyForAccount(author)   
        except:
            return "Posting key Invalid 🚫"
        result = stm.post(title=title, body=body, author=author, tags=tags, community=community, beneficiaries=beneficiario)
        return f"Post '{title}' pubblicato con successo!"
    
    def steem_upload_image(self, file_path, username, wif):
        stm = Steem(keys=[wif], node=self.steem_node, rpcuser=username)            
       
        uploader = ImageUploader(blockchain_instance=stm)
        result = uploader.upload(file_path, username)
        return result
    
    def steem_logging(self, language_code, user_id, username, wif):
        try:
            stm = Steem(keys=[wif], node=self.steem_node, rpcuser=username) 
        except:
            return "Posting key Invalid 🚫"
        try:
            account = Account(username, steem_instance=stm)
        except Exception as ex:            
            user_not_exist_text = self.language.username_not_exist(language_code)
            return user_not_exist_text
        try:
            user = stm.wallet.getAccountFromPrivateKey(wif)   
            follow_result = account.follow('tasubot', what=['blog'], account=None)
        except Exception as ex:   
            print(ex)
            return "Posting key Invalid 🚫"
        try:
            self.db.insert_user_account(user_id, username, wif)
            login_succesful_text = self.language.login_successful(language_code)
            return login_succesful_text
        except Exception as ex:
            return "Login Failed 🚫"
        
    def verify_identity(self, username, wif):
        stm = Steem(node=self.steem_node, rpcuser=username) 
        try:
            account = Account(username, steem_instance=stm)
        except Exception as ex:            
            return "Username not exist 🚫"
        try:
            key_usaname = stm.wallet.getAccountFromPrivateKey(wif)
        except Exception as ex:            
            return "Key not valid 🚫"
        return
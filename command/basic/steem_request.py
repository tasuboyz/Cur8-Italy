from beem import Steem, Hive
from beem.account import Account
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.community import Communities, Community
import requests
import json
from beem.nodelist import NodeList

steem = Steem()
blockchain = Blockchain(steem_instance=steem)

class Blockchain:
    def __init__(self, mode='irreversible'):
        self.mode = mode
        self.steem_node = "https://api.moecki.online"
        self.hive_node = 'https://api.hive.blog'
        self.nodelist = NodeList()
        self.stm = Steem(node=self.steem_node)
        self.hive = Hive(node=self.hive_node)
        self.community = Communities(blockchain_instance=self.stm)

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
        
    def post_to_steem(self, username, posting_key, title, body, tags, password):
        s = Steem()
        account = Account(username, steem_instance=s)
        s.wallet.unlock(password)
        s.post(title=title, body=body, tags=tags, self_vote=False)

    def pubblica_post(self, titolo, corpo, autore, chiave_posting, tags):
        steem_instance = Steem(keys=[chiave_posting])
        blockchain_instance = Blockchain(steem_instance=steem_instance)
        
        # Creazione del post
        post = Comment(
            title=titolo,
            body=corpo,
            author=autore,
            tags=tags,
            steem_instance=steem_instance
        )
        
        # Pubblicazione del post
        post.commit()
        
        return f"Post '{titolo}' pubblicato con successo!"
    
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
    
    def get_steem_community(self, community_name):
        result = self.community.search_title(community_name)
        return result
    
    def get_steem_community_post(self, community):
        community = Community(community, blockchain_instance=self.stm)
        result = community.get_ranked_posts(limit=100)
        return result
    
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
        top_delegators = self.get_top_20_steem_transactions()
        delegator_totals = {}
        top_10_delegator = []
        for delegator, total_amount in top_delegators:
            account = Account(delegator, steem_instance=self.stm)

            delegations = account.get_vesting_delegations()
            cur8_delegation = next((item for item in delegations if item['delegatee'] == 'cur8'), None)
            availableVESTS = cur8_delegation['vesting_shares']['amount'] if cur8_delegation else None
            if availableVESTS:
                vests = self.get_steem_dynamic_global_properties()
                total_vesting_fund_steem = float(vests['result']['total_vesting_fund_steem'].replace('STEEM', '').strip())
                total_vesting_shares = float(vests['result']['total_vesting_shares'].replace('VESTS', '').strip())
                result = (total_vesting_fund_steem * float(availableVESTS) ) / total_vesting_shares
                total_amount = result / 10**6
                delegator_totals[delegator] = total_amount

                sorted_delegators = sorted(delegator_totals.items(), key=lambda x: x[1], reverse=True)

        for delegator, total_amount in sorted_delegators[:10]:
            top_10_delegator.append((delegator, total_amount))
        return top_10_delegator
    
    def get_hive_top_delegators(self):
        top_delegators = self.get_top_20_hive_transactions()
        delegator_totals = {}
        top_10_delegator = []
        for delegator, total_amount in top_delegators:
            account = Account(delegator, steem_instance=self.hive)

            delegations = account.get_vesting_delegations()
            cur8_delegation = next((item for item in delegations if item['delegatee'] == 'cur8'), None)
            availableVESTS = cur8_delegation['vesting_shares']['amount'] if cur8_delegation else None
            if availableVESTS:
                vests = self.get_hive_dynamic_global_properties()
                total_vesting_fund = float(vests['result']['total_vesting_fund_hive'].replace('HIVE', '').strip())
                total_vesting_shares = float(vests['result']['total_vesting_shares'].replace('VESTS', '').strip())
                result = (total_vesting_fund * float(availableVESTS) ) / total_vesting_shares
                total_amount = result / 10**6
                delegator_totals[delegator] = total_amount

                sorted_delegators = sorted(delegator_totals.items(), key=lambda x: x[1], reverse=True)

        for delegator, total_amount in sorted_delegators[:10]:
            top_10_delegator.append((delegator, total_amount))
        return top_10_delegator

    def read_current_block_info(self):
        # Legge le informazioni dell'attuale blocco
        pass

    def monitor_new_blocks(self, stop=None):
        # Monitora i nuovi blocchi
        pass

    def get_transaction(self, transaction_id):
        # Restituisce la transazione come vista dalla blockchain
        pass

    def get_block_datetime(self, block_num):
        # Restituisce la data e l'ora del blocco con il numero specificato
        pass

    def yield_blocks(self, start):
        # Produce blocchi a partire da 'start'
        pass

    def find_pending_recovery_requests(self, accounts):
        # Trova richieste di cambio dell'account in sospeso
        pass

    def get_rc_params(self, accounts):
        # Restituisce i parametri RC degli account
        pass

    def get_account_count(self):
        # Restituisce il numero di account
        pass

    def yield_account_reputations(self, start, stop):
        # Produce la reputazione degli account tra 'start' e 'stop'
        pass

    def get_current_block(self):
        # Restituisce il blocco corrente
        pass

    def estimate_block_num(self, date):
        # Stima il numero del blocco basato su una data fornita
        pass

    def find_similar_accounts(self, name, limit):
        # Restituisce account simili con nome come lista
        pass

    def get_transaction_hex(self, transaction):
        # Restituisce un hexdump della forma binaria serializzata di una transazione[^4^][4]
        pass

    def is_transaction_valid(self, transaction_id):
        # Restituisce vero se l'id della transazione è valido
        pass

    # Altri metodi...

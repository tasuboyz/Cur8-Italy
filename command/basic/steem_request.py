from beem import Steem
from beem.account import Account
from beem.blockchain import Blockchain
from beem.comment import Comment
import requests
import json

steem = Steem()
blockchain = Blockchain(steem_instance=steem)

account_name = 'cur8'
account = Account(account_name, steem_instance=steem)

# for transazione in account.history_reverse(only_ops=["transfer"]):
#     print(transazione)
def get_cur8_history():
    history = account.get_account_history(-1, limit=1)
    for operation in history:
        print(operation)

class Blockchain:
    def __init__(self, mode='irreversible'):
        self.mode = mode
        self.node = "https://api.moecki.online"

    def get_profile_info(self, username):  
        data = {
        "jsonrpc": "2.0",
        "method": "condenser_api.get_accounts",
        "params": [[username]],
        "id": 1
        }
        response = requests.post(self.node, data=json.dumps(data))
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
        response = requests.post(self.node, headers=headers, data=json.dumps(data))
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

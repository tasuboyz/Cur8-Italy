import logging
from pyngrok import ngrok

TEST = True

if TEST:
    TOKEN = "" #TasuAdmin
    log_level = logging.INFO 
    cur8_channel = '@'
    report_channel = '@'
else:
    TOKEN = '' #token produzione
    log_level = logging.ERROR
    cur8_channel = '@test_sniper_cur8'
    report_channel = '@'

admin_id = ''

account_creation_channel = 1234

api_base_url = 'http://localhost:8081'  

log_file_path = 'log.txt'  

use_local_api = False  # Set to False if the API is not in local

WEB_SERVER_HOST = "127.0.0.1"

WEB_SERVER_PORT = 5173

WEBHOOK_PATH = r"/webhook"

WEBHOOK_SECRET = "my-secret"

ngrok_auth = ""

ngrok.set_auth_token(ngrok_auth)

http_tunnel = ngrok.connect(5173) 

url_ngrok = http_tunnel.public_url

BASE_WEBHOOK_URL = url_ngrok

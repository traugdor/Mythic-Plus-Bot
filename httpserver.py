
from flask import Flask, request, flash, render_template, session, abort
from threading import Thread
import wow

client = None

app = Flask('')

@app.route('/')
def home():
    return render_template('main.html', name='World')

@app.route('/oauth/callback/')
async def oauth_callback():
    state = request.args.get('state')
    code = request.args.get('code')
    UID = state[3:]
    #post code to token url
    access_token = wow.login(code)
    if access_token.startswith("success! code="):
        """not implemented"""
        #read JSON response from blizzard and save access_token
        #check_token to get expiry
        #userinfo to get UID
        #save bUID, access_token, expiry, scope, and game
        #get id from DB where UID = bUID
        #save UID, and id in users
        #query list of characters and save in wowCharacters
        #message discord user (using UID) that the process is finished
    else:
        user = client.get_user(int(UID))
        await client.send_message(user, str(access_token))

def run():
    app.run(
        host='0.0.0.0', 
        port=8080
    )

def keep_alive():
    t = Thread(target=run)
    t.start()
    
def bot(in_client):
    client = in_client
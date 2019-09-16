import discord
from flask import Flask, request, flash, render_template, session, abort
from threading import Thread
from discord.utils import get
import wow
import db

client = None
DEFAULT = object()

app = Flask(__name__) #start web server

@app.route('/')
def home():
    return render_template('main.html', name='World') #render landing page

@app.route('/oauth/callback/') #response from Blizzard servers will land here.
def oauth_callback():
    #get state and code. Code will need to be verified with the wow.login function
    #state will be trimmed and used as the Discord UID
    state = request.args.get('state')
    code = request.args.get('code')
    UID = state[3:]
    #post code to token url
    access_token = wow.login(code)
    #function returns either success with the token or some error message
    if access_token.startswith("success token="):
        # Not finished
        #read token response from login function and save access_token
        token = access_token[14:]
        #check_token to get expiry
        success, data = wow.checktoken(token)
        if success:
            username = data[0]
            exp = data[1]
            btag = data[2]
        #userinfo to get UID
        #bUID is blizzard UserID = username in this instance
        #save bUID, access_token, expiry, scope, and game
        data = [username, token, exp, 'scope.wow', 'wow']
        #save UID, and id in users
        #get id from DB where UID = bUID
        #saveWowAccountData returns bID which is a unique id from the db server
        #    it returns this value ONLY if this is a new account
        bid = db.saveWowAccountData(data)
        #if it returned an ID from the DB, we need to save the account data with the discord UID
        if bid is not None:
            db.insertUser(UID, bid)
        #query list of characters and save in wowCharacters
        
        #eventually......... we'll get here.
        return render_template('main.html', name=btag, message="You have successfully linked your Discord and World of Warcraft accounts. Please close this window and return to Discord to start using the bot. Also your token is " + token)
    else:
        #there was some error, tell the user so they can hopefully report it. :P
        return render_template('main.html', message=access_token)
    

#below is code that keeps the http server running. I advise shoving it through nginx or apache with internal port forwarding because this code spits tons of errors if you try to run it through gunicorn. Please help.
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
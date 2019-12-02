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
    return render_template('landing.html', message="Thanks for choosing to use Mythic Plus Bot.") #render landing page

@app.route('/oauth/callback/') #response from Blizzard servers will land here.
def oauth_callback():
    msgstr = ""
    #get state and code. Code will need to be verified with the wow.login function
    #state will be trimmed and used as the Discord UID
    state = request.args.get('state')
    code = request.args.get('code')
    UID = ""
    if state is not None:
        UID = state[3:]
    else:
        UID = ""
        state = ""
    if code is None:
        code = ""
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
        newuser, bid = db.saveWowAccountData(data)
        #if it returned an ID from the DB, we need to save the account data with the discord UID
        if newuser is True:
            db.insertUser(UID, bid)
        #query list of characters and save in wowCharacters
        characters = wow.listCharacters(access_token = token)
        updatedCharacters = []
        for char in characters:
            char["bid"] = bid
            char["UID"] = UID
            updatedCharacters.append(char)
        result = db.saveCharacters(updatedCharacters)
        if result is True:
            #update userCharacters!
            
            msgstr = "You have successfully linked your Discord and World of Warcraft accounts. We were able to save all your character data. If you wish to add data for a different World of Warcraft account, you will need to run the register command again using a different discord profile. Please close this window to start using the bot and add characters to the watch list for Mythic Plus key runs."
        else:
            msgstr = "You appear to have successfully linked your Discord and World of Warcraft accounts, but we were unable to save your character data. I'm not sure how we got here, but here we are. Please contact a developer to investigate this incident. <br><br>BID=" + bid +"<br><br>Please use the above information when contacting the developer."
        
        #eventually......... we'll get here.
        return render_template('main.html', name="Hello " + btag + "!", message=msgstr + " Also your token is " + token)
    else:
        #there was some error, tell the user so they can hopefully report it. :P
        return render_template('main.html', name="Uh oh!", message="There was an error: " + access_token)
    
@app.route('/discordoauth/callback/') #response from adding to discord servers will land here.
def discordoauth():
    state = request.args.get('state')
    msg = ""
    if state == 'bot':
        msg = "Thanks for choosing to use Mythic Plus Bot. Please use the Discord command '!mplus register' to get started!"
    else:
        msg = ""
    
    return render_template('discord_added.html', message="Thanks for choosing to use Mythic Plus Bot. Please use the Discord command '!mplus register' to get started!") #render landing page
    
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
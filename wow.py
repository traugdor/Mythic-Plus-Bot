import settings as cfg
import db
import requests
import json

#--- setup and definitions used in code ---#
urlpre = 'https://'
region = cfg.wowRegionCode
authorizeurlpost = '.battle.net/oauth/authorize'
oauthurlpost = '.battle.net/oauth/'
wowurlpost = '.api.blizzard.com/wow/'
oauthBase = "" #blank but will be filled out below

if(region == 'china'):
    authorizeurlpost = 'www.battlenet.com.cn/oauth/authorize'
    oauthurlpost = 'www.battlenet.com.cn/oauth/'
    wowurlpost = 'gateway.battlenet.com.cn/wow/'
    region = ''
    
authorizeUrl = ''.join([urlpre, region, authorizeurlpost])
oauthBase = ''.join([urlpre, cfg.wowClientId, ':', cfg.wowClientSecret, '@', region, oauthurlpost])
#--- End setup ---#

def listCharacters(bID = None, access_token = None, bUsername = None):
    """Returns list of blizzard characters from database.
    Required input, one of: bID, bUsername, or access_token"""
    if bID is not None:
        """do something"""
        #lookup accesstoken where bid = bid
        #use access_token below
        
    
        
    if bUsername is not None:
        """do something"""
        #lookup accesstoken where UID = bUsername
        #use access_token below
        
    if access_token is not None:
        """do something"""
        #get json from wow and pull all characters
        wowCharactersURL = urlpre + region + wowurlpost + 'user/characters?access_token=' + access_token
        r = requests.get(wowCharactersURL)
        response = json.loads(json.dumps(r.json))
        characters = response["characters"]
        responseData = []
        for char in characters:
            name = char["name"].lower()
    else:
        raise ValueError("No combination of errors could produce a valid access_token")

def getCharacter(characterId):
    """return character information from WoW using the supplied characterID"""
    
def getMythicKey(characterId):
    """Get this character's highest key from Raider.IO"""
    #query raider.io
    
def login(code):
    """use supplied authorization_code to complete the wow OAuth exchange and get an access_token
    Returns one of the following:
        success token=<token>
        <error message>"""
    tokenUrl = oauthBase + "token?redirect_uri=" + cfg.botBaseUrl + "oauth/callback&grant_type=authorization_code&scope=wow.profile&code=" + code
    #post
    r = requests.post(tokenUrl)
    #expect JSON response in body
    print(r.json())
    response = json.loads(json.dumps(r.json()))
    if 'access_token' not in response:
        if 'error' not in response:
            return "Something terrible happened with connecting with the WoW servers."
        else:
            return response["error"] + "   " + response["error_description"]
    else:
        return "success token=" + response["access_token"]
        
            
def checktoken(token):
    """checks the wow token to make sure it's still good
    returns one of the following:
        False, [<error description>]
        True, [<bUsername>, <token expiration date>, <battletag>]"""
    #complete token check URL
    checktokenUrl = oauthBase + "check_token?token=" + token
    r = requests.get(checktokenUrl)
    response = json.loads(json.dumps(r.json()))
    #check for errors
    if 'user_name' not in response:
        if 'error' not in response:
            return False, ["", ""]
        else:
            return False, [response["error_description"], ""]
    else:
        #process good data
        username = response["user_name"]
        exp = response["exp"]
        #if token is still good, get the user information in case we need to update anything
        userinfoUrl = oauthBase + "userinfo?access_token=" + token
        r = requests.get(userinfoUrl)
        response = json.loads(json.dumps(r.json()))
        #check for errors
        if 'battletag' not in response:
            if 'error' not in response:
                return False, ["", ""]
            else:
                return False, [response["error_description"],""]
        else:
            #process good data and return to calling function
            btag = response["battletag"]
            return True, [username, exp, btag]
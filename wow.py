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
wowurlbase = '.api.blizzard.com/'
oauthBase = "" #blank but will be filled out below

if(region == 'china'):
    authorizeurlpost = 'www.battlenet.com.cn/oauth/authorize'
    oauthurlpost = 'www.battlenet.com.cn/oauth/'
    wowurlpost = 'gateway.battlenet.com.cn/wow/'
    wowurlbase = 'gateway.battlenet.com.cn/'
    region = ''
    
authorizeUrl = ''.join([urlpre, region, authorizeurlpost])
oauthBase = ''.join([urlpre, cfg.wowClientId, ':', cfg.wowClientSecret, '@', region, oauthurlpost])
#---      End setup and definitions      ---#

def listCharacters(bID = None, access_token = None, bUsername = None):
    ##########################################################
    # Returns list of blizzard characters from database.     #
    # Required input, oneof: bID, bUsername, or access_token #
    ##########################################################
    """Not complete"""
    if bID is not None:
        """do something"""
        #lookup accesstoken where bid = bid
        #use access_token below
        access_token = db.getToken(bid = bID)
        
    
        
    if bUsername is not None:
        """do something"""
        #lookup accesstoken where UID = bUsername
        #use access_token below
        access_token = db.getToken(username = bUsername)
        
    if access_token is not None:
        """do something"""
        #get json from wow and pull all characters
        data = getCharacters(access_token)
        return data
    else:
        raise ValueError("No combination of values could produce a valid access_token in wow.listCharacters")

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

def getCharacters(access_token, bID = None):
    """get characters from wow api and get only the data we need
    returns:
        [{
            "name": name,
            "charRegion": charRegion,
            "bid": bid,
            "level": level
        }"""
    bid = ""
    wowCharactersURL = urlpre + region + wowurlbase + 'profile/user/wow?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(wowCharactersURL)
    response = json.loads(json.dumps(r.json()))
    wowaccounts = response["wow_accounts"]
    responseData = []
    if bID is None:
        #lookup bid using accesstoken?
        bid = db.getBIDfromToken(access_token)
    else:
        bid = bID
    for wowaccount in wowaccounts:
        characters = wowaccount["characters"]
        for char in characters:
            name = char["name"].lower()
            charRegion = char["realm"]["slug"]
            level = char["level"]
            wowChar = {
                "name": name,
                "charRegion": charRegion,
                "bid": bid,
                "level": level
            }
            responseData.append(wowChar)
    return responseData
    
def getClientToken():
    """get a unique access token just for this client
    returns:
        access_token to use for API calls that do not need specific user authorization"""
    url = oauthBase + "/token?grant_type=client_credentials&scope=wow.profile"
    r=requests.get(url)
    response = json.loads(json.dumps(r.json()))["access_token"]
    return response
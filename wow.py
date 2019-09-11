from wowapi import WowApi
import settings as cfg
import db
import requests
import json

urlpre = 'https://'
region = cfg.wowRegionCode
authorizeurlpost = '.battle.net/oauth/authorize'
tokenurlpost = '.battle.net/oauth/token'


if(region == 'china'):
    authorizeurlpost = 'www.battlenet.com.cn/oauth/authorize'
    tokenurlpost = 'www.battlenet.com.cn/oauth/token'
    region = ''
    
authorizeUrl = ''.join([urlpre, region, authorizeurlpost])
tokenUrl = ''.join([urlpre, cfg.wowClientId, ':', cfg.wowClientSecret, '@', region, tokenurlpost])
tokenUrl = tokenUrl + "?redirect_uri=" + cfg.botBaseUrl + "oauth/callback&grant_type=authorization_code&scope=wow.profile&code="

api = WowApi(cfg.wowClientId, cfg.wowClientSecret)

def getCharacter(characterId):
    """ do something """
    
def getMythicKey(characterId):
    """ do something """
    
def login(code):
    #post
    r = requests.post(tokenUrl + code)
    #expect JSON response in body
    response = json.load(r.json())
    if 'access_token' not in response:
        if 'error' not in response:
            return "Something terrible happened with connecting with the WoW servers."
        else:
            return response["error"] + "   " + response["error_description"]
    else:
        return "success token=" + response["access_token"]
        
            
    
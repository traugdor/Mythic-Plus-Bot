from wowapi import WowApi
import settings as cfg
import db
import requests

urlpre = 'https://'
region = cfg.wowRegionCode
authorizeurlpost = '.battle.net/oauth/authorize'
tokenurlpost = '.battle.net/oauth/token'

if(region == 'china'):
    authorizeurlpost = 'www.battlenet.com.cn/oauth/authorize'
    tokenurlpost = 'www.battlenet.com.cn/oauth/token'
    region = ''
    
authorizeUrl = ''.join([urlpre, region, authorizeurlpost])
tokenUrl = ''.join([urlpre, region, tokenurlpost])

api = WowApi(cfg.wowClientId, cfg.wowClientSecret)

def getCharacter(characterId):
    """ do something """
    
def getMythicKey(characterId):
    """ do something """
    
def login():
    print(authorizeUrl)
    print(tokenUrl)
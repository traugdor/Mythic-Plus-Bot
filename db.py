import mysql.connector
import settings as cfg
import dblayout as dbl
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user=cfg.dbuser,
    passwd=cfg.dbpass,
    database=cfg.dbname
)

mycursor = db.cursor()

def configure():
    sql = "SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema='" + cfg.dbname + "'"
    val = ()
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    count = mycursor.rowcount
    if count == -1 or count < 4:
        print("Installing tables in DB")
        print("creating users table")
        sql = dbl.SQL_users
        mycursor.execute(sql, val)
        db.commit()
        print("creating blizzard_account_data table")
        sql = dbl.SQL_blizzard_account_data
        mycursor.execute(sql, val)
        db.commit()
        print("creating wowCharacters table")
        sql = dbl.SQL_wowCharacters
        mycursor.execute(sql, val)
        db.commit()
        print("creating userCharacters table")
        sql = dbl.SQL_userCharacters
        mycursor.execute(sql, val)
        db.commit()
        print("done")
        sql = "SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema='" + cfg.dbname + "'"
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        count = mycursor.rowcount
        if count == -1 or count < 4:
            print("Something went wrong. Please check DB. Bot will fail to work properly until DB is fixed.")
        else:
            print("DB is good to go!")
    else:
        print("DB is good to go!")

def insertUser (discordId, blizzardAccountId):
    sql = "INSERT INTO users (discordUID, blizzardAccountID) VALUES (%s, %s)"
    val = (int(discordId), int(blizzardAccountId))
    mycursor.execute(sql, val)
    db.commit()
    print(mycursor.rowcount, "record inserted.")
    
def findCharacterByName(characterName, regionName):
    sql = ""
    if regionName is None:
        sql = "SELECT * FROM wowCharacters WHERE characterName = '" + characterName + "'"
    else:
        sql = "SELECT * FROM wowCharacters WHERE characterName = '" + characterName + "' and region = '" + regionName + "'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    print(results)
    return results
    
def saveWowAccountData(data):
    #data = [username, token, exp, 'scope.wow', 'wow']
    #check if bUID already exists
    sql = "SELECT * FROM blizzard_account_data where UID = " + data[0]
    mycursor.execute(sql)
    result = mycursor.fetchall()
    count = mycursor.rowcount
    date = data[2]
    formatted_date = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    if count == 0:
        sql = "INSERT INTO blizzard_account_data (UID, game, access_token, expires_on, scope) \
        VALUES ( %s, %s, %s, %s, %s)"
        val = (data[0], data[4], data[1], formatted_date, data[3])
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "record inserted.")
        sql = "Select id from blizzard_account_data where UID = '"+  data[0] + "'"
        mycursor.execute(sql)
        bid = mycursor.fetchone()[0]
        return True, bid
    else:
        sql = """UPDATE blizzard_account_data
        SET access_token=%s, expires_on=%s
        WHERE UID=%s"""
        val = (data[1], formatted_date, data[0])
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "record updated.")
        sql = "Select id from blizzard_account_data where UID = '"+  data[0] + "'"
        mycursor.execute(sql)
        bid = mycursor.fetchone()[0]
        return False, bid
        
def getToken(bid = None, username = None):
    sql = ""
    val = ()
    if bid is None:
        if username is None:
            raise ValueError("No combination of values could produce a valid access_token in db.getToken")
        else:
            sql = "SELECT access_token from blizzard_account_data where UID=%s"
            val = (username)
    else:
        sql = "SELECT access_token from blizzard_account_data where id=%s"
        val = (bid)
    
    mycursor.execute(sql, val)
    access_token = mycursor.fetchone()[0]
    return access_token

def saveCharacters(charData):
    selectSql = "SELECT * from wowCharacters WHERE wowAccountId=%s and characterName=%s and region=%s"
    sql = "INSERT INTO wowCharacters (wowAccountId, characterName, region, characterLevel) VALUES(%s,%s,%s,%s)"
    for char in charData:
        insertval=(char["bid"], char["name"], char["charRegion"], char["level"])
        val=(char["bid"], char["name"], char["charRegion"])
        mycursor.execute(selectSql, val)
        results = mycursor.fetchall()
        if mycursor.rowcount == 0:
            mycursor.execute(sql, insertval)
            db.commit()
            if mycursor.rowcount == 1:
                print(val, "inserted.")
            else:
                print(val, "not inserted or there was an error")
    return True
    
def getBIDfromToken(access_token):
    sql = "SELECT id from blizzard_account_data WHERE access_token = '" + access_token + "'"
    mycursor.execute(sql)
    bid = mycursor.fetchone()[0]
    return bid
    
def getBIDfromDiscordUser(UID):
    sql = "SELECT blizzardAccountID FROM users WHERE discordUID = '" + UID + "'"
    mycursor.execute(sql)
    bid = mycursor.fetchone()[0]
    return bid
    
def listAllCharacters(bid = None):
    sql = ""
    if bid is None:
        sql = "SELECT * from wowCharacters"
    else:
        sql = "SELECT * FROM wowCharacters where wowAccountId = '" + str(bid) + "'"
    mycursor.execute(sql)
    characters = mycursor.fetchall()
    return characters
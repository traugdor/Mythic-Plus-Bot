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
    if count == -1 or count < 5:
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
        print("creating characters table")
        sql = dbl.SQL_characters
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
        if count == -1 or count < 5:
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
    
def insertWowCharacter(userId, characterName, characterRegion):
    sql = "INSERT INTO characters (characterName, region, highestKey) VALUES (%s, %s, 0)"
    val = (characterName, characterRegion)
    mycursor.execute(sql, val)
    db.commit()
    sql = "SELECT id FROM characters WHERE characterName = '" + characterName + "'"
    mycursor.execute(sql)
    cid = mycursor.fetchone()[0]
    print(str(cid) + " was inserted");
    sql = "INSERT INTO userCharacters (userId, characterId) VALUES (%s, %s)"
    val = (int(userId), int(cid))
    mycursor.execute(sql, val)
    db.commit()
    print("Character added")
    
def findCharacterByName(characterName):
    sql = "SELECT * FROM wowCharacters WHERE characterName = '" + characterName + "'"
    mycursor.execute(sql)
    results = mycursor.fetchone()
    print(results)
    
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
        return bid
    else:
        sql = """UPDATE blizzard_account_data
        SET access_token=%s, expires_on=%s
        WHERE UID=%s"""
        val = (data[1], formatted_date, data[0])
        mycursor.execute(sql, val)
        print(mycursor.rowcount, "record updated.")
        return None
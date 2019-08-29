import mysql.connector
import settings as cfg

db = mysql.connector.connect(
    host="localhost",
    user=cfg.dbuser,
    passwd=cfg.dbpass,
    database=cfg.dbname
)

"""
this is a comment
"""

mycursor = db.cursor()

def insertUser (discordId, blizzardAccountId):
    sql = "INSERT INTO users (discordUID, blizzardAccountID) VALUES (%s, %s)"
    val = (int(discordId), int(blizzardAccountId))
    mycursor.execute(sql, val)
    db.commit()
    print(mycursor.rowcount, "record inserted.")
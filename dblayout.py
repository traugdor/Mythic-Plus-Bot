#tables

#users
#characters
#usercharacters
#Blizzard_Account_Data

#Users --

#id -- unique numerical id -- used internally
#Discord uid
#Blizzard account id

SQL_users = "CREATE TABLE IF NOT EXISTS `users` ( \
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT, \
 `discordUID` bigint(20) unsigned NOT NULL, \
 `blizzardAccountID` bigint(20) unsigned NOT NULL, \
 `datelastmaint` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
 KEY `id` (`id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1"

#Characters --

#id -- unique numerical id -- used internally
#characterName
#highestKey

SQL_characters = "CREATE TABLE IF NOT EXISTS `characters` ( \
 `id` int(11) NOT NULL AUTO_INCREMENT, \
 `characterName` varchar(20) NOT NULL, \
 `region` varchar(30) NOT NULL, \
 `highestKey` int(11) NOT NULL, \
 `datelastmaint` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
 KEY `id` (`id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1"

#UserCharacters --

#id -- unique numerical id -- used internally
#userId
#characterId

SQL_userCharacters = "CREATE TABLE IF NOT EXISTS `userCharacters` ( \
 `id` int(11) NOT NULL AUTO_INCREMENT, \
 `userId` int(11) NOT NULL, \
 `characterId` int(11) NOT NULL, \
 `datelastmaint` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
 KEY `id` (`id`), \
 KEY `characterId` (`characterId`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1"

#Blizzard_Account_Data --

#id -- unique numerical id -- used internally
#UID -- discord user id
#game -- game for which the token can access API calls. `wow` is the only valid value at this time
#access_token -- blizzard accesstoken
#expires_on -- generated timestamp that would suggest that the token is expired and needs to be refreshed
#scope -- scope of the token. `wow.profile` is the only valid value at this time.

SQL_blizzard_account_data = "CREATE TABLE IF NOT EXISTS `blizzard_account_data` ( \
 `id` int(11) NOT NULL AUTO_INCREMENT, \
 `UID` bigint(20) NOT NULL, \
 `game` varchar(20) NOT NULL, \
 `access_token` varchar(40) NOT NULL, \
 `expires_on` timestamp NULL NOT NULL, \
 `scope` varchar(20) NOT NULL, \
 `datelastmaint` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
 KEY `id` (`id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1"

#wowCharacters --

#id -- unique numerical id -- used internally
#accountId -- blizzard account id
#characterName -- name of character
#characterLevel -- level of character
#region -- character region

SQL_wowCharacters = "CREATE TABLE IF NOT EXISTS `wowCharacters` ( \
 `id` int(11) NOT NULL AUTO_INCREMENT, \
 `wowAccountId` int(11) NOT NULL, \
 `characterName` varchar(20) NOT NULL, \
 `region` varchar(30) NOT NULL, \
 `datelastmaint` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
 KEY `id` (`id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1"
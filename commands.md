# MPB Commands

## Syntax

`!mplus register`

This is a straight forward command and needs no additional arguments

`!mplus add <toon name>`

Replace `<toon name>` with the name of one of the World of Warcraft characters you would like to track.
You can obtain a list of characters by either logging into the game client or using a different bot (such as Jeeves)
to get a list of characters for you. The purpose of this bot is not to track all characters, but just the ones you
want to track for mythic plus.

`!mplus check`

This is a straight forward command and needs no additional arguments

`!mplus remove <toon name>`

Replace `<toon name>` with the name of one of the World of Warcraft characters you would no longer like to track.
You can obtain a list of characters by either logging into the game client or using a different bot (such as Jeeves)
to get a list of characters for you. The purpose of this bot is not to track all characters, but just the ones you
want to track for mythic plus.

`!mplus notification <on/off>`

Replace `<on/off>` with either the option `on` or the option `off`. Selecting off will exclude you from any
messages that might alert you that the mythic week is almost up.

## Actions

### Register
When a user invokes the 'register' command, it will respond with in a private message with a URL. This URL will take
them to a webpage where they will be prompted to log into their World of Warcraft account. Logging into this account
will register it to make it easier to search mythic plus statistics for the characters that will be added later.
All accounts connected to the login used will be registered. Accounts may be unregistered by using the 'register remove'
command.

### Add
When a user invokes the 'add' command, check to see if it is followed by a valid character name. If the character
named exists within the user's account registered, then the character will be added to the list of characters to 
track. If this is the first character the user has added, they will recieve a reply in the same channel explainging
that they will start to recieve notifications if they have not run at least a +10 keystone before the weekly reset.

### Check
When a user invokes the 'check' command, the bot will reply with a list of all registered characters and the highest
key that character has completed.

### Remove
When a user invokes the 'remove' command, check to see if it is followed by a valid character name. If the character
named exists within the user's account registered, then the character will be removed from the list of characters to
track. If this is the last character the user has added, they will no longer get notifications of they have not run
at least a +10 keystone before the weekly reset.

### Notification
When a user invokes the 'notification' command, check to see if it is followed by 'on' or 'off'. Either option will
add or remove the user from any notifications if they have not run at least a +10 keystone before the weekly reset.
Notifications will be sent 48 hours and again 24 hours before the weekly reset. Sample notification text:

    You haven't run at least a +10 keystone on all your registered characters!
    Weekly reset is in 48 hours.

This notification will be sent via DM to avoid interfering with the Discord server operations.

#### ----

If any command is not properly entered, then the bot will reply in the same channel with the proper syntax of that
command. If no valid command is entered, then the bot will reply with a list of all the available commands. If the
`!mplus` command prefix is not properly entered, then the bot will not respond. All proper commands will receive a
reply in the same channel to provide the user with feedback that the command was entered properly.
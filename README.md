<p align='center'>
<img src='https://github.com/foo290/resonate-beats/blob/main/readme_imgs/discord-logo.png' width=180px, alt='an image was supposed to be here'>
</p>
<h1 align='center', style='font-size:30px'><b> resonate-beats</b> 🎵</h1>

## Setup

### 1. Dependencies :

Everything you need to run this player is defined in requirements.txt.


### 2. Directory and files setup :

There is an extension file in COG directory named musiccog.py, add that file to your existing cog directory and the add "resonate_utils" directory to one level top of it. So if your current setup should look like this : 

```
├── bot.py
├── cogs
│   ├── __init__.py
│   ├── admin_cmds.py
|   |__ ...
│   |__ musiccog.py     ----> Music Cog file.
|   |__ ...
|
└── resonate_utils     ----> Utilities directory one level above from COG.
    ├── __init__.py
    ├── custom_exceptions.py
    ├── decorators.py
    ├── embeds.py
    ├── logger.py
    ├── music_utils.py
    ├── resonate_settings.py
    └── track_utils.py
```
<b>NOTE : </b>The ```musiccog.py``` file contains relative imports from ```resonate_utils``` dir, If your project needs to change the location of resonate utiils then change the relative imports to absolute imports.

Once your directory setup is complete, load the cog/extension in your bot by the method you are using to load COGs in your bot.
The musiccog contains a built in logger so you will know it the file has been loaded successfully as it will print status to the STDOUT.

### 3. Server setup :
The server and configuration used in this project is provided in ```server``` directory exactly for cloud server setup. (I used heroku for testing.)

This project uses lavalink server to stream music which can be downloaded <a href='https://github.com/Frederikam/Lavalink/releases'>here</a>.

Once you download the server ```Lavalink.jar``` file, to test it locally, run command in your terminal :

```
>>> java -jar Lavalink.jar
```

This will start the server at your local machine. To connect it locally or remotely, set <a href='#serverconfigs'>these configurations</a> in ```resonate_settings.py``` file.

# Commands

Join the voice channel and run ```<your_prefix>join``` command to connect bot. The bot will join the voice channel in which the command invoker currently in, if no voice channel is found, the bot will show relevant message. 

Every command must be followed by yout command prefix like : ```<command_prefix>command```.


|  Command Name |  Command Alias |          Command Parameters          |                 Command Action                    |                 Extra note                  |
|---------------|----------------|--------------------------------------|---------------------------------------------------|---------------------------------------------|
| connect       |    join        |            channel name(Optional)    | connect the bot to the voice channel              | Command invoker should be in voice channel  |
| play          |         p      | song_name/song_link/playlist_link    | Searches for the given params, will ask for the songs found and add that to the playlist.         | Resumes the playerif it is paused.|
| stop          |      s         |            None                      | Stops the player and clears the current playlist. |         None                                |
| pause         |     ps         |            None                      | Pauses the player.                                | To resume the player, use play command without params.|
| playlist      |       pl       | int (2,3,4...) Page no. of playlist  | The playlist shows limited songs by default, to traverse between all the songs, use pl command with an integer specifying the page you want to fetch  |                      None                       |
| remove        |          rm    | int (1,2,3...) Index no. of the song you want to remove. | Every song has an index in playlist. You can remove any song simply by number which is shown in playlist |  None |
| information   |      info      |                None                  | Shows raw information of current player config like pointer, total songs, volume etc.  |  None  |
| volume        |       v        | int (10,14,...any)                   | Sets the volume of current player to the given param| If no param is passed, then displays the current volume level |
| seek          |           sk   |      int (0-9)                       | seeks the song. Every song is scaled on scale of 10, pass any int in range 0-9 and player will autotically seek playback to specific interval based on song length   |                           None              |
| next          |      +1        |      None                            | Plays next song in playlist if available          |   None |
| previous      |      -1        |      None                            | Plays previous song in playlist if available          |   None |

# Customize your music player

Every setting of music player is defined in ```resonate_setting.py``` module. There is a data class holding all the important variables which you can customize according to your preferences.

## 1. Customizing the command aliases :

In ```resonate_settings.py```, there is a dict named ```CMD_ALIASES``` which holds all the available commands and their corresponding aliases as a list. you can define more than one aliases for one command (obviously...), keeping them unique for each command. 

<br>
Here is the snapshot of that dict representing how it is defined...

```
CMD_ALIASES = {
    'connect': [    ----> Original command
        'join',     ----> Alias
    ],              ----> A list of aliases
    'leave': [              ...
      'lv'
    ],
    'play': [
        'p',
    ],
    'stop': [
        's',
    ],
    'next': [
        '+1',
    ],
    
    ...
```

## 2. Enforcing music commands

Unlike all the commands of your bot, you may want to enforce music commands to a specific channel. This can be done by simply changing a variable ```RESTRICT_CMDS_TO_MUSIC_CHANNEL``` to ```True``` in ```resonate_settings.py``` inside the dataclass Config.

### If set to False (Default is False):
If this is set to ```False```, then music commands can be used from any channel of your server.

### If set to True :
If this is set to true then music commands will only be accessible from the provided channel. 
If set to ```True```, then  you also have to provide the id of the channel you want to use as music commands channel. To do this, set the variable ```MUSIC_CMD_CHANNEL``` to the channel id. for ex:

```
MUSIC_CMD_CHANNEL: int = 785846xxxxx
```

## 3. Player Volume :
A default volume is set to level : 50 when the player starts(which can be changed by command "v" later. If you want the default volume to something else, change the variable ```DEFAULT_VOLUME``` to desired value. 

The maximum limit of player is level 1000 but at that level, you'll be listening to ```zombies (not clear at all)```. 

To avoid the unpleasant experiance by setting the volume more than 100, maximum value is defined as ```MAX_VOLUME: int = 100```. 
But again, you are free to listen to the zombies by changing this variable in Config dataclass.

## 4. Logging :
The COG file comes with its prebuilt customized logger class which sits in ```resonate_utils``` directory as ```logger.py```. This will keep you updated for every event happening in your player.

To write the logs to a file, define the file location as variable ```LOG_FILE``` and set variable ```WRITE_LOGS``` as ```True``` in the ```resonate_settings.py``` . Default is set to ```LOG_FILE: str = "logs/music.log"```.

This logger also pukes the logs in STDOUT/console, if you dont want this behaviour, then set variable ```STDOUT_LOGS``` to ```False```.

<p id='serverconfigs'>
<h2>5. Server configs :</h2>

You must be hosting a lavalink server for this project (obviously), here is how you can define and set its configurations :

Inside the Config dataclass in ```resonate_settings.py``` :

```
MUSIC_HOST: str = "Host name here"
MUSIC_PORT: int = 80
REST_URI: str = "Host uri here"
MUSIC_SERVER_PW: str = os.environ.get('MUSIC_SERVER_PW') ----> set this environment variable for password (recommended).
MUSIC_SERVER_REGION: str = "your region"
```

</p>

...further docs will be added soon ...










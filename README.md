# resonate-beats 🎵
resonate-beats is a Discord COG file which can be integrated to any discord bot to add superb music streaming functionality to the existing bot.

## Setup
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

# Commands

Join the voice channel and run ```<your_prefix>join``` command to connect bot. The bot will join the voice channel in which the command invoker currently in, if no voice channel is found, the bot will show relevant message. 

Every command must be followed by yout command prefix like : ```<command_prefix>command```.


|  Command Name |  Command Alias |          Command Parameters          |                 Command Action                    |                 Extra note                  |
|---------------|----------------|--------------------------------------|---------------------------------------------------|---------------------------------------------|
| connect       |    join        |            channel name              | connect the bot to the voice channel              | Command invoker should be in voice channel  |
| play          |         p      | song_name/song_link/playlist_link    | Searches for the given params, will ask for the songs found and add that to the playlist.         | Resumes the playerif it is paused.|
| stop          |      s         |            None                      | Stops the player and clears the current playlist. |         None                                |
| pause         |     ps         |            None                      | Pauses the player.                                | To resume the player, use play command without params.|
| playlist      |       pl       | int (2,3,4...) Page no. of playlist  | The playlist shows limited songs by default, to traverse between all the songs, use pl command with an integer specifying the page you want to fetch  |                      None                       |
| remove        |          rm    | int (1,2,3...) Index no. of the song you want to remove. | Every song has an index in playlist. You can remove any song simply by number which is shown in playlist |  None |
| information   |      info      |                None                  | Shows raw information of current player config like pointer, total songs, volume etc.  |  None  |
| volume        |       v        | int (10,14,...any)                   | Sets the volume of current player to the given param| If no param is passed, then displays the current volume level |
| seek          |           sk   |      int (0-9)                       | seeks the song. Every song is scaled on scale of 10, pass any int in range 0-9 and player will autotically seek playback to specific interval based on song length   |                           None              |


# Customize your music player

... docs will be updated soon...



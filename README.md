# redQueen discord bot

Ths bot aims to automate much of the moderation and upkeep of the Women Only discord server. It's code can be applied to any server as long as the settings.example.json is adapted to fit the scheme used (and the file should be renamed to settings.json upon completion). redQueen is run via a remote server and accessed using FileZilla and PuTTY.

## Requirements

1. Python 3.5.3 or higher (Required by the python library)
1. discord.py `python3 -m pip install -U discord.py` (Discord updates frequently break the library so the most up to date version is recommended)

## How to run

The previously mentioned package(s) can be installed onto either the global path or a virual environment. After activating the environment run the entrypoint of the bot `main.py` and it should boot, printing a message to the console. 

###### Note

Much of this project references ID's. Viewing of these can be enabled in the client via `Settings > Appearance > Advanced > Developer Mode` and right-clicking elements of discord (Users, Channels, Messages, etc.). Most of these elements will have a context menu option that says "Copy ID". These are used throughout redQueen's commands and settings.json file.
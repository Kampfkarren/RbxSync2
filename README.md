# RbxSync2 - Like RbxSync only it doesn't take 80% of your CPU.

RbxSync2 is a rewrite of the [RbxSync server](https://github.com/evaera/RbxSync) to avoid the use of Electron. Note this is only the SERVER, and does not provide the plugin that RbxSync provides.

It is recommended not to update RbxSync until it has been confirmed the RbxSync2 server is prepared for it.

## Last Confirmed Working Build of RbxSync
v1.3.4 (BUILD 16)

## Downloads
~~RbxSync2 can be downloaded in the [releases section](https://github.com/boynedmaster/RbxSync2/releases/latest).~~

RbxSync2 must be made from source as of current. Use `pip install -r requirements.txt` to install the needed libraries, and then use `python rbxsync2.py` with Python >= 3.6.

RbxSync (the plugin) can be downloaded in [RbxSync's release section](https://github.com/evaera/RbxSync/releases/latest). Simply download it, run it, and then once the plugin has been installed, close the server and then run RbxSync2.

## Issues
There are many known issues with editing scripts inside studio and with your editor at the same time. It is recommended you only use your external editor to write scripts. 

There are also issues with scripts saving in the wrong places and files. There is not yet a repro case for this.

MoonScript is not supported currently, and is not a high priority. 

## Donate
RbxSync2 is free software. If you would like to fund this or other projects of mine, you can donate to me on [Patreon](https://www.patreon.com/kampfkarren). 

I am also trying to get into the developer forums on Roblox, so you can help out for free by making a nomination for me (Kampfkarren).

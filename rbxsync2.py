import json
import os
import re
import string
import time
from collections import defaultdict, OrderedDict
from flask import Flask, jsonify, request
from urllib.request import urlopen
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

app = Flask(__name__)
fileCache = {}
guidCache = {}
watchers = {}
updates = OrderedDict()

with open("./settings.json", "r") as _settings:
    settings = json.loads(_settings.read())

def get_setting(name):
    if name in settings:
        return settings[name]

    if name == "pluginPath":
        return os.path.join(os.getenv("localappdata"), "Roblox", "Plugins")
    elif name == "pmPath":
        return os.path.join(os.getenv("userprofile"), "Documents", "ROBLOX", "RSync")
    elif name == "tempPath":
        return os.path.join(os.getenv("temp"), "RSync")

with open(os.path.join(get_setting("pluginPath"), "RSync", "VERSION"), "r") as _plugin_version:
    plugin_version = int(_plugin_version.read())

@app.route("/new", methods=["POST"])
def new():
    data = request.get_json()

    if data["place_name"] in guidCache:
        for guid in guidCache[data["place_name"]]:
            os.remove(fileCache[guid])
    
    guidCache[data["place_name"]] = []

    return jsonify({
        "status": "OK",
        "app": "RSync",
        "pm": get_setting("pmPath"),
        "version": "rbxsync2",
        "build": plugin_version
    })

@app.route("/poll", methods=["GET"])
def poll():
    if len(updates) > 0:
        list_updates = updates.pop(list(updates.keys()).pop(0))
        update = list_updates[max(list_updates.keys())].copy()
        
        return jsonify({
            "type": "update",
            "data": update
        })

    return jsonify({})

extensions = defaultdict(str)
extensions["LocalScript"] = ".local"
extensions["ModuleScript"] = ".module"

syntax = defaultdict(lambda: ".rbxs")
syntax["lua"] = ".lua"
syntax["moon"] = ".moon"

class WriteHandler(FileSystemEventHandler):
    def __init__(self, data):
        self.data = data
    
    def on_modified(self, event):
        filename = event.src_path

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                if self.data["syntax"] == "lua":
                    if self.data["guid"] not in updates:
                        updates[self.data["guid"]] = {}
                    
                    updates[self.data["guid"]][time.time()] = {
                        "guid": self.data["guid"],
                        "source": file.read()
                    }

@app.route("/write/<action>", methods=["POST"])
def write(action):
    openAfter = action == "open"
    data = request.get_json()
    ext = extensions[data["class"]]
    fext = syntax[data["syntax"]]
    name = re.sub(r'[<>:"\/\\|?*]', '', data['name'])
    filename = f"{name}{ext}{fext}"
    filepath = os.path.join(get_setting("tempPath" if data["temp"] else "pmPath"), data["place_name"], re.sub(r'[<>:"\\|?*]', '', data["path"])) #HACK: Folder names with slashes won't work (not escaped). This is a client issue.
    file = os.path.join(filepath, filename)
    
    if fileCache.get(file) != data["guid"]:
        num = 1

        while fileCache.get(file) and fileCache[file] != data["guid"]:
            num += 1
            file = os.path.join(filepath, f"{name}{ext} ({num}){fext}")

    if not data["place_name"] in guidCache: #shouldnt happen but sometimes does?
        guidCache[data["place_name"]] = []
    
    guidCache[data["place_name"]].append(data["guid"])
    os.makedirs(filepath, exist_ok=True)

    with open(file, "w") as f:
        f.write(data["source"])
    
    if file not in fileCache:
        observer = Observer()
        observer.schedule(WriteHandler(data), filepath + "/", recursive=True)
        observer.start()

        watchers[file] = observer
    
    fileCache[file] = data["guid"]
    fileCache[data["guid"]] = file

    if openAfter:
        os.startfile(file)
    
    return "OK"

@app.route("/delete", methods=["POST"])
def delete():
    data = request.get_json()
    os.remove(fileCache[data["guid"]])
    return "OK"

if __name__ == "__main__":
    print("rbxsync2")
    app.run(port=21496)

from flask import Flask, request, redirect
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def bp():
    return os.path.abspath(os.path.dirname(__file__))

def getCreds():
    with open(f"{bp()}/creds.txt", "r") as f:
        id, secret = [i.lstrip().rstrip().split()[1] for i in f.readlines()]
    return id, secret

clientID, clientSecret = getCreds()

scope = 'user-library-read, user-read-private, user-read-playback-state, user-modify-playback-state'

app = Flask(__name__)

@app.route("/index")
@app.route("/")
def index():
    with open(f"{bp()}/index.html", "r") as f:
        html = f.read()
    return html

@app.route("/select", methods=["POST"])
def select():
    query = request.form.get("query", "")

    if query == "":
        return redirect("/")

    if query[0] == "~":
        command = query[1:].strip()
        if command == "purge-used":
            os.system(f"echo '' > {bp()}/used.dat")
        elif command == "lock":
            with open(f"{bp()}/lock.dat", "w") as lockF:
                lockF.write("1")
        elif command == "unlock":
            with open(f"{bp()}/lock.dat", "w") as lockF:
                lockF.write("0")
        elif command == "used":
            with open(f"{bp()}/used.dat", "r") as usedF:
                return usedF.read()

    sp = spotipy.Spotify(  \
        auth_manager=SpotifyOAuth(clientID, clientSecret, "http://www.google.co.uk", \
        scope=scope, cache_path=f"{bp()}/.cache", open_browser=False))

    devices = sp.devices()

    trackIDs = []
    trackLines = []
    results = sp.search(query)

    for item in results['tracks']['items']:
        trackIDs.append("spotify:track:" + item['id'])
        trackLines.append(item["name"] + " by " + ", ".join([a["name"] for a in item["artists"]]))

    with open(f"{bp()}/select.html", "r") as f:
        html = f.read()
        html = html.replace("@@trackoptions@@", makeTrackOptions(trackLines, trackIDs))

    return html

@app.route("/add", methods=["POST"])
def add():
    trackID = request.form.get("trackID")
    sp = spotipy.Spotify(  \
        auth_manager=SpotifyOAuth(clientID, clientSecret, "http://www.google.co.uk",\
        scope=scope, cache_path=f"{bp()}/.cache", open_browser=False))

    devices = sp.devices()

    usedF = open(f"{bp()}/used.dat", "r")
    used = usedF.readlines()
    used = [s.strip("\n").strip("\r") for s in used]
    usedF.close()

    if trackID not in used:

        message = "Successfully added to queue! Thanks!"

        try:
            deviceID = devices["devices"][0]["id"]
            try: ### likewise
                sp.add_to_queue(trackID, device_id=deviceID)
                usedF = open(f"{bp()}/used.dat", "a")
                usedF.write(trackID + "\n\r")
                usedF.close()
            except:  # debugging
                message = "Adding unsuccessful: Spotify Error."
        except:
            message = "Adding unsuccessful: No devices."

    else:
        message = "Track already recently queued!"

    with open(f"{bp()}/add.html", "r") as f:
        html = f.read()
        html = html.replace("@@message@@", message)

    return html

@app.route("/list")
def list():
    sp = spotipy.Spotify(  \
        auth_manager=SpotifyOAuth(clientID, clientSecret, "http://www.google.co.uk",\
        scope=scope, cache_path=f"{bp()}/.cache", open_browser=False))
    return "Not Implemented"

def makeDeviceOptions(devices):
    out = ""
    for dev in devices["devices"]:
        out += f"            <option>{dev['name']}</option>\n"
    return out

def makeTrackOptions(trackLines, uris):

    with open(f"{bp()}/lock.dat", "r") as lockF:
        locked = int(lockF.read())

    if locked:
        return "<div class='container'> Chune has been locked by the Admin, try again later!</div>"

    out = ""
    for name, uri in zip(trackLines, uris):
        out += f"                <button type='Submit' name='trackID' class='btn btn-primary' value='{uri}'>{name}</button>\n"
    return out

def devName2ID(devices, name):
    for dev in devices["devices"]:
        if dev["name"] is name:
            return dev["id"]

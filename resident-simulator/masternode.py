"Manages uploading to the metrics server."

import json
import requests
import datetime
import itertools
import sys#debug

thisWorld = None
creds = None
dtStart = None
nRequests = 0

HTTP_HEADER = {
    "Connection" : "close"
}

def sendData(packet_body):
    global nRequests
    res = requests.post("http://api1.localhost:3001/upload", packet_body, headers=HTTP_HEADER)
    res.raise_for_status()
    res.close()
    nRequests += 1

def updateDatabase():
    global nRequests
    # upload sensor data
    world_state = thisWorld.GetState()
    state = world_state[0]
    time = state["time"]
    
    # Upload the state of every room
    for room in state["rooms"]:
        rn = room["room_name"].lower()
        assets = room["assets"]
        for asset in assets:
            asset_name = asset['name']
            for propertykey in itertools.filterfalse(lambda key: key == 'name', asset.keys()):
                access_token = creds[propertykey][asset_name]
                value = asset[propertykey]
                sendData({"access_token": access_token, "labels": time, "data": value})
    
    # Upload building variables
    building_vars = state['variables']
    for variable in building_vars:
        access_token = creds[variable]
        value = building_vars[variable]
        sendData({"access_token": access_token, "labels": time, "data": value})

    #total_seconds = thisWorld.GetDateTime().strftime('%s')
    #sendData({"access_token": creds["clock"], "labels":time, "data": total_seconds})

    # profile performance
    tdseconds = (datetime.datetime.now() - dtStart).total_seconds()
    if int(tdseconds) % 15 == 0:
        #print ("Average requests per second: %f" % (nRequests / 15))
        nRequests = 0

def connect(world):
    global dtStart
    global thisWorld
    global creds
    dtStart = datetime.datetime.now()
    thisWorld = world
    login_info = open("sensor_credentials.json", "r")
    creds = json.load(login_info)["credentials"]
    login_info.close()

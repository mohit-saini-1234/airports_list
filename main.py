import haversine as hs
from haversine import Unit
import json
from flask import Flask, abort, jsonify, request


app = Flask(__name__)

with open('airports.json', 'r') as f:
    airports_list = json.load(f)
    


#funcrion for sort 
def extract_time(json):
    try:
        return int(json['distance'])
    except KeyError:
        return 0




#route for get all airports list
@app.route('/get_list' , methods=['GET'])
def get_Airportslist():
    get_list= [distro for distro in airports_list]
    return jsonify(get_list) 


#distence between two airports by objectID
@app.route('/distance' , methods=['GET'])
def get_Distance():
    SiteNumber1 = request.json.get("SiteNumber1")
    SiteNumber2 = request.json.get("SiteNumber2")
    
    for keyval in airports_list:
        if SiteNumber1.lower() == keyval['SiteNumber'].lower():
            print(keyval['Lat'])
            Lat1 =keyval['Lat']
            Lon1 =keyval['Lon']
            Loc1 =(Lat1,Lon1)
        if SiteNumber2.lower() == keyval['SiteNumber'].lower():
            Lat2 =keyval['Lat']
            Lon2 =keyval['Lon']
            Loc2 =(Lat2,Lon2)
    Distance = hs.haversine(Loc1,Loc2, unit=Unit.MILES)
    return jsonify(Distance)
    
    

@app.route('/get_nearby', methods=['GET'])
def nearby_Airport():
    user_lat = request.json.get("Lat")
    user_lon = request.json.get("Lon")
    loc=(user_lat,user_lon)
    find_inlist = [x for x in airports_list]
    distance = []
    for doc in find_inlist:
        LAT = doc["Lat"]
        LON = doc["Lon"]
        LOC = (LAT,LON)
        distance.append({"distance":hs.haversine(loc,LOC, unit=Unit.MILES),"name":doc["City"]}) 
    distance.sort(key=extract_time, reverse=True)
    nearests= distance[-3:]
    return jsonify(nearests)



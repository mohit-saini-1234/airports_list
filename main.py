import json
from flask import Flask , request , abort , jsonify
import haversine as hs
from haversine import Unit

app =Flask(__name__)
with open('airports.json', 'r') as f:
    distros_dict = json.load(f)


#funcrion for sort 
def extract_time(json):
    try:
        return int(json['distance'])
    except KeyError:
        return 0

@app.route('/get_list', methods=['GET'])
def get_List():
    user =[distro for distro in distros_dict]
    return jsonify(user)



@app.route('/distance', methods=['GET'])
def get_dis():
    SiteNumber1 = request.json.get("SiteNumber1")
    SiteNumber2 = request.json.get("SiteNumber2")
    
    for keyval in distros_dict:
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

@app.route('/nearby', methods=['GET'])
def get_Nearby():
    user_lat = request.json.get("Lat")
    user_lon = request.json.get("Lon")
    loc=(user_lat,user_lon)
    find_inlist =[x for x in distros_dict]
    distance=[];    
    for doc in find_inlist:
        LAT = doc["Lat"]
        LON = doc["Lon"]
        LOC = (LAT,LON)
        distance.append({"distance":hs.haversine(loc,LOC, unit=Unit.MILES),"name":doc["City"]}) 
    distance.sort(key=extract_time, reverse=True)
    nearests= distance[-3:]
    return jsonify(nearests)


if __name__ == "__main__":
    app.run()
    
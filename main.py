import haversine as hs
from haversine import Unit
import json
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import pymongo
from flask import Flask, abort, jsonify, request





app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://1111111111:1111111111@cluster0.tzzym.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)


def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


#funcrion for sort 
def extract_time(json):
    try:
        return int(json['distance'])
    except KeyError:
        return 0

#route for add airports list 
@app.route('/add_list' , methods=['POST'])
def add_List():
    tasks = request.json.get("airport_lists")
    List =[i for i in mongo.db.airport_list.insert(tasks)]
    return str(List)



#route for get all airports list
@app.route('/get_list' , methods=['GET'])
def get_Airportslist():
    find_list = mongo.db.airport_list.find()
    get_list= [serialize_doc(doc) for doc in find_list]
    return jsonify(get_list) 


#distence between two airports by objectID
@app.route('/distance' , methods=['GET'])
def get_Distance():
    airport_one = request.json.get("airport_one")
    airport_two = request.json.get("airport_two")
    
    airport_id1 = mongo.db.airport_list.find_one({"_id": ObjectId(airport_one)})   
    
    lat1 = airport_id1["Lat"]
    lon1 = airport_id1["Lon"]
    loc1 = (lat1,lon1)
    
    airport_id2 = mongo.db.airport_list.find_one({"_id": ObjectId(airport_two)})  
    lat2 = airport_id2["Lat"]
    lon2 = airport_id2["Lon"]
    loc2 = (lat2, lon2)
    Distance = hs.haversine(loc1,loc2, unit=Unit.MILES)
    return jsonify(Distance)
    
    

@app.route('/get_nearby', methods=['GET'])
def nearby_Airport():
    user_lat = request.json.get("Lat")
    user_lon = request.json.get("Lon")
    loc=(user_lat,user_lon)
    find_inlist = mongo.db.airport_list.find({},{"Lat": 1 , "Lon": 1 , "City":1})
    distance = []
    for doc in find_inlist:
        LAT = doc["Lat"]
        LON = doc["Lon"]
        LOC = (LAT,LON)
        distance.append({"distance":hs.haversine(loc,LOC, unit=Unit.MILES),"name":doc["City"]}) 
    distance.sort(key=extract_time, reverse=True)
    nearests= distance[-3:]
    return jsonify(nearests)
    
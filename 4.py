# Q4. Write an API to remove null values from Database and replace those values with empty string

from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import numpy as np
import pymongo

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
mydb =myclient["crud"]
app.config['MONGO_URI'] = "mongodb://localhost:27017/crud"
mycol = mydb["data"]


mongo = PyMongo(app)

data = {'birds': ['Cranes', 'Cranes', 'plovers', 'spoonbills', 'spoonbills', 'Cranes', 'plovers', 'Cranes', 'spoonbills', 'spoonbills'], 'age': [3.5, 4, 1.5, np.nan, 6, 3, 5.5, np.nan, 8, 4], 'visits': [2, 4, 3, 4, 3, 4, 2, 2, 3, 2], 'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}
df = pd.DataFrame(data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
x=mycol.insert_many([
    {"birds":"Cranes","age":3.5,"visits":2,"priority":"yes"},
    {"birds":"Cranes","age":4.0,"visits":4,"priority":"yes"},
    {"birds":"plovers","age":1.5,"visits":3,"priority":"no"},
    {"birds":"spoonbills","age":None,"visits":4,"priority":"yes"},
    {"birds":"spoonbills","age":6.0,"visits":3,"priority":"no"},
    {"birds":"Cranes","age":3.0,"visits":4,"priority":"no"},
    {"birds":"plovers","age":5.5,"visits":2,"priority":"no"},
    {"birds":"Cranes","age":None,"visits":2,"priority":"yes"},
    {"birds":"spoonbills","age":8.0,"visits":3,"priority":"no"},
    {"birds":"spoonbills","age":4.0,"visits":2,"priority":"no"}
    ])   

#update api
@app.route('/update/',methods=['PUT'])
def update_db():
    myquery = {"age":None}
    newvalue = {"$set":{"age":' '}}
    result = mycol.update_one(myquery,newvalue)
    resp = jsonify("User updated successfully")
    resp.status_code = 200
    return resp   
      
      
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found'+request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp                                           

if __name__ == "__main__":
    app.run(debug=True)

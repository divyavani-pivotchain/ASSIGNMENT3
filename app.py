# Q1.Perform CRUD operations using Flask API connected to MongoDB. CRUD(Create a database,Read data from Database,Update the database, Delete any entries in database. The methods should be hit using postman, So install Postman

from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/crud"

mongo = PyMongo(app)

#create api
@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _city = _json['city']

    if _name and _email and _city and request.method == 'POST':
        id = mongo.db.user.insert({'name':_name,'email':_email,'city':_city})

        resp = jsonify("User added successfully")

        resp.status_code = 200
        return resp
    else:
        return not_found()

#get api
@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

#get api in specific user
@app.route('/users/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

#delete api
@app.route('/delete/<id>' ,methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User delete successfully")
    resp.status_code = 200
    return resp

#update api
@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _city = _json['city']

    if _name and _email and _city and _id and request.method == 'PUT':
        mongo.db.user.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{'name':_name,'email':_email,'city':_city}})
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
    app.run(port=5100,debug=True)

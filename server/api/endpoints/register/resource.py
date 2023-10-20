from flask import Flask, request, jsonify
from app import app
from users.model import User


@app.route("/register", methods=["POST"])
def registerNewUser():
    #TODO Catch, if the user already exists authorize / authenticate
    data = request.get_json()
    
    #from the received data create new user in database
    userId = User(id=None,
                name=data['name'], 
                email=data['email'])
    
    # get the id of that user and return it
    # everytime the frontend makes a call, it needs to add the userid / subjectid /documentid/ etc. if necessary for the call
    
    
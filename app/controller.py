from flask import render_template, request, jsonify
import json
import pymongo
import os
import dotenv
from pymongo import MongoClient

dotenv.load_dotenv()
dbuser = os.environ.get("DBUSER","")
dbpass = os.environ.get("DBPASS","")

def index():
    return render_template('index.html')

def regist():
    return render_template('register.html')

def login():
    #body = request.get_json()
    email = request.form.get("email")
    password = request.form.get("password")
    
    try:
        uri = f"mongodb+srv://{dbuser}:{dbpass}@mydb.rvfulzg.mongodb.net/?retryWrites=true&w=majority&appName=myDB"
        client = MongoClient(uri)
        database = client["baba"]
        collection = database["users"].find_one({"username" : email, "password" : password})
        print(collection)
        client.close()
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
        
    if collection is not None and len(collection) > 0:
        return jsonify({
            "status" : 200,
            "message" : "Berhasil login !",
            "data" : None
        })
    return jsonify({
            "status" : 401,
            "message" : "Gagal login !",
            "data" : None
        })
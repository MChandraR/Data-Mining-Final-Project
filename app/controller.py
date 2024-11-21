from flask import render_template, request, jsonify, Response
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

def getPenjualan():
    try:
        uri = f"mongodb+srv://{dbuser}:{dbpass}@mydb.rvfulzg.mongodb.net/?retryWrites=true&w=majority&appName=myDB"
        client = MongoClient(uri)
        database = client["baba"]
        collection = database["penjualan"].find().sort('waktu', pymongo.DESCENDING)
        print(collection)
        client.close()
        data = []
        for res in collection:
            data.append({
                "_id" : str(res["_id"]),
                "aroma" : res["aroma"],
                "waktu" : res["waktu"],
                "jumlah" : res["jumlah"]
            })        

        print(data)
        
        return jsonify({
            "status" : 200,
            "message" : "Berhasil mengambil data !",
            "data" : data
        })
    
    
    except Exception as e:
        return jsonify({
            "status" : 201,
            "message" : "Gagal mengambil data !" + e,
            "data" : None
        })


def input():
    if request.method=="GET": return render_template('input.html')
    
    payload = request.get_json()
    
    if(payload["aroma"] == "" or payload["waktu"] == "" or payload["jumlah"] == ""):
        return jsonify({
            "status" : 201,
            "message" : "Gagal : Harap periksa kembali data !",
            "data" :payload
        })

    
    try:
        uri = f"mongodb+srv://{dbuser}:{dbpass}@mydb.rvfulzg.mongodb.net/?retryWrites=true&w=majority&appName=myDB"
        client = MongoClient(uri)
        database = client["baba"]
        collection = database["penjualan"].insert_one({
            "aroma" : payload["aroma"],
            "waktu" : payload["waktu"],
            "jumlah" : payload["jumlah"],
        })
        print(collection)
        client.close()
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    
    return jsonify({
        "status" : 200,
        "message" : "Berhasil",
        "data" :payload
    })

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
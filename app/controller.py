from flask import render_template, request, jsonify
import json

def index():
    return render_template('index.html')

def login():
    body = request.get_json()
    if body["username"] == "admin" and body["password"] == "1234":
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
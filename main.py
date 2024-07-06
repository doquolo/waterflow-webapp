from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db, firestore
import json
import argon2

# init firebase
databaseURL = "https://waterflow-583e8-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": databaseURL})
firestore = firestore.client()

# init hasher
hasher = argon2.PasswordHasher()

# init flask
app = Flask(__name__)

@app.route("/getUserData", methods=["POST"])
def getUserData():

    jsondata = json.loads(request.data)

    username = jsondata["user"]
    password = jsondata["password"]

    try:
        user = firestore.collection("users").document(str(username)).get()
        user = user.to_dict()
        if (user != None):
            isPasswordCorrect = hasher.verify(user["password"], password)
        elif (user == None or not isPasswordCorrect):
            return {"state": "authenticate"}
        elif (isPasswordCorrect):
            device_list = []
            for device in user["devices"]:
                device_list.append(device)
            if (len(device_list) == 0): return {"state": "notfound"}  
            return {"state": "found", "data": {"machines": device_list}}
    except Exception as e:
        return {"e": e}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getdata")
def getdata():
    timestamp = request.args.get('date')
    date = timestamp[0:2]
    month = timestamp[2:4]
    year = timestamp[4:8]
    device_id = request.args.get('deviceid')
    ref_path = f"/{device_id}/{int(year)}/{int(month)}/{int(date)}/"
    try:
        ref = db.reference(ref_path)
        data = ref.get()
        if (data == None): raise ValueError
        return data
    except:
        return {"error": 'true', "reason": 'date not exist'}

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)



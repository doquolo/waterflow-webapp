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

# home
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getUserData", methods=["POST"])
def getUserData():
    jsondata = json.loads(request.data)

    username = jsondata["user"]
    password = jsondata["password"]

    try:
        user = firestore.collection("users").document(str(username)).get()
        user = user.to_dict()
        print(user)
        if (user == None): return {"state": "authenticate"}
        else:
            try:
                isPasswordCorrect = hasher.verify(user["password"], password)
                if (isPasswordCorrect):
                    device_list = []
                    for device in user["devices"]:
                        device_list.append(device)
                    if (len(device_list) == 0): return {"state": "notfound"}  
                    return {"state": "found", "data": {"machines": device_list}}
            except Exception as e:
                return {"state": "authenticate"}
    except Exception as e:
        return {"e": e}

@app.route("/getData")
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

@app.route("/getMonthData")
def getMonthData():
    timestamp = request.args.get('date')
    month = timestamp[0:2]
    year = timestamp[2:6]
    device_id = request.args.get('deviceid')
    ref_path = f"/{device_id}/{int(year)}/{int(month)}/"
    try:
        ref = db.reference(ref_path)
        data = ref.get()
        if (data == None): raise ValueError
        return data
    except:
        return {"error": 'true', "reason": 'date not exist'}
    

# admin
@app.route("/admin")
def adminPanel():
    return render_template("admin.html")

@app.route("/getAdminData", methods=["POST"])
def getAdmin():
    jsondata = json.loads(request.data)

    username = jsondata["user"]
    password = jsondata["password"]

    try:
        user = firestore.collection("admins").document(str(username)).get()
        user = user.to_dict()
        if (user == None): return {"state": "authenticate"}
        else:
            try:
                isPasswordCorrect = hasher.verify(user["password"], password)
                if (isPasswordCorrect):
                    return {"state": "found"}
            except Exception as e:
                return {"state": "authenticate"}
    except Exception as e:
        return {"e": e}

@app.route("/getAllUserData")
def getAllUserData():
    userlist = []
    users = firestore.collection("users").stream()
    for user in users:
        userlist.append({
            'username': user.id,
            'devices': user.to_dict()['devices']
        })
    return userlist

@app.route("/delUser")
def delUser():
    username = request.args.get('username')
    try:
        firestore.collection("users").document(str(username)).delete()
    except Exception as e:
        return {"state": "error", "error": e}
    return {"state": "done"}    

@app.route("/newLink")
def newLink():
    username = request.args.get('username')
    id = request.args.get('deviceid')
    try:
        devicelist = firestore.collection("users").document(username).get().to_dict()['devices']
        devicelist.append(id)
        firestore.collection("users").document(username).update({"devices": devicelist})
    except Exception as e:
        return {"state": "error", "error": e}
    return {"state": "done"}    

@app.route("/unlink")
def unlink():
    username = request.args.get('username')
    id = request.args.get('deviceid')
    try:
        devicelist = firestore.collection("users").document(username).get().to_dict()['devices']
        devicelist.remove(id)
        firestore.collection("users").document(username).update({"devices": devicelist})
    except Exception as e:
        return {"state": "error", "error": e}
    return {"state": "done"}    

@app.route("/registerNewUser", methods=['POST'])
def registerNewUser():
    jsondata = json.loads(request.data)

    username = jsondata["user"]
    hash = jsondata["hash"]
    try:
        firestore.collection("users").document(str(username)).set({
            "devices": [],
            "password": str(hash)
        })
    except Exception as e:
        return {"state": "error", "error": e}
    return {"state": "done"}    

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)



from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db, firestore
import json

# init firebase
databaseURL = "https://waterflow-583e8-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": databaseURL})
firestore = firestore.client()

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
        if (user == None):
            return {"state": "authenticate"}
        elif (user["password"] == str(password)):
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
    date = request.args.get('date')
    device_id = request.args.get('deviceid')
    ref_path = f"/{device_id}/"
    all_dates = list(db.reference(ref_path).get().keys())
    print(all_dates)
    if (date in all_dates):
        ref = db.reference(f"{ref_path}{date}")
        data = ref.get()
        return data
    else:
        return {"error": 'true', "reason": 'date not exist'}

@app.route("/testDB")
def testDB():
    users = firestore.collection("users").document("noc").get()
    return users.to_dict()

app.run("0.0.0.0", debug=True)



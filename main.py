from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db
import json

# init firebase
databaseURL = "https://waterflow-583e8-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": databaseURL})

# init flask
app = Flask(__name__)

def authenticateUser(username, password):
    # 1 - success; 2 - wrong password; 3 - user not found
    # TODO: implement a function that verify user cred with firebase db
    # placeholder

    data = None
    with open("user.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())

    try:
        if (data[username] == password):
            return 1
        else:
            return 2
    except Exception:
        return 3


@app.route("/retriveLinkedMachine", methods=["POST"])
def retriveLinkedMachine():

    jsondata = json.loads(request.data)

    print(jsondata)

    username = jsondata["user"]
    password = jsondata["password"]

    print(username)
    print(password)


    data = None
    with open("linked_machine.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
        if (authenticateUser(username, password) not in (2, 3)):
            if (username in data.keys()):
                return {"state": "found", "data" : data[username]}
            return {"state": "notfound"}
        return {"state": "authenticate"}



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

app.run("0.0.0.0", debug=True)

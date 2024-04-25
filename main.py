from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db

# init firebase
databaseURL = "https://waterflow-583e8-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": databaseURL})

# init flask
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getdata")
def getdata():
    date = request.args.get('date')
    all_dates = list(db.reference('/').get().keys())
    print(all_dates)
    if (date in all_dates):
        ref = db.reference(f"/{date}")
        data = ref.get()
        return data
    else:
        return {"error": 'true', "reason": 'date not exist'}

app.run("0.0.0.0", debug=True)


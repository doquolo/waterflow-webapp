import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('creds.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

users = db.collection("users")

print(users.document("noc").get().to_dict())
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./plaid-generic-14913cb13710.json")
app = firebase_admin.initialize_app(cred)


class FirestoreClient:
    def __init__(self):
        db = firestore.client()

        self.Items = db.collection("items")


client = FirestoreClient()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./plaid-generic-14913cb13710.json")
app = firebase_admin.initialize_app(cred)


class FirestoreClient:
    def __init__(self):
        self.db = firestore.client()

        self.Items = self.db.collection("items")

fs_client = FirestoreClient()
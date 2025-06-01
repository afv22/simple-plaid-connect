from firebase_admin import firestore
from app.services.firebase import initialize_firebase

initialize_firebase()


class FirestoreClient:
    def __init__(self):
        db = firestore.client()

        self.Items = db.collection("items")


client = FirestoreClient()

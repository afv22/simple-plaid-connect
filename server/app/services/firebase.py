import os

import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "firebase-cert.json")

    # Check if Firebase Admin is already initialized
    if not firebase_admin._apps:
        # If running in production environment like Google Cloud, use default credentials
        if os.getenv("GAE_ENV", "").startswith("standard"):
            cred = credentials.ApplicationDefault()
        else:
            # For local development, use the service account file
            cred = credentials.Certificate(cred_path)

        firebase_admin.initialize_app(cred)

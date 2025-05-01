## Server
Simple Flask server to handle the Plaid account link flow. Stores the access tokens in Firestore.


To run the server:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install waitress
waitress-serve --port=5001 --call server:create_app
```

Must generate a Firebase cert and save it to this directory. Create a private key for a service user in the [Google Cloud console](https://console.cloud.google.com/iam-admin/serviceaccounts).

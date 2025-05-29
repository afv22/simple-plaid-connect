# Simple Plaid Connect

A simple web application that demonstrates integration with Plaid API and Firebase Authentication.

## Features

- Firebase Authentication with Google Sign-in
- Protected frontend routes requiring authentication
- Integration with Plaid API
- Secure backend with token verification

## Prerequisites

- Docker and Docker Compose installed
- Plaid API credentials
- Firebase account with a service account key
- Google Sign-in configured in Firebase Authentication

## Running with Docker

### Setup Environment Variables

Create a `.env` file in the project root with your Plaid API credentials:

```
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET_SANDBOX=your_sandbox_secret
PLAID_SECRET_PRODUCTION=your_production_secret
PLAID_ENV=sandbox
PLAID_PRODUCTS=transactions
PLAID_COUNTRY_CODES=US
```

### Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Add a web app to your Firebase project and get the configuration
3. Enable Google authentication in the Firebase Authentication section
4. Generate a Firebase Admin SDK service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file securely
5. Update the `.env` file in the client directory with your Firebase configuration
6. Update the server `.env` file with the path to your service account key

### Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The services will be available at:

- Client: http://localhost:8080
- Server API: http://localhost:5001/api

## Development Setup

### Client Setup

```bash
cd client
cp .env.example .env  # Edit with your Firebase config
npm install
npm run dev
```

### Server Setup

```bash
cd server
cp .env.example .env  # Edit with your Plaid and Firebase credentials
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

See the README files in the `client/` and `server/` directories for more details.

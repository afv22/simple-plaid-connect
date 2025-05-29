## Plaid Connect

Creating a simple interface to generate Plaid access tokens that can be used in other projects.

## Prerequisites

- Docker and Docker Compose installed
- Plaid API credentials
- Firebase credentials (saved as `firebase-cert.json` in the project root)

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

### Firebase Certificate

Place your Firebase service account certificate in the project root as `firebase-cert.json`.

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

For development without Docker, see the README files in the `client/` and `server/` directories.

# Apple CLI V2

A full-stack portfolio management application with a Flask backend and a React frontend, authenticated via AWS Cognito OIDC.

## Backend

The Flask backend provides RESTful APIs for user management, portfolio CRUD, securities lookup, and trade execution.

### Setup

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in Cognito values
5. Run: `flask run`

### Testing

```bash
pytest --cov=app --cov-report=term-missing
```

## Frontend

The React frontend integrates with the backend and authenticates users via AWS Cognito's OIDC Hosted UI using the Authorization Code Flow. See [`frontend/README.md`](frontend/README.md) for full setup instructions.

### Quick Start

```bash
cd frontend
cp .env.example .env  # then fill in Cognito values
npm install
npm run dev
```

Visit http://localhost:5173/.
# Apple CLI Portfolio Manager

## Setup Instructions

This project includes a Flask backend and a Vite+React frontend.

### Backend

1. Create a virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `flask run`

### Frontend

1. Ensure Node.js (18+) is installed.
2. Navigate to frontend: `cd frontend`
3. Install dependencies: `npm install`
4. Set up `.env` using `.env.example`
5. Run: `npm run dev`

### Features
- OIDC Authentication with AWS Cognito
- View, create, and delete portfolios
- Trade securities on the market
- Track portfolio holdings and transaction history
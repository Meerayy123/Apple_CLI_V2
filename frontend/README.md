# Apple CLI V2 — Frontend

React frontend for the Apple CLI Portfolio Manager, authenticated via AWS Cognito OIDC.

## Prerequisites

- Node.js 18+ and npm
- A running backend at `http://localhost:5000`
- An AWS Cognito User Pool configured per the project's auth setup

## Installation

```bash
cd frontend
npm install
```

## Environment Configuration

Copy `.env.example` to `.env` and fill in the values from your Cognito User Pool:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the Flask backend (e.g., `http://localhost:5000`) |
| `VITE_COGNITO_AUTHORITY` | Cognito OIDC issuer URL (`https://cognito-idp.<region>.amazonaws.com/<pool-id>`) |
| `VITE_COGNITO_CLIENT_ID` | Cognito app client ID (public, no client secret) |
| `VITE_COGNITO_DOMAIN` | Cognito Hosted UI domain (e.g., `https://<prefix>.auth.<region>.amazoncognito.com`) |
| `VITE_COGNITO_REDIRECT_URI` | OAuth callback URL (`http://localhost:5173/callback`) |
| `VITE_COGNITO_LOGOUT_URI` | Post-logout redirect URL (`http://localhost:5173/`) |
| `VITE_COGNITO_SCOPE` | OIDC scopes (`openid email profile`) |

## Running Locally

```bash
npm run dev
```

The dev server runs on `http://localhost:5173`, which is the URL configured in Cognito's allowed callback list.

## Building for Production

```bash
npm run build
npm run preview
```

## Cognito Configuration Requirements

The Cognito User Pool app client must be configured with:

- **App client type:** Single-page application (public, no client secret)
- **Authorization code grant** enabled
- **Allowed callback URL:** `http://localhost:5173/callback`
- **Allowed sign-out URL:** `http://localhost:5173/`
- **OpenID Connect scopes:** `openid`, `email`, `profile`

## Project Structure

```
frontend/src/
  main.jsx                    Entry: wraps App in AuthProvider and BrowserRouter
  App.jsx                     Route definitions
  index.css                   Global reset and base styles
  auth/
    authConfig.js             react-oidc-context config object built from env vars
    ProtectedRoute.jsx        Wrapper that redirects to /login if not authenticated
    useUsername.js             Hook to extract username from auth.user
  api/
    client.js                 Fetch wrapper with token attach + error handling
    portfolios.js             Portfolio API functions
    trades.js                 Trade API functions
  pages/
    LoginPage.jsx             Sign-in page with Cognito redirect
    CallbackPage.jsx          Handles OAuth callback and redirects
    PortfoliosListPage.jsx    List portfolios, create, delete
    PortfolioDetailPage.jsx   Holdings, buy/sell forms, transaction history
  components/
    NavBar.jsx                Navigation with sign-out
    PortfolioCard.jsx         Single portfolio card with view/delete
    CreatePortfolioForm.jsx   Controlled form for portfolio creation
    HoldingsTable.jsx         Holdings table with refresh support
    TransactionsTable.jsx     Transaction history table
    BuyForm.jsx               Buy order form with validation
    SellForm.jsx              Sell order form with validation
    ErrorBanner.jsx           Error message display
    LoadingSpinner.jsx        Loading indicator
```

## Features

- **Authentication (25%):** OIDC Authorization Code Flow via Cognito Hosted UI. Tokens in sessionStorage. ProtectedRoute redirects unauthenticated users. Logout clears session and redirects to Cognito /logout.
- **Portfolio management (25%):** List, create, and delete portfolios. Empty state messaging. Error surfacing from backend.
- **Holdings and trading (25%):** Holdings table per portfolio. Buy and sell forms with validation, loading states, and error handling. Trade completion refreshes holdings and transactions.
- **Transaction history (10%):** Reverse chronological transaction table. Formatted timestamps and prices.
- **Code quality and project structure (10%):** Clean component separation. Shared API client with typed errors. No console.log of tokens. No localStorage. No CSS framework.
- **Version control (5%):** Feature branch, phase-based commits, PR left open.

## Known Limitations

- Logout uses Cognito's `/logout` endpoint, which terminates the session globally. After logout the user lands on `/`, which redirects to `/login`.
- Silent token renewal depends on Cognito's session cookie; if the cookie expires, the user is redirected to login.

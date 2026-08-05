# NCNL Coffee frontend

Production-ready frontend for the Coffee House backend. Built with React, TypeScript and Vite.

## Features

- RU/EN interface and light/dark themes;
- public menu with backend categories, server search and incremental loading;
- persistent local basket and public table booking, pre-order and event requests;
- administrator sign-in and admin-code registration through the real backend, with HttpOnly cookie authentication;
- protected requests dashboard with server filters, pagination and 25-second polling;
- responsive layout, keyboard focus states, error/empty/loading states and an error boundary.

## Local development

Requirements: Node.js 20+ and the backend running on `http://localhost:8000`.

```bash
npm ci
npm run dev
```

Vite proxies `/api`, `/auth`, `/users`, `/admin` and `/health` to the local backend. The browser therefore keeps the backend HttpOnly cookie without a token in web storage.

For a separately hosted production API, copy `.env.example` to `.env.production` and set `VITE_API_BASE_URL`. The backend CORS and cookie settings must allow that origin.

## Quality checks

```bash
npm run build
npm run lint
npm test
```

## Backend limitations respected by this frontend

- Public catalog shows only active categories and available items because these are the only public read endpoints.
- The admin dashboard manages customer requests only.
- Notifications are not displayed because the backend currently exposes no notification HTTP endpoints.
- Polling is used instead of realtime because the backend exposes no WebSocket or SSE endpoint.

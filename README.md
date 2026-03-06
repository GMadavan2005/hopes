# Soundlog Music Discovery App

A full-stack music discovery platform with AI-powered search, multiple music API integrations, sentiment analysis, and a React frontend built with Vite + shadcn-ui.

---

## Project Overview

This repository contains two main parts:

1. **backend** – FastAPI server written in Python. Provides smart search, artist info, review sentiment, user preferences, and integrates with Gemini AI, MusicBrainz, Last.fm, iTunes, and AudioDB.
2. **frontend** – React/TypeScript application powered by Vite and Tailwind CSS. Uses React Query to call backend endpoints and render the UI.

Continue reading for setup instructions.

## Project info

**URL**: https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID

## Getting Started

To run the project locally you'll need Node.js (for the frontend) and Python 3.11+ (for the backend). The repository uses a virtual environment for Python and npm/yarn for the frontend.

### Backend setup

```bash
cd backend
python -m venv venv            # create virtual environment
venv\Scripts\activate         # Windows; use `source venv/bin/activate` on macOS/Linux
pip install -r requirements.txt # install dependencies
cp .env.example .env            # create your own environment file
# edit `.env` with API keys and database URL
```

Once the backend is configured you can start the server:

```bash
cd backend
venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

The API will listen on `http://localhost:8000` and exposes endpoints like `/api/search`, `/api/artist/{mbid}`, etc.

### Frontend setup

```bash
cd ..                # root of repo
npm install
npm run dev          # starts Vite dev server on http://localhost:5173
```

The frontend expects `VITE_BACKEND_URL` in `.env` (e.g. `http://localhost:8000`).

### Running both

You can open two shells and run the backend and frontend commands above simultaneously. Optionally install [`concurrently`](https://www.npmjs.com/package/concurrently) and add a script to `package.json` if you prefer.

---

# How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

(Note: the original README content below is generic; the section above contains project-specific instructions only.)

Simply visit the [Lovable Project](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)

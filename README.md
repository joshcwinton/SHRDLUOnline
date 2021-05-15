# SHRDLUOnline

Frontend:
Josh Winton, Jasper Cheung
Backend:
Saurav Hossain, Donald Chen

## Setup

### Frontend

#### Requirements

- Node

#### Getting Started

1. `cd frontend`
2. `npm i`
3. `npm start`

### Backend

- Python 3
- Download model file from drive and move file to backend/
- Download database secret file from drive and move file to backend/

#### Getting Started

1. `cd backend`
2. `python3 -m pip install -r requirements.txt`
3. `python3 app.py`

## Deployment

### Add remotes

1. `heroku git:remote --remote heroku-shrdluonline-backend -a shrdluonline-backend`
2. `heroku git:remote --remote heroku-shrdluonline-frontend -a shrdluonline-frontend`

### Deploy

1. `git subtree push --prefix frontend heroku-shrdluonline-frontend main`
2. `git subtree push --prefix backend heroku-shrdluonline-backend main`

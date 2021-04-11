# SHRDLUOnline 
Frontend:
Josh Winton, Jasper Cheung
Backend:
Saurav Hossain, Donald Chen

## Setup

### Frontend

#### Requirements
- `Node`

#### Getting Started

1. `cd frontend`
2. `npm i`
3. `npm start`

### Backend

#### Requirements
- `Pillow==8.1.2`
- `spacy==3.0.3`
- `en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl`
- `flask==1.1.2`
- `flask-cors==3.0.10`

#### Getting Started
1. `cd backend`
2. `python routes.py`



## Deployment

### Add remotes
1. `heroku git:remote --remote heroku-shrdluonline-backend -a shrdluonline-backend`
2. `heroku git:remote --remote heroku-shrdluonline-frontend -a shrdluonline-frontend`

### Deploy
1. `git subtree push --prefix frontend heroku-shrdluonline-frontend main`
2. `git subtree push --prefix backend heroku-shrdluonline-backend main`

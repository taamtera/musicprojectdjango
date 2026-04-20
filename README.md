# Chithara AI Music Generator - Web Application

This repository contains the fully built, consolidated web application for the Chithara AI Music Generator. It is cleanly separated into two distinct Django apps: `frontend` (managing templates, UI, and views) and `backend` (managing all database models and schemas).

## Project Setup

### Prerequisites
- Python 3.10+
- Django 6.0+ (required for official MongoDB backend)
- MongoDB Database (running locally at `localhost:27017` or configured in settings)

### Quickstart Guide
1. Clone or download the repository and navigate to the root directory.
2. (Optional but recommended) Create and activate a virtual Python environment:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install django django-mongodb-backend pymongo django-allauth
   ```
4. Run the database migrations to build your MongoDB schemas locally:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create an administrative superuser account (if you haven't used the automated injection script):
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```
7. **Google OAuth Setup** (Required for frontend login):
   - Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials → Create OAuth 2.0 Client ID (Web application).
   - Under **Authorized redirect URIs**, add exactly: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - Copy the `client_id` and `secret` into `config/settings.py` under `SOCIALACCOUNT_PROVIDERS > google > APP`.
   - The callback is handled automatically by `django-allauth` — do not create a custom view for it.
8. Open a web browser:
   - Dashboard & App UI: `http://127.0.0.1:8000/`
   - Django Admin: `http://127.0.0.1:8000/admin/`

## Architecture Structure

This project completely drops monolithic structures by separating logic into two core scalable systems:

- **`backend`**: Houses all database modeling via an `api/models/` folder. Contains schemas for `user_model.py`, `song_model.py`, and `share_model.py`. The Django Admin interface is explicitly registered to expose all these nested attributes.
- **`frontend`**: Manages the CRUD (Create, Read, Update, Delete) interfaces dynamically. Contains `views.py` handling form processing logic, `urls.py` managing all interaction routes, and `templates/frontend/` presenting the Tailwind-styled HTML views securely.

## Core Models

- **`User`**: Base profile extending the custom user matrix. Holds many-to-many relationship mappings to track a `listens_to` history. Replaces the older separate Artist/Enjoyer paradigms so anyone can act as a creator.
- **`Song`**: The core data object tied directly to the `User` framework who generated it. Includes metadata like tags, genre, description, and status.
- **`ShareLink`**: External links carrying specific user permissions (view, download, share forward) for shared interactions.

## CRUD Operations

CREATE
![CREATE](images/img1.png)

READ
![READ](images/img2.png)

UPDATE
![UPDATE](images/img3.png)

DELETE
![DELETE](images/img4.png)
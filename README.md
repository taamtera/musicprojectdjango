# Chithara AI Music Generator - Domain Layer Implementation

This repository contains the Django domain layer implementation for the Chithara AI Music Generator (Exercise 3).

## Project Setup

### Prerequisites
- Python 3.10+
- Django 5.2+

### Running the Project Locally
1. Clone or download the repository and navigate to the project root directory.
2. Install Django (if not already installed):
   ```bash
   pip install django
   ```
3. Apply the database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```
4. (Optional) Create a superuser to access the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Open a web browser and navigate to `http://127.0.0.1:8000/admin/` to access the admin site. 

## Domain Model Implementation
The domain models have been implemented straight from the domain diagram provided:
- **`User`**: Base user model extending `AbstractUser`. Includes custom string representations.
- **`Artist` & `Enjoyer`**: Submodels of `User`, inheriting using Django's multi-table inheritance strategy acting as specialized User types.
- **`Song`**: The main payload object. Tied to `Artist` (who generated it) through a one-to-many relation, and `Enjoyer` (who listens to it) through a many-to-many relation.
- **`Library`**: Contains references linking a 1-to-1 generated library or a 1-to-1 shared library directly from the User.
- **`LibraryEntry`**: Effectively a junction model spanning `Library` and `Song` containing its string `entry_type`.
- **`ShareLink`**: Holds individual shares representing permissions, an extrinsic email, the linked track, and the user who originated the share.

## CRUD Operations Setup
Creation, Reading, Updating, and Deletion operations can all be manually performed right in the browser via the **Django Admin** interface.
- Logging into `/admin` with your superuser credentials will permit adding new Users, generating Songs, and linking Libraries. 
- You do not need to construct specific API endpoints or View templates for this assignment based on instructions.

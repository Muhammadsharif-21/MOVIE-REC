# Watchlist - Movie/Anime Tracker API

A REST API and web frontend for tracking shows I'm watching, rating them, and leaving notes. Built with Flask, MySQL, and the OMDb API.

## Features

- Full CRUD for shows and reviews, with a one-to-many relationship (one show can have many reviews) and cascade delete
- Filter shows by status (watching, completed, dropped)
- Search by title, partial match, case-insensitive
- Sort by title, genre, status, or average rating
- Pagination on the show list
- Duplicate prevention (case-insensitive) and rating validation (1-10)
- Pulls poster image, plot, IMDb rating, and release year from OMDb when a show is added
- Frontend is plain HTML/CSS/JS, no framework, talks to the API with fetch()

## Tech Stack

Backend: Flask, Flask-RESTful
Database: MySQL, SQLAlchemy, Flask-Migrate
External API: OMDb API, requests
Config: python-dotenv
Frontend: HTML, CSS, vanilla JavaScript

## Project Structure

```
MOVIE-REC/
  app.py            app entry point, config, db/api init
  extensions.py      db and api instances, kept separate to avoid circular imports
  models.py          Show and Review models
  resources.py        all API routes
  templates/
    index.html        frontend
  migrations/          schema history
  .env                 local secrets, not committed
  requirements.txt
```

## Setup

1. Clone and install dependencies

```
git clone <your-repo-url>
cd MOVIE-REC
pip install -r requirements.txt --break-system-packages
```

2. Create a MySQL database

```
CREATE DATABASE moviedb;
```

3. Create a .env file in the project root

```
OMDB_API_KEY=your_omdb_key_here
```

Get a free key at omdbapi.com/apikey.aspx.

Update the MySQL connection string in app.py with your own username and password:

```
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<user>:<password>@127.0.0.1:3306/moviedb"
```

4. Run migrations

```
flask db upgrade
```

5. Start the server

```
python app.py
```

Visit 127.0.0.1:5000 for the frontend, or hit the API directly at 127.0.0.1:5000/api/

## API Endpoints

GET /api/shows/ - list shows, supports ?status=, ?title=, ?sort=, ?page=, ?per_page=
POST /api/shows/ - create a show, checked against OMDb first
GET /api/shows/<id> - get one show
PATCH /api/shows/<id> - update a show
DELETE /api/shows/<id> - delete a show and its reviews
GET /api/shows/<id>/reviews - list reviews for a show
POST /api/shows/<id>/reviews - add a review, rating 1-10
GET /api/reviews/<id> - get one review
PATCH /api/reviews/<id> - update a review
DELETE /api/reviews/<id> - delete a review
GET /api/shows/<id>/stats - average rating for a show

Sort options: sort=title, sort=-title, sort=genre, sort=status, sort=rating, sort=-rating
The minus sign means descending.

## Example

```
curl -X POST http://127.0.0.1:5000/api/shows/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Breaking Bad", "genre": "Crime", "status": "completed"}'
```

## Notes

Deleting a show deletes its reviews too, using cascade delete on the relationship.
Shows added before OMDb enrichment was added won't have poster, plot, or year data. The frontend just skips showing those fields for older entries instead of breaking.
No authentication yet. This is a personal project, not something running in production.

## Why I built this

Built this to practice REST API design, SQLAlchemy relationships, working with an external API, and connecting a plain JS frontend to a Flask backend.

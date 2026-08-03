from models import Show, Review
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from extensions import db, api
from sqlalchemy import func
import os
import requests
from dotenv import load_dotenv
from flask import request

OMDB_KEY = os.getenv("OMDB_API_KEY") 

showFields = {
    "id": fields.Integer,
    "title": fields.String,
    "genre": fields.String,
    "status": fields.String
}


reviewFields = {
    "id": fields.Integer,
    "show_id": fields.Integer,
    "rating": fields.Integer,
    "notes": fields.String
}




show_args = reqparse.RequestParser()
show_args.add_argument("title", type=str, required=True, help="Title is required")
show_args.add_argument("genre", type=str, required=True, help="Genre is required")
show_args.add_argument("status", type=str, required=True, help="Status is required")

review_args = reqparse.RequestParser()
review_args.add_argument("rating", type=int, required=True, help="Rating is required")
review_args.add_argument("notes", type=str, required=False, help="Notes are required")


class ShowlistResource(Resource):
    @marshal_with(showFields)
    def get(self):
        status = request.args.get("status")
        title = request.args.get("title")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        query = Show.query

        if status:
            query = query.filter_by(status=status)

        if title:
            query = query.filter(Show.title.ilike(f"%{title}%"))

        shows = query.paginate(page=page, per_page=per_page, error_out=False)
        return shows.items

    @marshal_with(showFields)
    def post(self):
        args = show_args.parse_args()
        existing = Show.query.filter_by(title=args['title']).first()
        if existing:
            abort(409, message="Show aleardy exists")
        response = requests.get(f"http://www.omdbapi.com/?t={args['title']}&apikey={OMDB_KEY}")
        data = response.json()
        if data.get("Response") == "False":
            abort(404, message="Show not found on OMDb")

        show = Show(title=args["title"], genre=args["genre"], status=args["status"])
        db.session.add(show)
        db.session.commit()
        return show, 201





class ShowResource(Resource):
    @marshal_with(showFields)
    def get(self, id):
        show = Show.query.filter_by(id=id).first()
        if not show:
            abort(404, message="Show not found.")
        return show    

    @marshal_with(showFields)
    def patch(self, id):
        args = show_args.parse_args()
        show = Show.query.filter_by(id=id).first()
        if not show:
            abort(404, message="Show not found.") 
        show.title = args["title"]    
        show.genre = args["genre"]    
        show.status = args["status"]    
        db.session.add(show)
        db.session.commit()    
        return show   

    
    @marshal_with(showFields)
    def delete(self, id):
        show = Show.query.filter_by(id=id).first()
        if not show:
            abort(404, message="Show not found.") 
        db.session.delete(show)
        db.session.commit()  
        shows = Show.query.all()
        return shows



class ReviewListShow(Resource):
    @marshal_with(reviewFields)
    def get(self, show_id):
        reviews = Review.query.filter_by(show_id=show_id).all()
        return reviews
    
    @marshal_with(reviewFields)
    def post(self, show_id):
        args = review_args.parse_args()
        review = Review(show_id=show_id, rating=args["rating"], notes=args["notes"])
        db.session.add(review)
        db.session.commit()
        return review, 201
    
class ReviewShow(Resource):
    @marshal_with(reviewFields)
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, message="Review not found")
        return review    

    @marshal_with(reviewFields)
    def patch(self, id):
        args = review_args.parse_args()
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, message="Review not found")
        review.rating = args["rating"]
        review.notes = args["notes"]
        db.session.add(review)
        db.session.commit()
        return review 

    @marshal_with(reviewFields)
    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, message="Review not found")
        db.session.delete(review)
        db.session.commit()
        return review



class ShowStatsResource(Resource):
    def get(self, show_id):
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.show_id == show_id).scalar()
        if avg_rating is None:
            return {"show_id": show_id, "average_rating": None, "message": "No reviews yet"}, 200
        return {"show_id": show_id, "average_rating": round(float(avg_rating), 2)}, 200
        
        

api.add_resource(ShowlistResource, "/api/shows/")
api.add_resource(ShowResource, "/api/shows/<int:id>")
api.add_resource(ReviewListShow, "/api/shows/<int:show_id>/reviews")
api.add_resource(ReviewShow, "/api/reviews/<int:id>")
api.add_resource(ShowStatsResource, "/api/shows/<int:show_id>/stats")
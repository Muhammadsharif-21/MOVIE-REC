from models import Show, Review
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from extensions import db, api



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
        shows = Show.query.all()
        return shows

    @marshal_with(showFields)
    def post(self):
        args = show_args.parse_args()
        show = Show(title=args["title"], genre=args["genre"], status=args["status"])
        db.session.add(show)
        db.session.commit()
        return show, 201





class ShowResource(Resource):
    @marshal_with(showFields)
    def get(self, id):
        show = Show.query.filter_by(id=id).first()
        if not show:
            abort(404, "show not found")
        return show    

    @marshal_with(showFields)
    def patch(self, id):
        args = show_args.parse_args()
        show = Show.query.filter_by(id=id).first()
        if not show:
            abort(404, "User not found.") 
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
            abort(404, "User not found.") 
        db.session.delete(show)
        db.session.commit()  
        users = Show.query.all()
        return users



class ReviewListShow(Resource):
    @marshal_with(reviewFields)
    def get(self, show_id):
        reviews = Review.query.filter_by(show_id=show_id).all()
        return reviews
    
    @marshal_with(reviewFields)
    def post(self, show_id):
        args = review_args.parse_args()
        reviews = Review(show_id=show_id, rating=args["rating"], notes=args["notes"])
        db.session.add(reviews)
        db.session.commit()
        return reviews, 201
    
class ReviewShow(Resource):
    @marshal_with(reviewFields)
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, "Review not found")
        return review    

    @marshal_with(reviewFields)
    def patch(self, id):
        args = review_args.parse_args()
        review = Review.query.filter_by(id=id).first()
        if not review:
            abort(404, "Review not found")
        review.rating = args["rating"]
        review.notes = args["notes"]
        db.session.add(review)
        db.session.commit()
        return review 

    @marshal_with(reviewFields)
    def delete(self, id):
        review = Review.query.filter_by(id=id)
        if not review:
            abort(404, "Review not found")
        db.session.delete(review)
        db.session.commit()
        return review
    

api.add_resource(ShowlistResource, "/api/shows/")
api.add_resource(ShowResource, "/api/shows/<int:id>")
api.add_resource(ReviewListShow, "/api/shows/<int:show_id>/reviews")
api.add_resource(ReviewShow, "/api/reviews/<int:id>")



from flask_restx import Resource , Namespace
from flask import request , jsonify,g
from app import db
from models.Movie import Movie,MovieItemList
from authenticate  import jwt_middleware
from datetime import datetime
from schema.Movie import MovieData
from pydantic import ValidationError

movie_api = Namespace('movie')


## Creating and Fetching the Movie 
@movie_api.route('/')
class CreateAndFetchMovie(Resource):
    @jwt_middleware #Check user Login
    def post(self):
        try:
            movieData = MovieData(**request.get_json())
        except ValidationError as e:
            return {"validation errors": e.errors()}, 400
        except Exception as e:
            return {"message": str(e)}, 400

        new_movie = Movie(
            title = movieData.title,
            description=movieData.description,
            release_date= movieData.release_date,
            director=movieData.director,
            avg_rating=movieData.avg_rating,
            ticket_price=movieData.ticket_price,
            genre = movieData.genre,
            user_id=g.user.id,
        )

        db.session.add(new_movie)
        db.session.commit()

        return {"message": "Movie created successfully"}, 201
    
    @jwt_middleware
    def get(self):
        page = int(request.args.get('page', 1))
        movies_per_page = request.args.get("movies_per_page", 10, type=int)
        sort_by = request.args.get("sort_by", "none", type=str)
        filter_by = request.args.get("filter_by", "none", type=str)
        filter_value = request.args.get("filter_value", "", type=str)
        order_by = request.args.get("order_by", "asc", type=str)

        if page < 1:
            return {"message": "Invalid page number"}, 400

        if sort_by not in ["release_date", "ticket_price", "none"]:
            return {"message": "Invalid sort_by parameter"}, 400

        if filter_by not in ["genre", "director", "release_year", "none"]:
            return {"message": "Invalid filter_by parameter"}, 400

        query = Movie.query

        # Apply filters
        if filter_by != "none":
            query = query.filter(getattr(Movie, filter_by).like("%" + filter_value + "%"))

        # Apply sorting
        if sort_by != "none":
            order_attr = getattr(Movie, sort_by)
            if order_by == "desc":
                query = query.order_by(order_attr.desc())
            else:
                query = query.order_by(order_attr.asc())

        # Paginate the results
        paginated_movies = query.paginate(page=page, per_page=movies_per_page, error_out=False)

        if not paginated_movies.items:
            return {"message": "No movies found"}, 404
        
        MovieData = MovieItemList(many=True).dump(paginated_movies)
        response = jsonify(MovieData)
        response.status_code = 200
        return response

# Updating and Deleting the Movie
@movie_api.route("/<int:movie_id>")
class MovieUpdateandDelete(Resource):
    @jwt_middleware
    def put(self,movie_id):
        try:
            movie_data = request.get_json()
        except Exception as e:
            return {"message":str(e)},400
        
        user_id = g.user.id

        movie = Movie.query.filter_by(id = movie_id).first()

        if not movie:
            return {"message":'movie not found'},404
        
        if movie.user_id != user_id:
            return {"message": "You can only update movies created by you"}, 400

        if 'title' in movie_data:
            movie.title = movie_data['title']
        if 'description' in movie_data:
            movie.description = movie_data['description']

        db.session.commit()
        return {"message": "Movie updated successfully"}, 200

    @jwt_middleware
    def delete(self,movie_id):

        user_id = g.user.id

        movie = Movie.query.filter_by(id = movie_id).first()

        if not movie:
            return {"message": "Movie does not exist"}, 404
        
        if movie.user_id != user_id:
            return {"message": "You can only delete movies created by you"}, 400
        
        db.session.delete(movie)
        db.session.commit()

        return {"message":"Movie deleted Successfully"},200
    
    @jwt_middleware
    def get(self,movie_id:int):

        if movie_id is not None:
            movie = Movie.query.filter_by(id=movie_id).first()
            if not movie:
                return {"message": "Movie does not exist"},404
            
            #using Marshmallow
            MovieData = MovieItemList().dump(movie)
            response = jsonify(MovieData)
            response.status_code = 200
            return response
            
        else:
            return {"message": "Invalid movie id"},400
        
def search(query,field_names=["title", "description", "director","avg_rating"]):
    results = []
    data = Movie.query.all()
    print(query)

    for item in data:
        for name in field_names:
            field_value = getattr(item, name)
            if query.lower() in str(field_value).lower():
                movie_dict = {field: str(getattr(item, field)) for field in field_names}
                results.append(movie_dict)
                break
    return results


# search api call
@movie_api.route('/Search')
class SearchApi(Resource):
    @jwt_middleware
    def get(self):
        search_query = request.args.get('query')

        if not search_query:
            return ({'error': 'Please provide a search query'}), 404
        
        results = search(search_query, field_names=["title", "description", "director","avg_rating"])
        return (results),200
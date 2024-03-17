from flask_restx import Resource , Namespace
from flask import request , jsonify,current_app
from app import db
from models.Auth import User
from core.security import get_hashed_password, verify_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from schema.user import UserRegistration,UserLoginData
from pydantic import ValidationError

auth_api = Namespace('auth')

@auth_api.route('/register')
class RegisterData(Resource):
    def post(self):
        try:
            user_data = UserRegistration(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation error":e.errors()},400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return {"message":str(e)},400
        
        name = user_data.username
        email = user_data.email
        password = user_data.password

        try:
            existing_user = User.query.filter_by(email = email).first()
            if existing_user:
                res = jsonify({'message': 'User already exists'})
                res.status_code = 409
                return res
            
            hashed_password = get_hashed_password(password)
            new_user = User(username=name,email = email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            response = jsonify({'message': 'User registered successfully'})
            response.status_code = 200
            return response
        
        except Exception as e:
            error =  jsonify({'message': str(e)})
            error.status_code = 500
            return error

@auth_api.route('/login')
class LoginData(Resource):
    def post(self):
        try:
            user_data = UserLoginData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400

        email = user_data.email
        password = user_data.password

        try:
            user = User.query.filter_by(email = email).first()
            if not user:
                res = jsonify({"message":"User Not Found"})
                res.status_code = 404
                return res
            password = password
            if not verify_password(password.encode("utf-8"),user.password):
                return {"message": "Incorrect password"}, 400
            
            access_token = create_access_token(identity=user.id)
            response = jsonify({'access_token': access_token})
            response.status_code = 200
            return response
        
        except:
            error = jsonify({'message':'Invalid Credentials'})
            error.status_code = 401
            return error

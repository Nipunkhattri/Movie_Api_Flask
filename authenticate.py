from functools import wraps
from flask import request, jsonify,g
from flask_jwt_extended import verify_jwt_in_request,get_jwt

def jwt_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
        except:
            res = jsonify({"message":"Access Token Error"})
            res.status_code = 401
            return res
        
        from models.Auth import User
        user = User.query.filter(
            User.id == claims.get('sub')
        ).first()
        
        print(user)

        g.user = user
        return func(*args,**kwargs)
    
    return decorated_function

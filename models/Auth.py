from app import db , ma 

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable = False)
    password = db.Column(db.String,nullable = False)

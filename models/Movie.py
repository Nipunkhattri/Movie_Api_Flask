from app import db,ma

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.Date)
    director = db.Column(db.String)
    genre = db.Column(db.String)
    avg_rating = db.Column(db.Float)
    ticket_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    created_by = db.relationship("User", backref="Movie")

class MovieItemList(ma.Schema):
    class Meta:
        fields = ("title","description","director","release_date","genre","avg_rating","ticket_price")
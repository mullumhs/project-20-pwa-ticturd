from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.Text)
    genre = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    cast = db.Column(db.List)
    image = db.Column(db.String, nullable = True) #Store in static/uploads, generate a unique file name for it, store reference in database




    def __repr__(self):
        return f'<Movie {self.title}>'
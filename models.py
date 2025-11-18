from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.Text, nullable = False)
    genre = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable = True) #Store in static/uploads, generate a unique file name for it, store reference in database
    description = db.Column(db.String, nullable = False)



    def __repr__(self):
        return f'<Movie {self.title}>'
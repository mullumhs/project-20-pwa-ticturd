from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    def set_password(self, password):
        #Uses werkzeugs security class to generate a password hash when creating an account.
        self.password = generate_password_hash(password)

    def get_password(self, password):
        #Uses werkzeugs security class to return hashed password to normal state, when logging in.
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
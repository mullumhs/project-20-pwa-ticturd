from flask import render_template, request, redirect, url_for, flash
from models import db, Movie, User # Also import your database model here
import datetime

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

#-------------------------------------------Movie--------------------------------------------------------------
def init_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def get_items():
        # This route should retrieve all items from the database and display them on the page.
        movies = Movie.query.all()
        return render_template('index.html', message='Displaying all items', movies=movies)



    @app.route('/add', methods=['POST'])
    def create_movie():
        # This route should handle adding a new item to the database.

        new_movie = Movie(
            title = request.form['title'],
            director = request.form['director'],
            genre = request.form['genre'],
            year = int(request.form['year']),
            rating = float(request.form['rating']),
            image = request.form['image'],
            description = request.form['description'],
        )
        db.session.add(new_movie)
        db.session.commit()

        

        return render_template('index.html', message='Item added successfully')



    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.

        movie_id = request.form['id']
        movie = Movie.query.get_or_404(movie_id)

        movie.title = request.form['name']

        db.session.commit()

        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.

        movie_id = request.form['id']
        movie = Movie.query.get_or_404(movie_id)

        db.session.delete(movie)
        db.session.commit()

        return render_template('index.html', message=f'Item deleted successfully')
    


#--------------------------------------------------------Users----------------------------------------------------------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(username=username).first()
            if existing_user != None:
                return render_template('register.html', error=f'Username already exists.')
            else:
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                return render_template('dashboard.html', user=new_user)
        else:
             return render_template('register.html')
        
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and user.get_password(password):    
                return render_template('dashboard.html', user=user)
            else:
                return render_template('login.html', error="Invalid username or password.")
        else:
            return render_template('login.html')
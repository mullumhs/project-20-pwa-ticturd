from flask import render_template, request, redirect, url_for, flash
from models import db, Movie # Also import your database model here
import datetime

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def get_items():
        # This route should retrieve all items from the database and display them on the page.
        movies = Movie.query.all()
        return render_template('index.html', message='Displaying all items', movies=movies)



    @app.route('/add', methods=['POST'])
    def create_movie():
        # This route should handle adding a new item to the database.
        if request.method == 'POST':
            new_movie = Movie(
                title = request.form['title'],
                director = request.form['director'],
                genre = request.form['genre'],
                release_date = datetime.date(request.form['release_date']),
                cast = request.form['cast'],
                image = request.form['image']
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('index'))

        

        return render_template('index.html', message='Item added successfully')



    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')
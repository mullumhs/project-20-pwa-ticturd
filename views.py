from flask import render_template, request, redirect, url_for, flash, session
from models import db, Movie, User # Also import your database model here
from werkzeug.utils import secure_filename
import os
# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages





def init_routes(app):
#--------------------------------------------------------Landing--------------------------------------------------------------------
    @app.route('/')
    def index():
        return render_template('index.html')

#--------------------------------------------------------Users----------------------------------------------------------------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            #Checks database for existing usernames
            existing_user = User.query.filter_by(username=username).first()
            if existing_user != None:
                return render_template('register.html', error=f'Username already exists.')
            
            #Creates account, directs user to log in.
            else:
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                return render_template('login.html', message="Please log in.")
            
        else:
             return render_template('register.html')
        
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            #Checks if password matches hashed version stored in database.
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):    
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid username or password.")
        else:
            return render_template('login.html')
        
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.pop('user_id')
        return redirect(url_for('index'))
#--------------------------------------------------Dashboard---------------------------------------------------------------


    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        #Gets logged in user id
        user_id = session.get('user_id')
        if 'user_id' not in session:
            return render_template('login.html', message="Please log in or register.")
        user = User.query.get(user_id)

        #Queries movies for the specific user.
        movies = Movie.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', movies=movies, user=user)
    


#-------------------------------------------Movie--------------------------------------------------------------

    @app.route('/add', methods=['POST'])
    def create_movie():
        #Handles adding a new movie to the database and linking it to the current user.
        if 'user_id' not in session:
            return render_template('login.html', error="User ID not in session")
        else:
            #Handles image file / url upload
            image_file = request.files.get("image_file")
            image_url = request.form.get("image_url")

            if image_file and image_file.filename != "":
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)

                image_path = f'static/uploads/{filename}'

            elif image_url:
                image_path = image_url

            else:
                image_path = None

            #Creates the movie
            new_movie = Movie(
                title = request.form['title'],
                director = request.form['director'],
                genre = request.form['genre'],
                year = int(request.form['year']),
                rating = float(request.form['rating']),
                description = request.form['description'],
                image = image_path,
                user_id = session.get('user_id')
            )

            db.session.add(new_movie)
            db.session.commit()

            return redirect(url_for('dashboard'))



    @app.route('/update', methods=['POST'])
    def update_item():
        #Again handles image upload / url changes
        movie_id = request.form['id']
        movie = Movie.query.get_or_404(movie_id)

        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url")

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)

            image_path = f'static/uploads/{filename}'

        elif image_url:
            image_path = image_url

        else:
            image_path = None

        #Updates the specified movie.
        movie.title = request.form["title"]
        movie.director = request.form["director"]
        movie.genre = request.form["genre"]
        movie.year = request.form["year"]
        movie.rating = request.form["rating"]
        movie.description = request.form["description"]
        movie.image = image_path
        

        db.session.commit()

        return redirect(url_for('dashboard'))



    @app.route('/delete', methods=['POST'])
    def delete_item():
        #Deletes specified movie.

        movie_id = request.form['id']
        movie = Movie.query.get_or_404(movie_id)

        db.session.delete(movie)
        db.session.commit()

        return redirect(url_for('dashboard'))
    


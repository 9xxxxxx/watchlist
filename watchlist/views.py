from watchlist import app, db
from watchlist.models import Movie, User
from flask import redirect, url_for, request, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user

from werkzeug.security import generate_password_hash


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        
        title = request.form.get('title')
        year = request.form.get('year')
        poster = request.form.get('poster')
        
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        
        movie = Movie(title=title, year=year, poster=poster)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        edit_title = request.form['edit_title']
        edit_year = request.form['edit_year']
        edit_poster = request.form['edit_poster']
        edit_review = request.form['edit_review']

        if not edit_title or not edit_year or len(edit_year) > 4 or len(edit_title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = edit_title
        movie.year = edit_year
        movie.poster = edit_poster
        movie.review = edit_review
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    
    return render_template('settings.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('signup'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('The username is already existed.')
            return redirect(url_for('signup'))

        user = User(name='guest', username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/movie/detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('detail.html', movie=movie)
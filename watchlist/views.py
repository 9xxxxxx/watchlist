from datetime import datetime
from watchlist import app, db
from watchlist.models import Movie, User, Comment
from flask import redirect, url_for, request, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user

from werkzeug.security import generate_password_hash
from watchlist.myform import LoginForm, RegisterForm, CommentForm, SettingForm

per_page = 3
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
        
        movie = Movie(title=title, year=year, poster=poster,time=datetime.now())
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
      # Define how many items per page you want
    pagination = Movie.query.paginate(page=page, per_page=app.config['PER_PAGE'], error_out=False)
    items = pagination.items
    return render_template('index.html', movies=items, pagination=pagination)


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
        if user:
            # 验证用户名和密码是否一致
            if username == user.username and user.validate_password(password):
                login_user(user)
                user.last_login_time = datetime.now()
                db.session.commit()
                flash('Login success.')
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        
    form = LoginForm()
    return render_template('login.html', form = form)


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
    form = SettingForm()
    return render_template('settings.html', form=form)


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

        user = User(name='guest', username=username, password_hash=generate_password_hash(password), avatar =url_for('static', filename='images/default_avatar.png'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    form = RegisterForm()
    return render_template('signup.html', form=form)

@app.route('/movie/detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get(movie_id)
    comments = Comment.query.filter_by(movie_id=movie_id).all()
    return render_template('detail.html', movie=movie, comments=comments)


@app.route('/movie/comment/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def comment(movie_id):
    if request.method == 'POST':
        content = request.form.get('Content')
        user_id = current_user.id
        time = datetime.now()
        username = current_user.username
        name = current_user.name
        
        comment = Comment(movie_id=movie_id, content=content, 
                          user_id=user_id, time=time,
                          username=username, name=name,
                          updated_at = datetime.now())
        # 相当于创建新的一行数据
        db.session.add(comment)
        db.session.commit()
        
        return redirect(url_for('detail', movie_id=movie_id))
    
    form = CommentForm()
    return render_template('comment.html', form=form)

@app.route('/movie/<int:page>')
def items(page):
  # Define how many items per page you want
    pagination = Movie.query.paginate(page=page, per_page=app.config['PER_PAGE'], error_out=False) 
    top_ten_items = pagination.items
    action_url = url_for('index')
    return render_template('items.html', movies=top_ten_items, pagination=pagination, action_url=action_url)
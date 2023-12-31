import sys
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import click
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required, current_user


app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:  # 是否删除数据库
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
    
    
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Garry HOst'
    movies = [
        {'title': '龙猫-My Neighbor Totoro', 'year': '1988','poster':'https://img9.doubanio.com/view/photo/l/public/p2540924496.webp'},
        {'title': '死亡诗社-Dead Poets Society', 'year': '1989','poster':'https://img1.doubanio.com/view/photo/m/public/p2575465690.webp'},
        {'title': '完美的世界-A Perfect World', 'year': '1993','poster':'https://img1.doubanio.com/view/photo/m/public/p1562273940.webp'},
        {'title': '这个杀手不太冷-Leon', 'year': '1994','poster':'https://img3.doubanio.com/view/photo/m/public/p2408302602.webp'},
        {'title': '麻将-Mahjong', 'year': '1996','poster':'https://img9.doubanio.com/view/photo/m/public/p2873829595.webp'},
        {'title': '燕尾蝶-Swallowtail Butterfly', 'year': '1996','poster':'https://img3.doubanio.com/view/photo/m/public/p2056451383.webp'},
        {'title': '喜剧之王-King of Comedy', 'year': '1999','poster':'https://img1.doubanio.com/view/photo/m/public/p2181431029.webp'},
        {'title': '鬼子来了-Devils on the Doorstep', 'year': '1999','poster':'https://img1.doubanio.com/view/photo/m/public/p2553104888.webp'},
        {'title': '机器人总动员-WALL-E', 'year': '2008','poster':'https://img1.doubanio.com/view/photo/m/public/p1037415760.webp'},
        {'title': '麦兜-The Pork of Music', 'year': '2012','poster':'https://img9.doubanio.com/view/photo/m/public/p1626461596.webp'},
    ]
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'], poster=m['poster'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
# ...
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key
    name = db.Column(db.String(20)) # name
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):         
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)



class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key
    title = db.Column(db.String(60))    # movie title
    year = db.Column(db.String(4))  # movie year
    poster = db.Column(db.String(256))



@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        
        title = request.form.get('title')
        year = request.form.get('year')
        
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        
        movie = Movie(title=title, year=year)
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
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
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

        user = User.query.first()
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



@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user



if __name__ == '__main__':
    app.run()

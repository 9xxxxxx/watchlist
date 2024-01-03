import datetime
import click

from watchlist import app, db
from watchlist.models import User, Movie
from werkzeug.security import generate_password_hash

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
@click.option('--drop', is_flag=True, help='Create after drop.', prompt=True) 
def initdb(drop):
    """Initialize the database."""
    if drop:  # 是否删除数据库
        click.echo('Drop database.')
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')
    
    
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Garry Host'
    movies = [
        {'title': '龙猫 - My Neighbor Totoro', 'year': '1988','poster':'https://img9.doubanio.com/view/photo/l/public/p2540924496.webp'},
        {'title': '死亡诗社 - Dead Poets Society', 'year': '1989','poster':'https://img1.doubanio.com/view/photo/m/public/p2575465690.webp'},
        {'title': '完美的世界 - A Perfect World', 'year': '1993','poster':'https://img1.doubanio.com/view/photo/m/public/p1562273940.webp'},
        {'title': '这个杀手不太冷 - Leon', 'year': '1994','poster':'https://img3.doubanio.com/view/photo/m/public/p2408302602.webp'},
        {'title': '麻将 - Mahjong', 'year': '1996','poster':'https://img9.doubanio.com/view/photo/m/public/p2873829595.webp'},
        {'title': '燕尾蝶 - Swallowtail Butterfly', 'year': '1996','poster':'https://img3.doubanio.com/view/photo/m/public/p2056451383.webp'},
        {'title': '喜剧之王 - King of Comedy', 'year': '1999','poster':'https://img1.doubanio.com/view/photo/m/public/p2181431029.webp'},
        {'title': '鬼子来了 - Devils on the Doorstep', 'year': '1999','poster':'https://img1.doubanio.com/view/photo/m/public/p2553104888.webp'},
        {'title': '机器人总动员 - WALL-E', 'year': '2008','poster':'https://img1.doubanio.com/view/photo/m/public/p1037415760.webp'},
        {'title': '麦兜 - The Pork of Music', 'year': '2012','poster':'https://img9.doubanio.com/view/photo/m/public/p1626461596.webp'},
    ]
    
    user = User(name=name, username='jack', password_hash=generate_password_hash('000'))
    db.session.add(user)
    for m in movies:
        addtime = datetime.datetime.now()
        movie = Movie(title=m['title'], year=m['year'], poster=m['poster'], time=addtime)
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
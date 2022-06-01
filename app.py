import os

from flask import Flask
from flask import render_template
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Routes
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.errorhandler(404)  
def page_not_found(e):  
    return render_template('404.html'), 404  

@app.context_processor
def inject_user():  
    user = User.query.first()
    return dict(user=user)  

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:22055@localhost/flask_sample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

import click

@app.cli.command() 
@click.option('--drop', is_flag=True, help='Create after drop.') 
def initdb(drop):
    """Initialize the database."""
    if drop: 
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
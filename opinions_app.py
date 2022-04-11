from datetime import datetime
from random import randrange

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# В ORM передаётся в качестве параметра экземпляр приложения Flask
db = SQLAlchemy(app)


class Opinion(db.Model):
    # ID — целое число, первичный ключ
    id = db.Column(db.Integer, primary_key=True)
    # Название фильма — строка длиной 128 символов, не может быть пустым
    title = db.Column(db.String(128), nullable=False)
    # Мнение о фильме — большая строка, не может быть пустым,
    # должно быть уникальным
    text = db.Column(db.Text, unique=True, nullable=False)
    # Ссылка на IMDb — строка длиной 256 символов
    source = db.Column(db.String(256))
    # Дата и время — текущее время,
    # по этому столбцу база данных будет проиндексирована
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return 'В базе данных мнений о фильмах нет.'

    # Если не 0, то выбирается случайное число в диапазоне от 0 и до quantity
    offset_value = randrange(quantity)
    # Получается случайный объект
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add')
def add_opinion_view():
    return render_template('add_opinion.html')


@app.route('/opinions/<int:id>')
# Параметром указывается имя переменной
def opinion_view(id):
    # Теперь можно запрашивать мнение по id
    opinion = Opinion.query.get_or_404(id)
    # И передавать его в шаблон
    return render_template('opinion.html', opinion=opinion)


if __name__ == '__main__':
    app.run()

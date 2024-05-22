from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from . repository import UrlsRepository
from . validator import validate
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

repo = UrlsRepository(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    url = {}
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        url=url,
        messages=messages,
    )


@app.post('/urls')
def add_url():
    messages = get_flashed_messages(with_categories=True)
    data = request.form.to_dict()
    error, url = validate(data.get('url'))
    if error:
        flash(f'Ошибка: {error}', 'danger')
        return render_template(
            'index.html',
            url=url,
            messages=messages,
        ), 422
    old_url = repo.find(name=url)
    if not old_url:
        repo.add(url)
        flash(f'Добавлен новый сайт {url}', 'success')
    else:
        flash(f'Сайт уже присутствует {url}', 'warning')
    return redirect(url_for('urls'))


@app.route('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        urls=repo.get_all(),
        messages=messages,
    )


@app.route('/urls/<id>')
def url_view(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id=id)
    if url:
        return render_template(
            'url.html',
            url=url[0],
            messages=messages,
        )
    return render_template(
           'not_found.html',
    ), 404

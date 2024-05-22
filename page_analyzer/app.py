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
    if not repo.find_urls(name=url):
        repo.add_url(url)
        flash(f'Добавлен новый сайт {url}', 'success')
    else:
        flash(f'Сайт уже присутствует {url}', 'warning')
    return redirect(url_for('urls'))


@app.route('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        url_items=repo.get_all_url(),
        messages=messages,
    )


@app.route('/urls/<id>')
def url_view(id):
    messages = get_flashed_messages(with_categories=True)
    url_item = repo.find_one_url(id=id)
    checks = repo.find_checks(id=id)
    print('checks =', checks)
    if url_item:
        return render_template(
            'url.html',
            url_item=url_item,
            messages=messages,
            checks=checks,
        )
    return render_template(
           'not_found.html',
    ), 404


@app.post('/urls/<id>/checks')
def url_check(id):
    result = False
    url_item = repo.find_one_url(id=id)
    print('url_item =', url_item)
    if url_item:
        url = url_item.name
        print('url =', url)
        result = repo.add_check(url)
    if result:
        flash(f'Checked {id}', 'success')
    else:
        flash(f'Check error {id}', 'danger')
    return redirect(url_for('url_view', id=id))

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.db import DatabaseManager
from page_analyzer.utils import validate, normalize_url
from page_analyzer.checker import extract_page_data
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db_manager = DatabaseManager(app.config)


@app.route('/')
def index():
    url = {}
    return render_template('index.html', url=url,)


@app.post('/urls')
def add_url():
    url_check = request.form.get('url')
    normal_url = normalize_url(url_check)
    data = request.form.to_dict()
    url = data.get('url')
    error = validate(url)
    validation_error = validate(normal_url)
    if error:
        flash(validation_error, 'danger')
        return render_template('index.html'), 422
    url_id = db_manager.find_url_by_name(normal_url)
    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('url_view', id=url_id))
    url = db_manager.insert_url(normal_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_view', id=url.id))


@app.route('/urls')
def urls():
    urls_data = db_manager.get_all_urls()
    return render_template('urls.html', urls=urls_data)


@app.route('/urls/<int:id>')
def url_view(id):
    url_item = db_manager.find_url_by_id(id)
    checks = db_manager.find_checks_by_id(id)
    if url_item:
        return render_template('url.html', url_item=url_item, checks=checks,)
    return render_template('not_found.html',), 404


@app.post('/urls/<int:id>/checks')
def url_check(id):
    result = False
    url_item = db_manager.find_url_by_id(id)
    print(url_item, '-----')
    if url_item:
        url = url_item.name
        id = url_item.id
        result_check = extract_page_data(url)
        if result_check:
            result = db_manager.add_check(id, result_check)
    if result:
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('url_view', id=id))

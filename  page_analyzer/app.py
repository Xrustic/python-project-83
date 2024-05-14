from flask import Flask, render_template
from flask import get_flashed_messages
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template("main.html", messages=messages)

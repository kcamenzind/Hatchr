from flask import Flask
import os

app = Flask(__name__)

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join('html', filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/')
def home_page():
    return get_file('index_page.html')

@app.route('/another_page')
def next_page():
    return "WAssup dawg"

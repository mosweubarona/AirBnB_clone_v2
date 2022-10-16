#!/usr/bin/python3
"""Start web with two routings
"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """Return string when routing
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """Return string when routing
    """
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    """Return reformatted text
    """
    return 'C ' + text.replace('_', ' ')

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)

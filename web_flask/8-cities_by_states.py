#!/usr/bin/python3
"""Start web with routings
"""

from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/cities_by_states')
def states_list():
    """Render template with states
    """
    path = '8-cities_by_states.html'
    states = storage.all(State)

    # sort State object alphabetically by name
    return render_template(path, states=states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0')

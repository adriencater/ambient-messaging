"""
AM Standalone Local Server:

  - Serve static HTML/JS for UI
  - Serve REST API for receiving messages from UI
  - Display received messages on display (Inkyphat)

"""

try:
    from . import core
except ImportError as e:
    print(
        '\n*',
        '\n* WARNING: Ignoring `import core` error:', e,
        '\n*')
import flask
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/say/<message>')
def post_text(message):
    core.display_text(message)
    return flask.jsonify({"message_sent": message})


# Run server
app.run(host='0.0.0.0', port=9999)

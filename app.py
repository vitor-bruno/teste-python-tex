from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify({'erro': str(e)}), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


from routes.addresses import addresses_blueprint
from routes.people import people_blueprint

app.register_blueprint(addresses_blueprint, url_prefix='/api/addresses')
app.register_blueprint(people_blueprint, url_prefix='/api/people')


if __name__ == '__main__':
    app.run('0.0.0.0')
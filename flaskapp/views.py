from flask import make_response

from flaskapp import app


@app.route('/ver')
def version():
    response = make_response('{"version" : %s }' % app.config.get('VERSION'), 200)
    response.content_type = "application/json"
    return response

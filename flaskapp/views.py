import json

from flask import make_response, request

from flaskapp import app
from flaskapp.functions import generate_random_session_id


@app.route('/version')
def version():
    response = make_response('{"version" : %s }' % app.config.get('VERSION'), 200)
    response.content_type = "application/json"
    return response


@app.route('/session', methods=['GET', 'POST'])
def get_new_session():
    response_dict = {}
    if request.method == 'GET':
        response_dict['request_id'] = generate_random_session_id()
        response_dict['data'] = {}
    elif request.method == 'POST':
        response_dict = {}
    else:
        response_dict = {}

    response = make_response(json.dumps(response_dict))
    response.content_type = "application/json"
    return response

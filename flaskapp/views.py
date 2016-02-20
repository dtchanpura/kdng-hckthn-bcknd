import json

from flask import make_response, request

from flaskapp import app
from flaskapp.functions import generate_random_session_id, update_or_create_session, get_session_data


@app.route('/version')
def version():
    """
    Get the version of API being deployed

    :return: Responds with a simple json {"version": "0.0.1b"}
    """
    response = make_response('{"version" : %s }' % app.config.get('VERSION'), 200)
    response.content_type = "application/json"
    return response


@app.route('/session/', methods=['GET', 'POST', 'PUT'], defaults={'session_id': None})
@app.route('/session/<session_id>', methods=['GET', 'POST', 'PUT'])
def get_session(session_id):
    """
    GET Method will generate a new session id
    POST Method requires a json with session_id in it.

    :return: Responds with session_id and data object
    """
    response_dict = {}
    if request.method == 'POST' and request.json:
        # First Time creation
        # with or without json data
        # session_id = request.json.get('session_id')
        if not session_id:
            return return_response({"message": "Something is missing, read the API docs for more information."}, 403)
        if request.json:
            update_or_create_session(session_id=session_id, data=request.json.get('data'))
            response_dict = {"ok": True}
    elif request.method == 'GET':
        # Getting information for a session_id
        if session_id is None:
            response_dict['session_id'] = generate_random_session_id()
        else:
            response_dict['data'] = get_session_data(session_id=session_id)
            response_dict['ok'] = True
    else:
        # PUT method to update the given data
        update_or_create_session(session_id=session_id, data=request.json.get('data'))
        response_dict['ok'] = True
    return return_response(response_dict)


def return_response(response_dict, code=200):
    """
    Utility function for returning a decorated response

    :param response_dict: dictionary to be returned as json
    :param code: status code to be returned
    :return: Response object for flask's request
    """
    response = make_response(json.dumps(response_dict))
    response.content_type = "application/json"
    return response, code

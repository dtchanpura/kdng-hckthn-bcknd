from flask import make_response, request

from flaskapp import app
from flaskapp.functions import *


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
    GET Method will generate a new session id or get details about it.
    POST Method requires a json with data in it.
    PUT Method also requires json with data in it.

    :param session_id: Session ID for particular session
    :return: Responds with session_id and data object
    """
    response_dict = {}
    if request.method == 'POST' and request.json:
        # First Time creation
        # with or without json data
        # session_id = request.json.get('session_id')
        if not session_id:
            return return_response({"message": "Something is missing, "
                                               "read the API docs for "
                                               "more information."}, 403)
        if is_active_session(session_id):
            return return_response({"message": "Conflict, ID already exists. Use PUT instead of POST."}, 409)
        if request.json:
            update_or_create_session(session_id=session_id, data=request.json.get('data'))
            response_dict['ok'] = True
    elif request.method == 'PUT' and request.json:
        # Updating information in session
        if not session_id:
            return return_response({"message": "Something is missing, "
                                               "read the API docs for "
                                               "more information."}, 403)
        if request.json:
            update_or_create_session(session_id=session_id, data=request.json.get('data'))
            response_dict['ok'] = True
    elif request.method == 'GET':
        # Getting information for a session_id or get new random session_id
        if session_id is None:
            response_dict['session_id'] = generate_random_session_id()
        else:
            data = get_session_data(session_id=session_id)
            if data is not None:
                response_dict = {'data': data, 'ok': True}
            else:
                return return_response({"message": "ID does not exists"}, 404)
    else:
        pass

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

from flask import make_response, request, render_template, session, redirect, url_for

from flaskapp import app
from flaskapp.forms import IntroForm
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


@app.route('/intro/', methods=['GET', 'POST'])
def intro():
    form = IntroForm(request.form)
    if 'session_id' in session:
        print(session['session_id'])
        return redirect(url_for('levels'))
    if request.method == "POST" and form.validate_on_submit():
        session_id = generate_random_session_id()
        update_or_create_session(session_id, data={'level_status': 1})
        session['session_id'] = session_id
        session['name'] = form.user_name.data
        return redirect(url_for('levels'))
    return render_template('intro.html', form=form)


@app.route('/levels/', methods=['GET', 'POST'], defaults={'level_id': None})
@app.route('/levels/<level_id>', methods=['GET', 'POST'])
def levels(level_id):
    if 'session_id' not in session:
        return redirect(url_for('intro'))
    if request.method == 'GET' and level_id is None:
        level = json.loads(get_session_data(session_id=session.get('session_id')))
        level_id = level.get('level_status')
        return render_template('levels.html', level_id=level_id, level_name="somename")
    if request.method == 'POST' and request.form is not None:
        pass_status = request.form.get('pass_status')
        if "true" in pass_status.lower():
            level = json.loads(get_session_data(session_id=session.get('session_id')))
            level_id = level.get('level_status') + 1
            if level_id > 10:
                return render_template('thank_you.html', name=session.get('user_name'))
                # remove_session_data(session_id=session.get('session_id'))
            level['level_status'] = level_id
            level_name = get_level_name(level_id)
            update_or_create_session(session_id=session.get('session_id'), data=level)
            return render_template('levels.html', level_id=level_id, level_name=level_name)
        else:
            return redirect(url_for('intro'))


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

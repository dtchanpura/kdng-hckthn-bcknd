from uuid import uuid4


def generate_random_session_id():
    """
    Generate a random string for unique session id.
    TODO Add check in database

    :return:
    """
    return str(uuid4())

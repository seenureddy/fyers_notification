
# Third party

import os


ALLOWED_EXTENSIONS = {'csv'}


def get_env(key):
    """
    :param key:
    :return:
    """
    try:
        value = os.getenv(key)
    except TypeError:
        print(f"The ENV variable {key} is not set correctly")
        value = None
    return value


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""
This file contains definitions of several functions for interacting
with the wakeup call backend
"""

import requests

import settings

def registerNewUser(params):
    """
    Forwards registration request to the API backend

    Returns a dict of the form:
        success => bool indicating successful registration or failure
        error => Error object
    """
    response = requests.post(settings.BACKEND_URL + '/users', params=params)
    try:
        resp_content = response.json()
        if resp_content['Status'] != 200:
            return {'success': False, 'error': resp_content['Error']}
    except:
        error = {'Message': 'Internal server error'}
        return {'success': False, 'error': error}

    return {'success': True, 'error': None}

def loginUser(params):
    """
    Signs a user in to the system by forwarding request to the backend API

    Returns a dict of the form:
        success => True if log in successful, false otherwise
        cookie => cookie generated by the backend to forward to client, or None
        on log in failure
        error => Error object, or None on success
    """
    response = requests.post(settings.BACKEND_URL + '/users/login', params=params)
    try:
        resp_content = response.json()
        if resp_content['Status'] != 200:
            return {'success': False, 'cookie': None, 'error': resp_content['Error']}
        else:
            generated_cookie = response.headers['Set-Cookie']
            return {'success': True, 'cookie': generated_cookie, 'error': None}
    except:
        error = {'Message': 'Internal server error'}
        return {'success': False, 'cookie': None, 'error': error}

    # Shouldn't reach here, but just in case
    return None

def verify_cookie(user_cookie):
    """
    Verifies that the given cookie is valid by checking with the backend

    Returns True if the cookie is a valid session, False otherwise
    TODO: Implement this on the backend
    """
    return True
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

        TODO: Change to just return tuples, the dicts are ugly
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
    """
    cookie = {'wakeup-session': user_cookie}
    response = requests.get(settings.BACKEND_URL + '/users/sessioncheck', cookies=cookie)
    return True if response.status_code == 200 else False

def get_user_info(request):
    """ Returns info for the currently logged in user """
    response = requests.get(settings.BACKEND_URL + '/users/info', cookies=request.cookies)
    if response.status_code != 200: return None # TODO: Handle specific errors

    try:
        resp_content = response.json()
        return resp_content['Data']
    except:
        return None

    # Shouldn't reach here, but just in case...
    return None


def get_user_groups(username, cookies):
    """ Returns all groups for the given user """
    url = '/users/{username}/groups'.format(username=username)
    response = requests.get(settings.BACKEND_URL + url, cookies=cookies)
    if response.status_code != 200: return []

    try:
        content = response.json()
        return content['Data']
    except:
        return []

    # Shouldn't reach here
    return []

def get_user_from_number(phone_number):
    """ Queries the API for a user with the given phone number """
    print 'Requesting user with phone number: {}'.format(phone_number)
    url = '/users'
    params = {'phoneNumber': phone_number}
    response = requests.get(settings.BACKEND_URL + url, params=params)
    if response.status_code != 200: return None

    try:
        content = response.json()
        return content['Data']
    except:
        return None

    return None

"""
Groups API Interactions
TODO: Decompose this + user api interactions above
"""

def create_group(params, cookies):
    """ Creates a group from the given form parameters """
    response = requests.post(settings.BACKEND_URL + '/groups', params=params, cookies=cookies)
    try:
        content = response.json()
        if response.status_code != 200:
            return False, content['Error']
    except:
        error = {'Message': 'Internal Server Error'}
        return False, error

    # If we reach here, group creation was successful
    return True, None

def get_group_info(group_name):
    """ Fetchs information for the given group """
    url = '/groups/{group}'.format(group=group_name)
    response = requests.get(settings.BACKEND_URL + url)
    if response.status_code != 200: return None

    try:
        content = response.json()
        return content['Data']
    except:
        return None

    return None

def get_group_users(group_name):
    """ Fetchs information on all users in the given group """
    url = '/groups/{group}/users'.format(group=group_name)
    response = requests.get(settings.BACKEND_URL + url)
    if response.status_code != 200: return []

    try:
        content = response.json()
        return content['Data']
    except:
        return []

    return []

def get_group_from_number(phone_number):
    """ Queries the API for a group matching the given phone number """
    return {}


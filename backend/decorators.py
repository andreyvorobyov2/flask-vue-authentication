from flask import session, request

def login_required(f):
    def decorator(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            if f.__name__.startswith('socket'):
                return False # server reject connection
            return {'error': 'You must be logged in to do that. Please log in or sign up.'}, 401
        else:
            return f(user_id, *args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator


def credentials_required(f):
    def decorator(*args, **kwargs):
        rq = request.get_json()
        username = rq.get('username')
        password = rq.get('password')

        if not username or not password:
            return {'error': 'Username and Password is required fields'}, 401
        else:
            return f(username, password, *args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator

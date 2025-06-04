from flask import request, make_response, session
from flask.sessions import SecureCookieSessionInterface
import bcrypt
from config import app, db
from models import User

session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)


@app.after_request
def cookies(response):
    client_cookie = session_cookie.dumps(dict(session))
    response.headers.add("Set-Cookie", f"session={client_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
    return response


def login_required(f):
    def decorator(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
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


@app.route('/', methods=["GET"])
def home_page():
    return make_response('API page', 200)

@app.route('/signup', methods=["POST"])
@credentials_required
def signup(username, password):
    if request.method == "POST":
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username,
            password=hashed_password.decode('utf-8'),
        )
        if new_user:
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                return {'error': 'Invalid Username or Password. Please try again.'}, 401
            session['user_id'] = new_user.id
            return make_response({'username': new_user.username}, 201)
        else:
            return {'error': 'Invalid Username or Password. Please try again.'}, 401


@app.route('/login', methods=["POST"])
@credentials_required
def login(username, password):
    if request.method == "POST":
        user = User.query.filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            return make_response({'username': user.username}, 200)
        else:
            return {'error': 'Invalid Username or Password. Please try again.'}, 401


@app.route('/logout', methods=["DELETE"])
def logout():
    if request.method == "DELETE":
        session['user_id'] = None
        response = make_response('', 204)
        return response


@app.route('/myprojects', methods=['GET'])
@login_required
def myprojects(user_id):
    # sql query to database
    return make_response({'backendtext': 'this text from backend only for user_id {}'.format(user_id)}, 200)



if __name__ == '__main__':
    app.run()

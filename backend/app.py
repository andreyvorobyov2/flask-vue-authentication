import bcrypt, datetime
# from flask.sessions import SecureCookieSessionInterface
from flask import session, request, make_response
from models import User
from flask_socketio import emit
from config import app, db, socketio, redis_manager
from decorators import login_required, credentials_required

# not needed if use Redis
# session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)
# @app.after_request
# def cookies(response):
#     client_cookie = session_cookie.dumps(dict(session))
#     response.headers.add("Set-Cookie", f"session={client_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
#     return response

# http routes

@app.route('/', methods=["GET"])
def home_page():
    return make_response('API index page', 200)


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
            except Exception as e:
                return {'error': 'Invalid Username or Password. Please try again. \n {0}'.format(e)}, 401
            session['user_id'] = new_user.id
            session['username'] = new_user.username

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
            session['username'] = user.username
            return make_response({'username': user.username}, 200)
        else:
            return {'error': 'Invalid Username or Password. Please try again.'}, 401


@app.route('/logout', methods=["DELETE"])
def logout():
    if request.method == "DELETE":
        session['user_id'] = None
        response = make_response('', 204)
        return response


@app.route('/userlist', methods=["GET"])
@login_required
def user_list(user_id):
    if request.method == "GET":
        online_users = []
        for rec in User.query.all():
            socket_status = redis_manager.get_status(rec.username)
            if request.args.get('only_online') == 'true' and socket_status == 'offline':
                continue

            count_unread_messages = redis_manager.get_count_unread_messages(rec.username, session['username'])
            online_users.append(
                {'id': rec.id,
                 'username': rec.username,
                 'created_at': rec.created_at,
                 'socket_status': socket_status.value,
                 'count_unread_messages': count_unread_messages})
        return make_response(online_users, 200)


@app.route('/myprojects', methods=['GET'])
@login_required
def myprojects(user_id):
    # sql query to database
    return make_response({'backendtext': 'this text from backend only for user_id {}'.format(user_id)}, 200)


@socketio.on('connect')
@login_required
def socket_connect(user_id):
    redis_manager.set_status_online(request, session)
    emit('user_connect', {
        'username': session['username']}, broadcast=True)


@socketio.on('disconnect')
def socket_disconnect():
    redis_manager.set_status_offline(request, session)
    emit('user_disconnect', {
        'username': session['username']}, broadcast=True)


@socketio.on('send_message_to_user')
@login_required
def socket_send_message_to_user(user_id, to_username, message):
    msg = {
        'from': session['username'],
        'to': to_username,
        'date': str(datetime.datetime.now()),
        'message': message,
    }
    redis_manager.save_message(msg)
    redis_manager.increase_unread_messages(msg)
    for sid in redis_manager.list_sids(to_username):
        emit('receive_message_from_user',msg, to=sid)
    emit('receive_message_from_user', msg)


@socketio.on('read_message_confirm')
@login_required
def socket_read_message_confirm(user_id, from_username):
    redis_manager.clear_unread_messages(from_username, session['username'])


@socketio.on('load_messages')
@login_required
def socket_load_messages(user_id, from_username):
    messages = redis_manager.list_messages(from_username, session['username'])
    emit('messages_loaded', {'messages':messages})

if __name__ == '__main__':
    redis_manager.reset()
    # socketio.run(app=app, host='127.0.0.1', allow_unsafe_werkzeug=True)
    socketio.run(app=app, host='172.20.0.10', allow_unsafe_werkzeug=True)
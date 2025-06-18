import pickle, uuid
from enum import Enum

CHAT_SIDS_KEY = 'chat:sids:{}'
CHAT_STATUS_KEY = 'chat:status:{}'
CHAT_MESSAGE_KEY = 'chat:message:{users}:{message_id}'
CHAT_NEW_MESSAGE_COUNT = 'chat:new_message_count:{from_username}:{to_username}'


class ClientStatus(Enum):
    ONLINE = 'Online'
    OFFLINE = 'Offline'


class RedisManager:
    def __init__(self, redis_db):
        self.redis_db = redis_db

    def reset(self):
        for key in self.redis_db.scan_iter(CHAT_STATUS_KEY.format('*')):
            self.redis_db.delete(key)
        for key in self.redis_db.scan_iter(CHAT_SIDS_KEY.format('*')):
            self.redis_db.delete(key)


    def set_status_online(self, request, session):
        username = session['username']
        sid = request.sid
        self.__redis_set(CHAT_STATUS_KEY.format(username), ClientStatus.ONLINE)
        self.__add_sid(username, sid)

    def set_status_offline(self, request, session):
        username = session['username']
        sid = request.sid
        self.__redis_set(CHAT_STATUS_KEY.format(session['username']), ClientStatus.OFFLINE)
        self.__remove_sid(username, sid)

    def get_status(self, username):
        return self.__redis_get(CHAT_STATUS_KEY.format(username), ClientStatus.OFFLINE)


    def save_message(self, msg):
        key = self.__generate_message_key(msg['from'], msg['to'])
        self.__redis_set(key, msg);


    def list_messages(self, username1, username2):
        key_template = self.__generate_message_key(username1, username2, '*')
        messages = []
        for key in self.redis_db.scan_iter(key_template):
            messages.append(self.__redis_get(key,{}))
        return sorted(messages, key=lambda x: x['date'])


    def increase_unread_messages(self, msg):
        key = CHAT_NEW_MESSAGE_COUNT.format(from_username=msg['from'], to_username=msg['to'])
        current_unread = self.__redis_get(key, 0)
        self.__redis_set(key, current_unread + 1)


    def get_count_unread_messages(self, from_username, to_username):
        key = CHAT_NEW_MESSAGE_COUNT.format(from_username=from_username, to_username=to_username)
        return self.__redis_get(key, 0)

    def clear_unread_messages(self, from_username, to_username):
        key = CHAT_NEW_MESSAGE_COUNT.format(from_username=from_username, to_username=to_username)
        self.__redis_set(key, 0)


    def __generate_message_key(self, username1, username2, message_id=None):
        users = [username1, username2]
        users.sort()
        return CHAT_MESSAGE_KEY.format(users='-'.join(users),
                                        message_id= message_id if message_id else str(uuid.uuid4()))

    def __add_sid(self, username, sid):
        self.__update_sids(username, sid, 'add')

    def __remove_sid(self, username, sid):
        self.__update_sids(username, sid, 'remove')

    def list_sids(self, username):
        return self.__redis_get(CHAT_SIDS_KEY.format(username), [])

    def __update_sids(self, username, sid, operation):
        key = CHAT_SIDS_KEY.format(username)
        sids = self.__redis_get(key, [])
        if operation == 'add':
            if sid not in sids:
                sids.append(sid)
        elif operation == 'remove':
            if sid in sids:
                sids.remove(sid)
        else:
            raise ValueError()
        self.__redis_set(key, sids)

    def __redis_get(self, key, default=None):
        value = self.redis_db.get(key)
        if value:
            return pickle.loads(value)
        return default

    def __redis_set(self, key, value):
        self.redis_db.set(key, pickle.dumps(value))

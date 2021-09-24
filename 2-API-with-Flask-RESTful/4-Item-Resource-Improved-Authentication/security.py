from werkzeug.security import safe_str_cmp
from user import User


users = [
    User(1, 'user1', 's3cr3t$1'),
    User(2, 'user2', 's3cr3t$2')
]


username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity'] # user_id is retrieved from the JWT token here
    return userid_table.get(user_id, None)
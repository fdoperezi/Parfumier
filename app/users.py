from werkzeug.security import check_password_hash
from app import login_manager, mongo, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import logging  # Delete this for prod

# LOGGING
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s %(name)s - %(filename)s :: %(lineno)d - %(levelname)s - %(message)s\n', datefmt='%Y-%m-%d %H:%M:%S')


class User():
    def __init__(self, username, first_name, last_name, email, _id, is_admin, avatar):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._id = _id
        self.is_admin = is_admin
        self.avatar = avatar

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


# START ATTEMPT TO SEND RESET PASSWORD EMAIL #


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY', expires_sec])
        return s.dumps({'_id': self._id})

# COREY
    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            _id = s.loads(token)['_id']
            logging.debug(_id) # LOGGING
        except:
            return None
        logging.debug(_id) # LOGGING
        return User.find_one({'_id': _id})

# COREY
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)
    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# END ATTEMPT TO SEND RESET PASSWORD EMAIL #


@login_manager.user_loader
def load_user(email):
    user = mongo.db.users.find_one({'email': email})
    if not user:
        return None
    return User(user['username'], user['first_name'], user['last_name'], user['email'], user['_id'], user['is_admin'], user['avatar'])

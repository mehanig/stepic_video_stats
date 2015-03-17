from app import mongo_db_collection

class User(object):
    pass
    # id = db.Column(db.Integer, primary_key=True)
    # nickname = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)

    # def __init__(self):
    id = ''
    nickname = ''
    email = ''
    passhash = ''

    def __init__(self, username, passhash):
        try:
            self.nickname = username
            self.passhash = passhash
            self.id = 1
            print('LOGIN SUCCES!!')
        except Exception as e:
            print('ERROR WHILE LOGIN: ', e)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.nickname)  # python 2
        except NameError:
            return str(self.nickname)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)
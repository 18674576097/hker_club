class Config:
    CSRF_ENABLED = True
    SECRET_KEY = '154165483'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1qaz@WSX@localhost/hker_club'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False
    MAIL_DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '154165483@qq.com'
    MAIL_PASSWORD = 'wkusymegpmefcagi'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Hker_Club]'
    FLASKY_MAIL_SENDER = '154165483@qq.com'
    FLASKY_ADMIN = '154165483@qq.com'
    FLASKY_MAIL_SUBJECT = 'New User'

    @staticmethod
    def init_app(app):
        pass

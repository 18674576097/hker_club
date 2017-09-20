import hashlib

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db
from app import login_manager

#用户表
class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True, index=True)
    # 外键role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    #单独调用password返回错误————password不可读（数据库根本就没有存储）
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #用户输入的password转化为hash并存储数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #将用户输入的密码，跟hash比对，一致返回true
    def verify_password(self, password):
       return check_password_hash(self.password_hash, password)

    #生成一个注册令牌，有效期半个小时
    def generate_confirmation_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': self.id})

    #检验令牌是否通过，通过把confirmed字段设置为True
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


    # 生成一个更改密码的令牌
    def gengenerate_password_change_token(self,new_password,expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'change_password': self.id, 'new_password': new_password})


    # 验证密码更改令牌
    def change_password(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_password') != self.id:
            return False
        new_password = data.get('new_password')
        if new_password is None:
            return False
        self.password_hash = generate_password_hash(new_password)
        db.session.add(self)
        db.session.commit()
        return True


    #生成一个更改Email的令牌
    def generate_email_change_token(self, new_email, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    # 验证Email更改令牌
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True
    # def is_authenticated(self): 如果用户已经登录，必须返回 True，否则返回 False
    #     return True
    # def is_active(self):如果允许用户登录，必须返回 True，否则返回 False。如果要禁用账户，可以返回 False
    #     return True
    # def is_anonymous(self):对普通用户必须返回 False
    #     return False
    # def get_id(self):必须返回用户的唯一标识符，使用 Unicode 编码字符串
    #     return self.id
    #这 4 个方法可以在模型类中作为方法直接实现，不过还有一种更简单的替代方案。FlaskLogin 提供了一个 UserMixin 类，其中包含这些方法的默认实现，且能满足大多数需求。


        # 生成一个重置密码的令牌---密码
    def gengenerate_password_reset_token(self,  expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset_password': self.id})

        # 验证重置密码更改令牌--密码
    def reset_password(self, token, renew_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset_password') != self.id:
            return False
        renew_password = renew_password
        if renew_password is None:
            return False
        self.password_hash = generate_password_hash(renew_password)
        db.session.add(self)
        db.session.commit()
        return True





    def __repr__(self):
        return '<User %r>' % self.username
    # 用户回掉函数
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))


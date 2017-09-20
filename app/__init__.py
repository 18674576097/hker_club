#导入包
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_script import Manager, Shell



#定义Bootstrap对象
bootstrap=Bootstrap()

#定义数据库对象
db = SQLAlchemy()

#定义令牌对象
csrf = CSRFProtect()

#定义邮箱对象
mail = Mail()

#定义数据库迁移对象
migrate = Migrate()

#登录管理
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# app = Flask(__name__)

#工厂
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    config_name.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)


    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix='/main')
    return app












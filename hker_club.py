from os import environ
from app import db
from app import create_app
from config import Config



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app = create_app(Config())
    # app = create_app(Config())
    # migrate = Migrate(app, db)
    # # 定义数据库管理对象
    # # manager = Manager(app)
    # migrate.add_command('db',MigrateCommand)

    app.run(HOST, PORT)
    # app.run()
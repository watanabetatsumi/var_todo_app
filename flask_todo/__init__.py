from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# flask_loginのLoginManagerクラスをインスタンス化しています
login_manager = LoginManager()

# ログインしていない場合、ログインを促すようにtodo_app.login( /login )へ遷移させます
login_manager.login_view = 'todo_app.login'

# login_viewメソッドが実行されたときに表示されるメッセージ
login_manager.login_message = 'ログインして下さい'

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # SECRET_KEYを定義
    app.config['SECRET_KEY'] = 'mysite'

    # データベースとの接続の設定を定義
    app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': "todo_user",
    'password': "todo_user_password",
    'host': "localhost",
    'db_name': "ToDo_DB"
     })


    
    # Trueにするとメモリを消費してしまうため、今回はFalse
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from flask_todo.views import bp
    
    # 後述するviews.pyに記述するBlueprintという機能を使用できるように設定
    app.register_blueprint(bp)
    
    # MySQLをFlaskアプリで使用できるように設定
    db.init_app(app)
    
    # MySQLのテーブルの作成や更新ができるように設定
    migrate.init_app(app, db)
    
    # FlaskアプリでLoginManagerを使用できるように設定
    login_manager.init_app(app)
    
    return app

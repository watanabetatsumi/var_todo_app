from flask_todo import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func

# 認証ユーザーの呼び出し方を定義します
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
# Userテーブルの定義
class User(UserMixin, db.Model):
    # テーブル名
    __tablename__ = 'users'

    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    # Userクラスをインスタンス化した時に各カラムを引数として使えるように設定します
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    # 入力されたパスワードとハッシュ化されたパスワードを比較して検証する
    def validate_password(self, password):
        return check_password_hash(self.password, password)

    # privteなメソッド
    @classmethod

    # emailで検索した時に一番最初にあるemailを取得します
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


        # Taskテーブルの定義
class Task(db.Model):
    # テーブル名
    __tablename__ = 'tasks'

    # カラム定義
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # タスクのタイトル
    title = db.Column(db.String(64), index=True, nullable=False)
    # タスクの内容
    detail = db.Column(db.String(128), index=True)
    # タスクの期限（終了日時）
    end_time = db.Column(db.DateTime, nullable=False)
    # タスクの作成日時
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    # タスクの更新日時
    update_at = db.Column(db.DateTime, onupdate=func.utc_timestamp(), nullable=True)
    # usersテーブルのidを外部キーとして設定している
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
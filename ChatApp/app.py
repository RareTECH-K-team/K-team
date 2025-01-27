from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from datetime import timedelta
import hashlib
import uuid
import re
import os
from models import User
# from assets import bundle_css_files # type: ignore

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

# アプリケーション初期化
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 静的ファイルキャッシュ設定（開発中はコメントアウト）
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400
# bundle_css_files(app)

# アクセス権限がない場合の画面
@app.route('/access_denied', methods=['GET'])
def access_denied():
    return render_template('access_denied.html')

# ログイン画面の表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        flash('メールアドレスまたはパスワードが空です。')
        return redirect(url_for('login_view'))

    # ユーザーをデータベースから取得
    user = User.find_by_email(email)
    if user is None:
        flash('このユーザーは存在しません。')
        return redirect(url_for('login_view'))

    # パスワードのハッシュ化と照合
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashed_password != user['password']:
        flash('パスワードが間違っています。')
        return redirect(url_for('login_view'))

    # 削除されたユーザーのチェック
    if user.get('is_deleted', False):
        flash('アクセス権限がありません。')
        return redirect(url_for('access_denied'))

    # ログイン成功
    session['uid'] = user['uid']
    session['role'] = user.get('role', 'user')  # ユーザーの役割を保存

    # 役割に応じてリダイレクト
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif session['role'] == 'user':
        return redirect(url_for('channels_view'))
    else:
        flash('不正な権限が検出されました。')
        return redirect(url_for('access_denied'))



# 管理者ダッシュボード
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('管理者のみアクセス可能です。')
        return redirect(url_for('access_denied'))
    return render_template('admin_dashboard.html')

# チャンネル画面（一般ユーザー）
@app.route('/channels', methods=['GET'])
def channels_view():
    if session.get('role') != 'user':
        flash('一般ユーザーのみアクセス可能です。')
        return redirect(url_for('access_denied'))
    return render_template('channels.html')

# アプリケーション起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

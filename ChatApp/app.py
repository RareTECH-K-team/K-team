from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from datetime import timedelta
import hashlib
import uuid
import re
import os
from models import User, Channel
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

#ルートページのリダイレクト処理
@app.route('/',methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('channels_view'))


# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')


# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    user_name = request.form.get('username')
    print(user_name)
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('confirm-password')

    if user_name == '' or email == '' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            User.create(user_name, email, password)
            UserId = str(user_id)
            session['user_id'] = UserId
            session['role'] = 'general_user'
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('signup_process'))


# アクセス権限がない場合の画面
@app.route('/access_denied', methods=['GET'])
def access_denied():
    return render_template('auth/access_denied.html')


# ログイン画面の表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')


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
    session['uid'] = user['user_id']
    if user['is_admin'] == True:
        session['role'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    elif user['is_admin'] == False:
        session['role'] = 'general_user'
        return redirect(url_for('work_channels_view'))
    else:
        return redirect(url_for('access_denied'))


# ログアウト処理
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))


# 管理者ダッシュボード
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('管理者のみアクセス可能です。')
        return redirect(url_for('access_denied'))
    return render_template('auth/admin_dashboard.html')


# チャンネル画面（一般ユーザー_work）
@app.route('/works_channels', methods=['GET'])
def work_channels_view():
    if session.get('role') != 'general_user':
        print(session.get('role'))
        return redirect(url_for('access_denied'))
    else:
        work_channels = Channel.get_all(1)
        work_channels.reverse()
        print(work_channels)
        return render_template('utils/works_channels.html', channels = work_channels)


# チャンネル画面（一般ユーザー_private）
@app.route('/private_channels', methods=['GET'])
def private_channels_view():
    if session.get('role') != 'general_user':
        flash('一般ユーザーのみアクセス可能です。')
        return redirect(url_for('access_denied'))
    else:
        private_channels = Channel.get_all(2)
        private_channels.reverse()
        print(private_channels)
        return render_template('utils/private_channels.html', channels = private_channels)


# アプリケーション起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

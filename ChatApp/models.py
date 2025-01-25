import pymysql
from flask import abort
from DB import DB # type: ignore

# データベース接続クラス
class User:
    @staticmethod
    def getUser(email):
        """
        メールアドレスでユーザーを検索
        :param email: メールアドレス
        :return: ユーザー情報の辞書（存在しない場合は None）
        """
        conn = DB.getConnection()  # データベース接続を取得
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(f"{e} が発生しています")  # エラー内容を表示
            return None
        finally:
            cur.close()
import pymysql
from flask import abort
from util.DB import DB # type: ignore

db_pool = DB.init_db_pool()

#ユーザークラス
class User:
    @classmethod
    def create(cls, user_name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_name, email, password, is_admin, delete_flag) VALUES (%s, %s, %s, 0, 0);"
                cur.execute(sql, (user_name, email, password,)) # type: ignore
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
                with conn.cursor() as cur:
                     sql = "SELECT * FROM users WHERE email=%s;"
                     cur.execute(sql, (email,))
                     user = cur.fetchone()
                return user
        except pymysql.Error as e:
             print(f'エラーが発生しています：{e}')
             abort(500)
        finally:
             db_pool.release(conn)


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
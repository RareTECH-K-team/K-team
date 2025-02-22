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


    @classmethod
    def get_all(cls, delete_flag):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE is_admin = 0 AND delete_flag = %s;"
                cur.execute(sql, (delete_flag,))
                user = cur.fetchall()
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


# チャンネルクラス
class Channel:
    @classmethod
    def create(cls, user_id, new_channel_name, distinction_type_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO channels (user_id, channel_name, distinction_type_id) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_id, new_channel_name, distinction_type_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    @classmethod
    def get_all(cls, distinction_type_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE distinction_type_id = %s;"
                cur.execute(sql, distinction_type_id)
                channels = cur.fetchall()
                return channels
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    def find_by_channels_id(channels_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE channel_id = %s;"
                cur.execute(sql, (channels_id,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)   


    @classmethod
    def find_by_name(cls, channels_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM channels WHERE channel_name=%s;'
                cur.execute(sql, (channels_name,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    @classmethod
    def update(cls, new_channel_name, distinction_type_id,):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE channels SET name=%s, distinction_type=%s;"
                cur.execute(sql, (new_channel_name, distinction_type_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


    @classmethod
    def delete(cls, channels_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM channels WHERE id=%s;"
                cur.execute(sql, (channels_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# メッセージクラス
class Message:
    @staticmethod
    def create(uid, cid, message):
        """
        新しいメッセージをDBに挿入
        """
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages (user_id, channel_id, message) VALUES (%s, %s, %s)"
                cur.execute(sql, (uid, cid, message))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しました: {e}")
            return None
        finally:
            db_pool.release(conn)


    @staticmethod
    def getMessagesByChannel(channels_id):
        """
        指定されたチャンネルのメッセージ一覧を取得する関数を定義
        """
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        m.message_id,
                        u.user_id,
                        u.user_name,
                        m.message,
                        m.fixed_message_id,
                        m.created_at
                    FROM
                        messages AS m
                    INNER JOIN
                        users AS u ON m.user_id = u.user_id
                    WHERE
                        m.channel_id = %s
                    ORDER BY
                        m.created_at ASC;
                """
                cur.execute(sql, (channels_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラー: {e}")
            abort(500)

        finally:
            db_pool.release(conn)


    @classmethod
    def get_fixed_messages(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM fixed_messages;"
                cur.execute(sql)
                fixed_messages = cur.fetchall()
                return fixed_messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

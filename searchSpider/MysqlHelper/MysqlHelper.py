import pymysql

#定义mysql帮助类，完成一些数据库相关操作
class MysqlHelper(object):
    conn = None

    def __init__(self, host, username, password, db, charset='utf8', port=3306):
        """
        Init func
        :param host: 主机
        :param username: 用户名
        :param password: 密码
        :param db: 数据库名称
        :param charset: 字符类型
        :param port: 端口号
        """
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        """
        数据库连接
        :return:
        """
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password, db=self.db,
                            charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        """
        数据库连接关闭
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        """
        获取一条数据
        :param sql: SQL语句
        :param params:
        :return:
        """
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params=()):
        """
        获取多条数据
        :param sql: SQL语句
        :param params:
        :return:
        """
        list_data = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list_data

    def insert(self, sql, params =()):
        """
        插入操作
        :param sql:
        :param params:
        :return:
        """
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        """
        更新操作
        :param sql:
        :param params:
        :return:
        """
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        """
        删除操作
        :param sql:
        :param params:
        :return:
        """
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        """
        编辑操作
        :param sql:
        :param params:
        :return:
        """
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count



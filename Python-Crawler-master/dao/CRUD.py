
import pymysql
import traceback

#mysql增删改查类
class CRUD(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.username = 'root'
        self.pwd = '123456'
        self.db = 'python_test'

    #查询方法
    def select(self, selectSql):
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(self.host, self.username, self.pwd, self.db, port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        try:
            cur.execute(selectSql)
            data = cur.fetchall()
            return data
            print("查询成功")
        except Exception:
            print("查询失败:",Exception)
        finally:
            cur.close()  # 关闭游标
            conn.close()  # 释放数据库资源

    def insert(self, insert_sql):
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(self.host, self.username, self.pwd, self.db, port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        try:
            # 执行sql语句
            cur.execute(insert_sql)
            # 提交到数据库执行
            conn.commit()
            # print("insert成功")
        except Exception:
            print("insert失败:",Exception)
            # 将错误日志输入到目录文件中
            f = open("d:log.txt", 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            # 如果发生错误则回滚
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    # update
    def operateDB(self, sql):
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(self.host, self.username, self.pwd, self.db, port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            conn.commit()
            print("operateDB成功")
        except Exception:
            print("operateDB失败:", Exception)
            # 将错误日志输入到目录文件中
            f = open("d:log.txt", 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            # 如果发生错误则回滚
            conn.rollback()
        finally:
            print('mysql连接关闭')
            cur.close()
            conn.close()

    # 删除整个表
    def deleteAllTableDate(self,sql):
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(self.host, self.username, self.pwd, self.db, port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            conn.commit()
            print("delete成功")
        except Exception:
            print("delete失败:", Exception)
            # 将错误日志输入到目录文件中
            f = open("d:log.txt", 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            # 如果发生错误则回滚
            conn.rollback()
        finally:
            cur.close()
            conn.close()

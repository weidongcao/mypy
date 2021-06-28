# -*- coding:utf-8 -*-
# import clickhouse_driver
import clickhouse_driver

from helper.helper_apollo import apollo_helper
from helper.helper_logger import get_logger

logger = get_logger(__name__)

DB_NAME = "clickhouse"

clickhouse_conf = apollo_helper.get_value("db.ch", namespace="commons.yml")


class ClickhouseHelper:
    """
    ClickHouse连接工具类
    因为ClickHouse与传统的数据库有些一样,所以不通用DBHelper
    """

    def __init__(self, host, port, username, password, database, charset="utf8", db_type="clickhouse"):
        self.host = host
        self.port = str(port)
        self.username = username
        self.password = password
        self.database = database
        self.charset = charset
        self.db_type = db_type
        self.conn = None
        self.conn = None
        self.get_client()

    def query(self, sql, clz=list):
        """
        查询返回多条数据
        :param clz:
        :param sql:
        :return:
        """
        return self.execute(sql, clz=clz)

    def query_one(self, sql, clz=tuple):
        """
        查询单条数据,
        返回指定的对象类型
        :param sql:
        :param clz:
        :return:
        """
        lt = self.query(sql, clz=list) if clz == tuple else self.query(sql, clz)

        return lt[0] if lt else None

    def insert(self, sql):
        """
        插入数据
        """
        self.execute(sql)

    def execute(self, sql, clz=list):
        """
        执行sql,ClickHouse中查询,插入,修改,删除都是一样的
        """
        try:
            return self.conn.execute(sql) if list == clz else self.convert2entity(
                self.conn.execute(sql, with_column_types=True), clz
            )
        except Exception as e:
            logger.error('SQL: %s\n  %s ' % (sql, e))
            return None

    def insert_bulk(self, sql, insert_data):
        """
        execute(sql) : 接受一条语句从而执行
        executemany(template,args)：能同时执行多条语句，执行同样多的语句可比execute()快很多，强烈建议执行多条语句时使用executemany
        template : sql模板字符串,　 例如 ‘insert into table(id,name,age) values(%s,%s,%s)’
        args: 模板字符串中的参数，是一个list，在list中的每一个元素必须是元组！！！ 　例如： [(1,‘mike’),(2,‘jordan’),(3,‘james’),(4,‘rose’)]
        :param sql:
        :param insert_data:
        :return:
        """
        if len(insert_data) == 0:
            logger.warning("empty insert data list, sql: {}".format(sql))
            return

        try:
            # 连接数据库
            # self.get_connect()
            # 执行sql命令
            return self.conn.execute(sql, insert_data)
        except Exception as e:
            logger.info(e)
            raise e

    def get_client(self):
        if "clickhouse" == self.db_type:
            connection = clickhouse_driver.Client(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
            )
            self.conn = connection

            logger.info("{} version: {}".format(self.db_type, self.conn.execute("SELECT version()")[0][0]))
            logger.info(f"{self.db_type} connection init success ...")

    @staticmethod
    def convert2entity(result_data, clz=None):
        """
        如果类型什么都不传只返回值
        如果类型为基本数据类型返回单个值
        如果指定类型转为指定的类型
        :return:
        """
        columns = [c[0] for c in result_data[1]]

        values = [e for e in result_data[0]]

        if clz in [str, int, bool]:
            lt = [e[0] for e in values]
            return lt[0]
        elif clz is None:
            return values
        else:
            return [clz(**dict(zip(columns, record))) for record in result_data[0]]





clickhouse_helper = ClickhouseHelper(
    host=clickhouse_conf["host"],
    port=clickhouse_conf["port"],
    username=clickhouse_conf["user"],
    password=clickhouse_conf["password"],
    database=clickhouse_conf["database"],
    db_type=DB_NAME
)

if __name__ == '__main__':
    # print(1)
    print(clickhouse_helper.execute("ALTER TABLE rpt.rpt_basic_business_trend_1min MODIFY TTL parse_time + toIntervalMonth(1)"))

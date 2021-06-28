# -*- coding:utf-8 -*-

from helper.helper_apollo import apollo_helper
from helper.helper_db import DBHelper
from helper.helper_logger import get_logger

logger = get_logger(__name__)

#################

db_type = "postgresql"
postgre_conf = apollo_helper.get_value("db.pg", namespace="commons.yml")
logger.debug(f"PostgreSQL connection info, "
             f"host: {postgre_conf.get('host')}, "
             f"port: {postgre_conf.get('port')}, "
             f"database: {postgre_conf.get('database')}, "
             f"username: {postgre_conf.get('user')}"
             )
postgres_helper = DBHelper(
    host=postgre_conf["host"],
    port=str(postgre_conf["port"]),
    username=postgre_conf["user"],
    password=postgre_conf["password"],
    database=postgre_conf["database"],
    db_type=db_type
)

if __name__ == '__main__':
    val = postgres_helper.query('select version()')
    print(type(val))
    print(val)

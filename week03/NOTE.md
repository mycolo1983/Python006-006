## 1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用户。
   
### . 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
```
# 修改字符集配置项
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4

[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
symbolic-links=0
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

interactive_timeout = 28800        #针对交互连接超时时间
wait_timeout = 28800               #针对非交互连接超时时间：python到mysql的连接
max_connections = 1000             #MySQL的最大连接数
character_set_server = utf8mb4     #MySQL字符集设置；默认内部操作字符集
init_connect = 'SET NAMES utf8mb4' #服务器为每个连接的客户端执行的字符串
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```
```
mysql> show variables like '%character%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8mb4                    |
| character_set_connection | utf8mb4                    |
| character_set_database   | utf8mb4                    |
| character_set_filesystem | binary                     |
| character_set_results    | utf8mb4                    |
| character_set_server     | utf8mb4                    |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```
```
mysql> show variables like '%collation_%';
+----------------------+--------------------+
| Variable_name        | Value              |
+----------------------+--------------------+
| collation_connection | utf8mb4_unicode_ci |
| collation_database   | utf8mb4_unicode_ci |
| collation_server     | utf8mb4_unicode_ci |
+----------------------+--------------------+
3 rows in set (0.00 sec)
```
### . 将增加远程用户的 SQL 语句作为作业内容提交
    ```
    GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
    FLUSH PRIVILEGES;
    ```
## 2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

## .用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
    ```
    import pymysql
    from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey,DateTime,Date,Enum
    from sqlalchemy.ext.declarative import declarative_base
    from datetime import datetime 

    Base = declarative_base()
    class Author_table(Base): 
        __tablename__ = 'userinfo' 
        user_id = Column(Integer(), primary_key=True) 
        username = Column(String(15), nullable=False, unique=True)
        age = Column(Integer())
        dob = Column(Date())
        gender = Column(Enum("男生","女生"),default="男生")
        edu = Column(Enum("大专","本科","硕士","博士"),default="本科")
        # salary = Column(Integer())
        created_on = Column(DateTime(), default=datetime.now) 
        updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    dburl="mysql+pymysql://testuser:testpass@mysqlsev1:3306/testdb?charset=utf8mb4" #为了避免出错，显示的指定了字符集，并且告诉其他人使用的默认字符集是什么样
    engine=create_engine(dburl, echo=True, encoding="utf-8") #连接的时候使用的编码是utf-8,如果不指定，会使用操作系统默认的编码
    Base.metadata.create_all(engine)
    ```
## .将 ORM、插入、查询语句作为作业内容提交
```
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey,DateTime,Date,Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime 
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Author_table(Base): 
    __tablename__ = 'userinfo' 
    user_id = Column(Integer(), primary_key=True) 
    username = Column(String(15), nullable=False, unique=True)
    age = Column(Integer())
    dob = Column(Date())
    gender = Column(Enum("男生","女生"),default="男生")
    edu = Column(Enum("大专","本科","硕士","博士"),default="本科")
    # salary = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now) 
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

dburl = "mysql+pymysql://testuser:testpass@mysqlsev1:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")

# 创建session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 增加数据
book_demo = Author_table(user_id=11,username="黄秋",age=45,dob="1976-10-12",gender="男生",edu="大专")
book_demo1 = Author_table(user_id=12,username="绿夏",age=30,dob="1991-7-22",gender="女生")
book_demo2 = Author_table(user_id=13,username="稚春",age=25,dob="1996-3-9",gender="男生")
session.add(book_demo)
session.add(book_demo1)
session.add(book_demo2)
session.commit()

#查询数据
result = session.query(Author_table).all()
print(result)
session.commit()
```

## 3. 为以下 sql 语句标注执行顺序：
```
SELECT DISTINCT player_id, player_name, count(*) as num #5 通过SELECT提取我们指定的字段
FROM player JOIN team ON player.team_id = team.team_id #1 先运行player JOIN team，然后通过ON进行筛选"player.team_id = team.team_id"
WHERE height > 1.80          #2 通过WHERE去判断一下，哪一个更符合我们的条件
GROUP BY player.team_id      #3 进行分组
HAVING num > 2               #4 对分组产生的分组表进行过滤
ORDER BY num DESC            #6 把提取字段进行相应的排序
LIMIT 2                      #7 限制排序后的数据显示行数
```

## 4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

Table1

id name

1 table1_table2

2 table1

Table2

id name

1 table1_table2

3 table2

```
mysql> select Table1.tid, Table1.tname, Table2.tid, Table2.tname from Table1 INNER JOIN Table2 on Table1.tname = Table2.tname;
+-----+---------------+-----+---------------+
| tid | tname         | tid | tname         |
+-----+---------------+-----+---------------+
|   1 | table1_table2 |   1 | table1_table2 |
+-----+---------------+-----+---------------+
1 row in set (0.00 sec)

mysql> select Table1.tid, Table1.tname, Table2.tid, Table2.tname from Table1 INNER JOIN Table2 on Table1.tid = Table2.tid;
+-----+---------------+-----+---------------+
| tid | tname         | tid | tname         |
+-----+---------------+-----+---------------+
|   1 | table1_table2 |   1 | table1_table2 |
+-----+---------------+-----+---------------+
1 row in set (0.00 sec)

mysql> select Table1.tid, Table1.tname, Table2.tid, Table2.tname from Table1 LEFT JOIN Table2 on Table1.tid = Table2.tid;
+-----+---------------+------+---------------+
| tid | tname         | tid  | tname         |
+-----+---------------+------+---------------+
|   2 | table1        | NULL | NULL          |
|   1 | table1_table2 |    1 | table1_table2 |
+-----+---------------+------+---------------+
2 rows in set (0.00 sec)

mysql> select Table1.tid, Table1.tname, Table2.tid, Table2.tname from Table1 RIGHT JOIN Table2 on Table1.tid = Table2.tid;
+------+---------------+-----+---------------+
| tid  | tname         | tid | tname         |
+------+---------------+-----+---------------+
|    1 | table1_table2 |   1 | table1_table2 |
| NULL | NULL          |   3 | table2        |
+------+---------------+-----+---------------+
2 rows in set (0.00 sec)
```

## 5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。
   
   查资料中，后补
## 6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：借鉴，后补

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mysql_host = "192.168.136.128"
mysql_port = 3306
mysql_user = "testuser"
mysql_password = "fT866jN^"
mysql_db = "testdb"
db_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}?charset=utf8mb4"
user_table = "user"
asset_table = "asset"
audit_table = "audit"

Base = declarative_base()


class UserTable(Base):
    __tablename__ = user_table
    user_id = Column(Integer(), primary_key=True, nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    create_time = Column(DateTime(), default=datetime.now)


class AssetTable(Base):
    __tablename__ = asset_table
    user_id = Column(Integer(), primary_key=True, nullable=False)
    total_asset = Column(Integer, nullable=False)
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AuditTable(Base):
    __tablename__ = audit_table
    trade_id = Column(Integer(), autoincrement=True, primary_key=True, nullable=False)
    trade_time = Column(DateTime(), nullable=False)
    from_user_id = Column(Integer(), nullable=False)
    to_user_id = Column(Integer(), nullable=False)
    trade_asset = Column(Integer, nullable=False)


def init_trade_info(orm_session_maker):

    user_1 = UserTable(
        user_id=1,
        user_name="张三"
    )
    user_2 = UserTable(
        user_id=2,
        user_name="李四"
    )

    user_1_asset = AssetTable(
        user_id=1,
        total_asset=50
    )

    user_2_asset = AssetTable(
        user_id=2,
        total_asset=20
    )

    sqlalchemy_session = orm_session_maker()
    try:
        sqlalchemy_session.add(user_1)
        sqlalchemy_session.add(user_2)
        sqlalchemy_session.add(user_1_asset)
        sqlalchemy_session.add(user_2_asset)
        sqlalchemy_session.flush()
        sqlalchemy_session.commit()
    except Exception as e:
        logger.error(e)
    finally:
        sqlalchemy_session.close()


def transfer_account(orm_session_maker):
    sqlalchemy_session = orm_session_maker(autocommit=False)
    from_user_name = "张三"
    to_user_name = "李四"
    trade_value = 100
    try:

        from_user_id = sqlalchemy_session.query(UserTable.user_id).filter(
            UserTable.user_name == from_user_name,
        ).one()[0]

        to_user_id = sqlalchemy_session.query(UserTable.user_id).filter(
            UserTable.user_name == to_user_name,
        ).one()[0]

        from_user_asset_entity = sqlalchemy_session.query(AssetTable).filter(
            AssetTable.user_id == from_user_id,
        ).one()

        to_user_asset_entity = sqlalchemy_session.query(AssetTable).filter(
            AssetTable.user_id == to_user_id,
        ).one()

        if from_user_asset_entity.total_asset >= trade_value:
            from_user_asset_entity.total_asset -= trade_value
            to_user_asset_entity.total_asset += trade_value
            audit_record = AuditTable(
                trade_time=datetime.now(),
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                trade_asset=trade_value
            )
            sqlalchemy_session.add(audit_record)
        else:
            logger.error(f"{from_user_name} 账户余额不足, 转账失败")

        sqlalchemy_session.flush()
        sqlalchemy_session.commit()

    except Exception as e:
        logger.error(e)
        sqlalchemy_session.rollback()
    finally:
        sqlalchemy_session.close()


def main():
    sqlalchemy_engine = create_engine(db_url, echo=True, encoding="utf-8")
    # 创建表
    Base.metadata.create_all(sqlalchemy_engine)
    orm_session_maker = sessionmaker(bind=sqlalchemy_engine)
    # 插入基础数据
    init_trade_info(orm_session_maker)
    # 交易
    transfer_account(orm_session_maker)


if __name__ == "__main__":
    main()
```

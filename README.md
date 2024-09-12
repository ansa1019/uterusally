目錄
======


## 1. [安裝](#1-安裝-1)

### 1.1. [安裝套件](#11-安裝套件-1)

```shell
# python requirements
\uterusally\Api>pip install -r requirements.txt
```

### 1.2. [安裝資料庫](#12-安裝資料庫-1)

```shell
# 更改設定在
\uterusally\Api\cnf\my.cnf
```

```shell
# mysql
# 正常來說使用進入到\uterusally\Api下使用python manage.py makemigrations 再使用python manage.py migrate就行
\uterusally\Api>python manage.py makemigrations
\uterusally\Api>python manage.py migrate
```

```mysql
# 檢查字元集
# 如果不同的話就修改，不然插入中文會出現錯誤
mysql> show variables like 'char%';
+--------------------------+----------------------------------------+
| Variable_name            | Value                                  |
+--------------------------+----------------------------------------+
| character_set_client     | utf8mb4                                |
| character_set_connection | utf8mb4                                |
| character_set_database   | utf8mb4                                |
| character_set_filesystem | binary                                 |
| character_set_results    | utf8mb4                                |
| character_set_server     | utf8mb4                                |
| character_set_system     | utf8                                   |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 8.0|
+--------------------------+----------------------------------------+
mysql> use database_name;
mysql> show tables; # 檢查資料表
+--------------------------------------+
| Tables_in_testcoll                   |
+--------------------------------------+
| auth_group                           |
| auth_group_permissions               |
| auth_permission                      |
| auth_user                            |
| auth_user_groups                     |
| auth_user_user_permissions           |
....
36 rows in set (0.001 sec)
mysql> SHOW FULL COLUMNS FROM table_name;
+--------------+--------------+--------------------+------+-----+---------+----------------+---------------------------------+---------+
| Field        | Type         | Collation          | Null | Key | Default | Extra          | Privileges                      | Comment |
+--------------+--------------+--------------------+------+-----+---------+----------------+---------------------------------+---------+
| id           | int(11)      | NULL               | NO   | PRI | NULL    | auto_increment | select,insert,update,references |         |
| password     | varchar(128) | utf8mb4_unicode_ci | NO   |     | NULL    |                | select,insert,update,references |         |
| last_login   | datetime(6)  | NULL               | YES  |     | NULL    |                | select,insert,update,references |         |
| is_superuser | tinyint(1)   | NULL               | NO   |     | NULL    |                | select,insert,update,references |         |
| username     | varchar(150) | utf8mb4_unicode_ci | NO   | UNI | NULL    |                | select,insert,update,references |         |
| first_name   | varchar(150) | utf8mb4_unicode_ci | NO   |     | NULL    |                | select,insert,update,references |         |
....
11 rows in set (0.009 sec)
```
---------------------------------------
# **Old version**
# **出問題就把整個資料庫的table改成utf8mb4**
```shell
# 如果改了還是出錯就直接import sql
\uterusally\Api>mysql -u root -p database_name < database_name.sql
```
---------------------------------------

<br>

2. [使用](#2-使用-2)

```shell
# mysql
# 正常來說使用進入到\uterusally\Api下使用python manage.py makemigrations 再使用python manage.py migrate就行
\uterusally\Api>python manage.py makemigrations
\uterusally\Api>python manage.py migrate
# launch server
\uterusally\Api>daphne -b 0.0.0.0 -p 8001 Api.asgi:application # daphne server for asgi application
\uterusally\Api>python manage.py runserver # 基本上run這個就能跑 上面是要使用到asgi application ex:chat server的時候才需要
```


只有auth有重寫成使用jwt token來登入，其他都可以從django rest framework的網頁介面來操作
或者用postman也行

endpoint | method | description
--- |--------| ---
/api/auth/ | GET    | API Auth root
/api/auth/register/ | POST   | 新增使用者
/api/auth/token/ | POST   | 登入Token
/api/auth/token/refresh/ | GET    | 取得所有使用者
/api/auth/users/{id}/ | GET    | 取得特定使用者
/api/auth/users/{id}/ | PATHCH | 更新特定使用者
/api/content/ | GET    | API Content realte root
/api/point/ | GET    | API Point realte root
/api/task/ | GET    | API Task realte root
/api/userdetail/ | GET    | API UserDetail realte root #用來存放{已按讚/已收藏}等相關判定
/api/userprofile/ | GET    | API UserProfile realte root
/api/product/ | GET    | API Product realte root
3. [補充](#3-參考-3)




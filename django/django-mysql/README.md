# dockerfiles

reference: 
- https://ithelp.ithome.com.tw/users/20141666/ironman/4696?page=1


```bash
# 使用當前目錄的 Dockerfile 建立容器
docker build -t django-mysqlclient:1.0.0 . -f Dockerfile --no-cache
```

## 啟動容器 under backgroud
```bash
docker run -dit \
--name django-mysql-client-test \
-v '/share/django:/root' \
-p 8080:8080 \
django-mysqlclient:1.0.0 

## serach mariadb images
docker search mariadb

## pull images
docker pull mariadb:10.4

## create data folder for backup sql data
if [ ! -d "/share/data/mariadb" ]; then mkdir -p /share/data/mariadb ;fi

## start mariadb
docker run -dit \
--name mariadbtest \
-e MYSQL_ROOT_PASSWORD=admin \
-p 3306:3306 \
-v '/share/data/mariadb:/var/lib/mysql' \
docker.io/library/mariadb:10.4

## start phpmyadmin
docker run -dit --name phpmyadmin -e PMA_HOST=192.168.137.99 -p 8088:80 phpmyadmin:5

```


## 進入容器後啟動django project
```bash

## 啟動django project
django-admin startproject keyboardmarket

## start web
python3.10 manage.py runserver 0.0.0.0:8080


python3 manage.py startapp product
python3 manage.py startapp userorder
python3 manage.py startapp usercart
python3 manage.py startapp users
 

### 若有調整各 app 的 models.py，需執行以下指令
## update models
python3 manage.py makemigrations
python3 manage.py migrate


## create superuser
python3 manage.py createsuperuser

## create admin user
python3 manage.py createsuperuser --username admin --email

## create admin user
python3 manage.py createsuperuser --username admin --email

```

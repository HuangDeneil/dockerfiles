# dockerfiles

reference: https://ithelp.ithome.com.tw/m/articles/10292250

```bash

# 使用當前目錄的 Dockerfile 建立容器
docker build -t django-env . -f Dockerfile --no-cache
```

## 建立 docker-entrypoint.sh (關於container 啟動後是否要自動執行 python manage.py，需順便調整dockerfile)
```bash
touch docker-entrypoint.sh
chmod 755 docker-entrypoint.sh
```

```bash
#docker-entrypoint.sh
#!/bin/bash
cd /root/app/web/

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000
exec "$@"
```


## 啟動容器 under backgroud
```bash
docker run -dit \
--name django-env \
-p 8000:8000 \
-v '/share/django:/opt/app' \
django-env 
```


## 進入容器後啟動django project
```bash

## 啟動django project
django-admin startproject main
mv main web

## update sql-lite
python3.10 manage.py migrate

## start web
python3.10 manage.py runserver 0.0.0.0:8000

```

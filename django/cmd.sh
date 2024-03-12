
# touch docker-entrypoint.sh
# chmod 755 docker-entrypoint.sh

# touch docker-compose.yml


# 使用當前目錄的 Dockerfile 建立容器
docker build -t django-env . 


docker run -dit --privileged  \
--name django-env \
-p 8000:8000 \
-v '/share/django:/opt/app' \
django-env 




docker compose up -d # 背景執行


touch .env

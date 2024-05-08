
DB_ROOT_PASSWORD=admin
DB_NAME=wordpress


## start mariadb
docker run -dit \
--name db \
-e MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD} \
-e MYSQL_DATABASE="${DB_NAME}" \
-p 3306:3306 \
-v 'db_data:/var/lib/mysql' \
mariadb:10.4

## start phpmyadmin
docker run -dit \
--name phpmyadmin \
-v "$(pwd)/config/pma_php.ini:/usr/local/etc/php/conf.d/conf.ini" \
-v "$(pwd)/config/pma_config.php:/etc/phpmyadmin/config.user.inc.php" \
-e PMA_HOST=192.168.0.47 \
-p 8080:80 \
phpmyadmin:5


docker run -dit \
--name wordpress \
-p 80:80 \
-v "$(pwd)/wp-app:/var/www/html" \
-v "$(pwd)/config/wp_php.ini:/usr/local/etc/php/conf.d/conf.ini" \
-e WORDPRESS_DB_HOST=192.168.0.47 \
-e WORDPRESS_DB_USER=root \
-e WORDPRESS_DB_PASSWORD="${DB_ROOT_PASSWORD}" \
-e WORDPRESS_DB_NAME="${DB_NAME}" \
wordpress:latest



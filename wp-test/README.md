
[Notion]
(https://easy-broker-f36.notion.site/wordpress-b24d6ea6c51640228262d84de29e630d?pvs=4#c175955eedbf464683ec69cf3a4e9d84)


## Basic require setting
```bash
cp env-example .env
```

## Edit .env
### ** Most Required File
```bash
## VM ip (check with ip addr )
LAN_IP=192.168.137.199

## wordpress http port
WP_PORT=80

## phpmyadmin http port
PHPMyAdmin_PORT=8080

## Wordpress DB root passwd & database name
DB_ROOT_PASSWORD=password
DB_NAME=wordpress

```



## Start/Down wordpress 
```bash
docker composr up -d

docker compose down
```


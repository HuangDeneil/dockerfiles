








docker run -dit \
-p 8080:80 \
--restart unless-stopped \
--name nginx \
nginx:1.27.0-alpine 








services: 
    server:
        build:
            context: .
            dockerfile: nginx.Dockerfile
        restart: always
        command: [nginx-debug, '-g', 'daemon off;']
        volumes:
            - "./mirror:/downloads:ro"
        ports:
            - "8080:80"



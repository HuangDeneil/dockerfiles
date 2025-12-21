FROM n8nio/n8n:1.123.1
# FROM n8nio/n8n:1.119.2
USER root
# 安裝擴充套件
RUN npm install -g \
    cheerio 
# USER node
# 
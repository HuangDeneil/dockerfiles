FROM n8nio/n8n:1.112.6
USER root
# 安裝擴充套件
RUN npm install -g \
    cheerio 
# USER node
# 
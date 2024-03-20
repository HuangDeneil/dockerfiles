


path=$1

if [ -z $path ]; then
    echo "Please provide a path"
    exit 1
fi
mkdir -p $path
mkdir -p $path/backend
mkdir -p $path/frontend


cd $path/frontend
npm install -g vue
npm install -g @vue/cli

## 創建專案
vue create keyboardmarket
# 選擇Default([Vue 2] babel,eslint)

## 安裝router
npm install --save vue-router


## 啟動專案
# cd keyboardmarket
# npm run serve


cd $path/frontend
django-admin startproject keyboardmarket




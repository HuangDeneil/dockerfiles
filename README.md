# dockerfiles

## Documentation

- [diskimage-builder vs Oz Comparison](docs/diskimage-builder-vs-oz.md) - 比較 OpenStack diskimage-builder 與 Oz 的差異

## centos9 dokcer installation

```bash
## remove docker
dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine -y


sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

## install docker
dnf install -y yum-utils device-mapper-persistent-data lvm2
yum install -y gcc gcc-c++

## install repo
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

dnf install -y docker-ce docker-ce-cli containerd.io

systemctl start docker
systemctl enable docker

docker version
```

## docker-compose

- tag list : https://github.com/docker/compose/releases/tag

```bash
## download from github
wget https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -O /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


## remove (installl with github)
sudo rm /usr/local/bin/docker-compose && sudo rm /usr/bin/docker-compose
## remove (install with rpm)
sudo apt-get -y remove docker-compose && sudo apt-get -y autoremove
```

## Build docker image testing
```bash
docker run -dit --name ubuntu22-build-test -v '/share/django:/root' -p 8080:8080 ubuntu:22.04
```

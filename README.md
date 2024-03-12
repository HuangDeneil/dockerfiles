# dockerfiles


## centos9 dokcer installation

```bash
## remove docker
dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine -y


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


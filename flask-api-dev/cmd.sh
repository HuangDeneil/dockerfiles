
## Build the image
docker build -t api-dev-env . -f dockerfile.txt --no-cache

## Run the container
# -v: Mount the NFS share to the container
docker run -dit \
-v '/share/data-NFS-300:/root/data-NFS-300:ro' \
-p 10022:22 \
--name api-dev-env api-dev-env


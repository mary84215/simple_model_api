# Demoostrate hwo to run a simpel ML API in a docker container

# How to run container
- Clone codes
- open your CLI and cd to the directory where Dockerfile locates
- build image: `docker image build -t <desired_image_name>`
- run container: `docker run -d -p 5000:5000 <image_id>`
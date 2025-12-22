docker stop hockey-api
docker rm hockey-api

docker build -t hockey-api . --no-cache
docker run -it --rm --name hockey-api -p 5600:8080 hockey-api


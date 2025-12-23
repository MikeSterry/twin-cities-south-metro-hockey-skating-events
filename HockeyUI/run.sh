docker stop hockey-ui
docker rm hockey-ui

docker build -t hockey-ui .
docker run -it --rm --name hockey-ui -p 3600:8080 \
  -e REACT_APP_API_URL=http://localhost:5600/api/public_skate_events \
  hockey-ui

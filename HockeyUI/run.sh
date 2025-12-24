API_URL=$1
echo "Using API URL: ${API_URL:=localhost}"

docker stop hockey-ui
docker rm hockey-ui

docker build -t hockey-ui . --no-cache
docker run -it --rm --name hockey-ui -p 3600:8080 \
  -e REACT_APP_API_URL=http://${API_URL:=localhost}:5600/api/public_skate_events \
  hockey-ui

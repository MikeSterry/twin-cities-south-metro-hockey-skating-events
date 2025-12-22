docker stop hockey-ui
docker rm hockey-ui

docker build -t hockey-ui .
docker run -it --rm --name hockey-ui -p 3600:80 \
  -e REACT_APP_API_URL=http://localhost:5600/api/public_skate_events \
  hockey-ui

#  -e REACT_APP_API_URL=https://hockey-api.mikesterry.com/api/public_skate_events \

#docker build --target build -t hockey-ui . --no-cache
#docker run -it --rm --name hockey-ui -p 3000:3000 \
#  -e REACT_APP_API_URL=http://192.168.1.155:5600/api/public_skate_events \
#  hockey-ui /bin/sh

FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
#RUN npm run build && \
#    npm install -g serve
#CMD ["serve", "-s", "build", "-l", "3000"]

FROM nginx:stable-alpine AS runtime
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
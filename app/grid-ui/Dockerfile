# Build step #1: build the React front end
FROM node:16-alpine
WORKDIR /app

RUN mkdir ./grid-ui
COPY . ./grid-ui
WORKDIR /app/grid-ui
RUN npm install

# # Build step #2: start nginx server at port 80 with the React build copied into html
# FROM nginx:alpine
# COPY --from=build-step /app/build /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/nginx.conf

CMD npm start
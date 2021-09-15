# Build step #1: build the React front end
FROM node:16-alpine AS builder

WORKDIR /app

RUN mkdir ./grid-ui
WORKDIR /app/grid-ui
COPY . .
RUN npm install
RUN npm run build

# Bundle static assets with nginx
FROM nginx:1.21.0-alpine
# Copy built assets from builder
COPY --from=builder /app/grid-ui/build /usr/share/nginx/html
# Add your nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose port
EXPOSE 80
# Start nginx
CMD ["nginx", "-g", "daemon off;"]

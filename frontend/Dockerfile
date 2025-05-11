# Stage 1: Build Angular app
FROM node:18 as build

WORKDIR /app
COPY . .
RUN npm install && npm run build

# Stage 2: Serve app with Nginx
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy built Angular app from previous stage
COPY --from=build /app/dist/power-fi/browser /usr/share/nginx/html

# Optional: Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

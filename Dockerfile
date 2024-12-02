# Use Nginx to serve the Angular app
FROM nginx:alpine

# Copy Angular build output to Nginx's HTML directory
COPY ./dist/cloud-chat-app /usr/share/nginx/html

# Expose port 80 for serving the app
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
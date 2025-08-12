# Use a Node.js image to build the React application
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Use a lightweight Nginx image to serve the built application
FROM nginx:alpine

# Copy the built application from the 'build' stage to the Nginx web root
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a custom nginx configuration file (created in the next step)
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
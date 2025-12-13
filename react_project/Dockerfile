# Use the official Node.js 14 image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for npm install
COPY package*.json ./

# Install npm dependencies in the container
RUN npm install

# Copy the rest of your React app source code into the container
COPY . .

# Expose the port that React runs on (default 3000)
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]

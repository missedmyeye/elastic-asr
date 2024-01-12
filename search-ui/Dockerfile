FROM node:18-alpine

WORKDIR /usr/src/app

# Install curl
RUN apk add --no-cache curl

# Install yarn
# RUN npm install --global yarn

# Download and extract the repository
RUN curl -L https://codeload.github.com/elastic/app-search-reference-ui-react/tar.gz/master | tar -xz

# Navigate into the extracted directory
WORKDIR /usr/src/app/app-search-reference-ui-react-master

# Copy the updated package files to prevent version conflict
COPY package.json ./package.json
COPY package-lock.json ./package-lock.json

# Copy engine.json file
COPY engine.json ./src/config

# Install yarn dependencies
RUN yarn install

# Add the required package
RUN yarn add @elastic/search-ui-elasticsearch-connector

# Copy the updated application file
COPY App.js ./src/App.js

EXPOSE 3000

CMD ["yarn","start"]
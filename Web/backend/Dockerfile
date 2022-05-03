FROM node:13.12.0-alpine 

COPY . /

RUN npm cache clean --force && npm install --silent

EXPOSE 3000


CMD ["npm","run","start"]


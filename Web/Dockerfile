FROM node:18.0.0-alpine 

ENV PATH ./node_modules/.bin:$PATH

COPY . /

RUN npm install

EXPOSE 3000

CMD ["node","app.js"]


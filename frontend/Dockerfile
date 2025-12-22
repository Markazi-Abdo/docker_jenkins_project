FROM node:20

WORKDIR /app

COPY  . .

RUN yarn
RUN yarn global add serve

CMD [ "yarn", "start" ]

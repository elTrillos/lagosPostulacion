FROM node:24.11.0

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/. .

EXPOSE 4200
CMD ["npm", "run", "start"]

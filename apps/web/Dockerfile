FROM node:20-alpine

WORKDIR /app

# Instala dependências antes de copiar o código (cache de layers)
COPY package*.json ./
RUN npm install

# Copia o restante do código
COPY . .

EXPOSE 5173

# Comando padrão (sobrescrito pelo docker-compose para --host)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

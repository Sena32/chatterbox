// infra/mongo-init/01-init.js
// Este script é executado automaticamente pelo container do MongoDB
// na primeira inicialização (quando o volume ainda não existe).
// Referência: variável MONGO_INITDB_DATABASE no docker-compose.yml

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE || "chatterbox")

// Cria índices que serão necessários quando a aplicação for implementada.
// Adicionar novos índices aqui conforme as specs forem implementadas.

// Spec 001: índice de ordenação de mensagens por data de criação da conversa
db.createCollection("conversations")
db.conversations.createIndex({ created_at: -1 })

print("✅ ChatterBox DB inicializado: coleção 'conversations' e índices criados.")

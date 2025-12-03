# 📋 Descrição

Este projeto implementa uma arquitetura de **microserviços** utilizando Docker e Flask.  
A solução é composta por três serviços principais e um cliente de testes:

- **Usuários Service (usuarios-service):** Microserviço responsável pelo CRUD de usuários e estatísticas de perfis.
- **Pedidos Service (pedidos-service):** Microserviço responsável pelo CRUD de pedidos e estatísticas de status e valores.
- **API Gateway (api-gateway):** Camada central que expõe endpoints unificados, roteando requisições para os microserviços de usuários e pedidos.
- **Cliente (client-gateway-test):** Script automatizado que executa testes de integração contra o API Gateway, validando endpoints e fluxos.

Todos os serviços se comunicam através da rede Docker `gateway-network`.

---

# 🔄 Funcionamento

- **Inicialização:**
    - A rede `gateway-network` é criada pelo Docker Compose.
    - O serviço `usuarios-service` sobe primeiro e expõe endpoints em `localhost:5001`.
    - O serviço `pedidos-service` sobe em paralelo e expõe endpoints em `localhost:5002`.
    - O serviço `api-gateway` sobe em seguida, conectando-se aos dois microserviços e expondo endpoints unificados em `localhost:5000`.
    - O serviço `client-gateway-test` sobe por último e executa o script `test_gateway.sh`, realizando chamadas periódicas ao Gateway.

- **Fluxo de comunicação:**
    - O **API Gateway** recebe requisições externas e delega para os microserviços internos.
    - Endpoints compostos como `/dashboard` e `/users-with-orders` agregam dados de múltiplos serviços.
    - O cliente de testes valida operações como criação, atualização, filtros e estatísticas de usuários e pedidos.

- **Endpoints principais:**
    - **Gateway:** `/health`, `/users`, `/orders`, `/dashboard`, `/users-with-orders`
    - **Usuários Service:** `/api/users`, `/api/users/<id>`, `/api/users/statistics/summary`
    - **Pedidos Service:** `/api/orders`, `/api/orders/<id>`, `/api/orders/user/<id>`, `/api/orders/statistics/summary`

---

# 🚀 Instruções passo a passo

## 1. Pré‑requisitos

- Docker 20.10+
- Docker Compose integrado (comando `docker compose`)
- Linux/macOS ou Windows com WSL2

Verifique a instalação:
```bash
docker --version
docker compose version
```

## 2. Estrutura dos arquivos (referência)
- docker-compose.yml
- Dockerfile.users
- Dockerfile.pedidos
- Dockerfile.gateway
- Dockerfile.client
- users/app.py
- pedidos/app.py
- gateway/app.py
- client/test_gateway.sh

## 3. Build das imagens
```bash
docker compose build
```

Resultado esperado:

- usuarios-service (Flask Users)
- pedidos-service (Flask Orders)
- api-gateway (Flask Gateway)
- client-gateway-test (script de testes)

## 4. Subir os serviços
Modo foreground (logs no terminal):
```bash
docker compose up
```

Modo background:
```bash
docker compose up -d
```

## 5. Acompanhar logs
```bash
docker compose logs -f
```

## 6. Testes manuais
Enquanto os containers estão rodando:
```bash
# Health check do Gateway
curl http://localhost:5000/health

# Listar usuários via Gateway
curl http://localhost:5000/users

# Criar novo usuário
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" \
    -d '{"name":"Victor","email":"victor@email.com","profile":"client"}'

# Listar pedidos via Gateway
curl http://localhost:5000/orders

# Criar novo pedido
curl -X POST http://localhost:5000/orders -H "Content-Type: application/json" \
    -d '{"user_id":1,"items":[{"product":"Notebook","quantity":1,"price":3500.00}]}'

# Dashboard consolidado
curl http://localhost:5000/dashboard
```

## 7. Verificar execução e rede
Listar containers:
```bash
docker ps
```

Inspecionar rede:
```bash
docker network inspect gateway-network
```

Testar conectividade entre containers:
```bash
docker exec client-gateway-test ping -c 2 api-gateway
```

## 8. Encerrar e limpar
Parar e remover serviços:
```bash
docker compose down
```

Remover também volumes e network:
```bash
docker compose down -v
```

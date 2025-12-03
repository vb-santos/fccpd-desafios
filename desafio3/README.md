# 📋 Descrição

Este projeto demonstra a comunicação entre três containers Docker em uma rede bridge customizada.  
O container `db` executa um banco de dados PostgreSQL inicializado com a tabela `posts`.  
O container `web` executa uma aplicação Flask que expõe endpoints REST para manipulação e consulta de posts, além de integração com Redis para cache e contadores.  
O container `client` realiza requisições periódicas à aplicação, exibindo status, posts e estatísticas.

- **Banco de Dados (db):** PostgreSQL inicializado com `init.sql`, contendo a tabela `posts` e dados de exemplo.
- **Aplicação (web):** Python 3.11 + Flask + psycopg2 + redis, expõe endpoints:
  - `GET /health` → health check
  - `GET /status` → status da aplicação e conexões
  - `GET /api/posts` → lista posts
  - `POST /api/posts` → cria post
  - `GET /api/posts/cache` → lista posts com cache Redis
  - `GET /api/counter` → contador de requisições (Redis)
  - `GET /api/stats` → estatísticas gerais
- **Cliente (client):** Base `curlimages/curl:8.4.0`, script shell automatiza requisições periódicas (a cada 15s).
- **Cache (cache):** Redis 7-alpine para cache de posts e contadores.

---

# 🔄 Funcionamento

- **Inicialização:**
  - A rede Docker é criada pelo Compose.
  - O serviço `db` sobe primeiro, inicializando a tabela `posts` com dados via `init.sql`.
  - O serviço `cache` sobe em paralelo, fornecendo Redis para cache e contadores.
  - O serviço `web` sobe em seguida, conectando-se ao banco e ao Redis.
  - O serviço `client` sobe por último e aguarda 15 segundos antes de iniciar o loop.

- **Ciclo do cliente:**
  - Faz `GET /health` para verificar saúde da aplicação.
  - Faz `GET /status` para verificar conexões com DB e Redis.
  - Faz `GET /api/posts` para listar posts do banco.
  - Faz `GET /api/posts/cache` para listar posts com cache.
  - Faz `GET /api/counter` para incrementar e exibir contador de requisições.
  - Faz `GET /api/stats` para estatísticas gerais.
  - Exibe resultados formatados e repete a cada 15 segundos.

- **Acesso externo:**
  - Os endpoints da aplicação podem ser testados via `localhost:5000` na máquina host.

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
- Dockerfile.web
- Dockerfile.client
- Dockerfile.cache
- web/app.py
- web/requirements.txt
- db/init.sql
- client/test_comunicacao.sh

## 3. Build das imagens
```bash
docker compose build
```

Resultado esperado:

- db (PostgreSQL com init.sql)
- web (Python + Flask + psycopg2 + redis)
- client (curl + script)
- cache (Redis)

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
# Health check
curl http://localhost:5000/health

# Status
curl http://localhost:5000/status

# Listar posts
curl http://localhost:5000/api/posts

# Criar novo post
curl -X POST http://localhost:5000/api/posts -H "Content-Type: application/json" \
    -d '{"titulo":"Novo Post","conteudo":"Conteúdo de teste","autor":"Victor"}'

# Posts com cache
curl http://localhost:5000/api/posts/cache

# Contador de requisições
curl http://localhost:5000/api/counter

# Estatísticas gerais
curl http://localhost:5000/api/stats
```

## 7. Verificar execução e rede
Listar containers:
```bash
docker ps
```

Inspecionar rede:
```bash
docker network inspect rede-persistencia
```

Testar conectividade entre containers:
```bash
docker exec client ping -c 2 web
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

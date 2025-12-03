# 📋 Descrição

Este projeto demonstra a comunicação entre três containers Docker em uma rede bridge customizada com persistência de dados.  
O container `db-postgres` executa um banco de dados PostgreSQL inicializado com tabelas e dados básicos.  
O container `app-flask` executa uma aplicação Flask que expõe endpoints REST para manipulação e consulta de usuários e logs.  
O container `leitor-dados` realiza requisições periódicas à aplicação, exibindo status, usuários e logs.

- **Banco de Dados (db-postgres):** PostgreSQL inicializado com `init.sql`, contendo tabelas `users` e `logs`.
- **Aplicação (app-flask):** Python 3.11 + Flask + psycopg2, expõe endpoints:
    - `GET /users` → lista usuários
    - `POST /users` → cria usuário
    - `GET /logs` → lista logs
    - `GET /status` → status da aplicação e conexão com banco
- **Leitor (leitor-dados):** Base `curlimages/curl:8.4.0`, script shell automatiza requisições periódicas (a cada 15s).
- **Rede:** `rede-persistencia` (driver bridge) para comunicação entre containers.

---

# 🔄 Funcionamento

- **Inicialização:**
    - A rede Docker `rede-persistencia` é criada pelo Compose.
    - O serviço `db-postgres` sobe primeiro, inicializando tabelas e dados via `init.sql`.
    - O serviço `app-flask` sobe em seguida, aguardando o banco estar saudável antes de iniciar.
    - O serviço `leitor-dados` sobe por último e aguarda 10 segundos antes de iniciar o loop.

- **Ciclo do leitor:**
    - Faz `GET http://app:5000/status` para verificar status da aplicação e banco.
    - Faz `GET http://app:5000/users` para listar usuários cadastrados.
    - Faz `GET http://app:5000/logs` para listar logs da aplicação.
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
- Dockerfile.app
- Dockerfile.reader
- Dockerfile.db
- app/app.py
- app/requirements.txt
- db/init.sql
- reader/script.sh

## 3. Build das imagens
```bash
docker compose build
```

Resultado esperado:

- db-postgres (PostgreSQL com init.sql)
- app-flask (Python + Flask + psycopg2)
- leitor-dados (curl + script)

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
# Listar usuários
curl http://localhost:5000/users

# Criar novo usuário
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" \
    -d '{"nome":"Maria","email":"maria@gmail.com"}'

# Listar logs
curl http://localhost:5000/logs

# Verificar status
curl http://localhost:5000/status
```

## 7. Verificar execução e rede
Listar containers:
```bash
docker ps
```

Inspecionar rede:
```bash
docker network inspect desafio_rede-persistencia
```

Testar conectividade entre containers:
```bash
docker exec leitor-dados ping -c 2 app
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

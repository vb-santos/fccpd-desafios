# Descrição

Este projeto demonstra a comunicação entre dois containers Docker em uma rede bridge customizada. O container `servidor-web` executa um servidor Flask na porta 8080 com dois endpoints (`/` e `/status`). O container `cliente-requisicoes` realiza requisições HTTP periódicas (a cada 10 segundos) ao servidor, registrando sucesso/falha e formatando a saída do endpoint de status.

- **Servidor (servidor-web):** Python 3.11 + Flask, expõe `GET /` com timestamp e `GET /status` com JSON de status.
- **Cliente (cliente-requisicoes):** Base `curlimages/curl:8.4.0`, script shell automatiza requisições, aguarda 5s antes de iniciar.
- **Rede:** `rede-comunicacao` (driver bridge) para comunicação via hostname entre os containers.

---

# Funcionamento

- **Inicialização:**
   - A rede Docker `rede-comunicacao` é criada pelo Compose.
   - O serviço `servidor-web` sobe primeiro e escuta em `0.0.0.0:8080`.
   - O serviço `cliente-requisicoes` sobe em seguida e aguarda 5 segundos antes de iniciar o loop.

- **Ciclo do cliente:**
   - Faz `GET http://servidor-web:8080/` e `GET http://servidor-web:8080/status`.
   - Exibe status HTTP, corpo das respostas e estatísticas acumuladas de sucesso/falha (contabilizadas pelo endpoint `/`).
   - Aguarda 10 segundos e repete indefinidamente.

- **Acesso externo:**
   - Os endpoints do servidor também podem ser testados via `localhost:8080` na máquina host.

---

# Instruções passo a passo

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
- Dockerfile.server 
- Dockerfile.client 
- server/app.py 
- client/script.sh 
- requirements.txt

## 3. Build das imagens
```bash
docker compose build
```

Resultado esperado:

- servidor-web (Python 3.11 + Flask)
- cliente-requisicoes (curl + script)

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
# Endpoint raiz (host)
curl http://localhost:8080/

# Endpoint de status (host)
curl http://localhost:8080/status

# Endpoint de status via cliente (dentro da rede)
docker exec cliente-requisicoes curl http://servidor-web:8080/status
```

## 7. Verificar execução e rede
Listar containers:
```bash
docker ps
```

Inspecionar rede:
```bash
docker network inspect desafio1_rede-comunicacao
```

Testar conectividade entre containers:
```bash
docker exec cliente-requisicoes ping -c 2 servidor-web
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

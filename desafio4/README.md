# 📋 Descrição

Este projeto demonstra uma arquitetura simples de **microserviços** com dois serviços independentes e um cliente de testes:

- **Serviço A (serva-usuarios):** Responsável pelo gerenciamento de usuários, oferecendo CRUD básico e estatísticas.
- **Serviço B (servb-analise):** Consome os dados do Serviço A, formata informações, gera relatórios e fornece endpoints de análise e status de comunicação.
- **Cliente (client-teste-microsservicos):** Script automatizado que executa testes periódicos, validando a comunicação entre os serviços e exibindo relatórios.

Todos os serviços se comunicam através da rede Docker `rede-microsservicos`.

---

# 🔄 Funcionamento

- **Inicialização:**
  - A rede `rede-microsservicos` é criada pelo Docker Compose.
  - O **Serviço A** sobe primeiro e expõe endpoints em `localhost:5001`.
  - O **Serviço B** sobe em seguida, aguardando o Serviço A estar saudável antes de iniciar. Ele consome os dados do Serviço A e expõe endpoints em `localhost:5002`.
  - O **Cliente** sobe por último e executa o script `test_microsservicos.sh`, realizando chamadas periódicas para validar os serviços.

- **Fluxo de comunicação:**
  - O **Serviço A** fornece dados brutos de usuários e estatísticas.
  - O **Serviço B** consome os dados do Serviço A, formata informações, gera relatórios detalhados e expõe endpoints adicionais.
  - O **Cliente** executa testes automáticos, verificando health checks, listagens, relatórios e status de comunicação.

- **Endpoints principais:**
  - **Serviço A:** `/health`, `/api/users`, `/api/users/<id>`, `/api/users/statistics/summary`
  - **Serviço B:** `/health`, `/api/users/formatted`, `/api/users/report`, `/api/users/<id>/details`, `/api/services-status`

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
- Dockerfile.serva
- Dockerfile.servb
- Dockerfile.client
- serva/app.py
- servb/app.py
- client/test_microsservicos.sh

## 3. Build das imagens
```bash
docker compose build
```

Resultado esperado:

- serva-usuarios (Flask Users)
- servb-analise (Flask Analysis)
- client-teste-microsservicos (script de testes)

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
# Health check Serviço A
curl http://localhost:5001/health

# Listar usuários Serviço A
curl http://localhost:5001/api/users

# Health check Serviço B
curl http://localhost:5002/health

# Usuários formatados Serviço B
curl http://localhost:5002/api/users/formatted

# Relatório completo Serviço B
curl http://localhost:5002/api/users/report

# Detalhes de um usuário via Serviço B
curl http://localhost:5002/api/users/1/details

# Status dos serviços
curl http://localhost:5002/api/services-status
```

## 7. Verificar execução e rede
Listar containers:
```bash
docker ps
```

Inspecionar rede:
```bash
docker network inspect rede-microsservicos
```

Testar conectividade entre containers:
```bash
docker exec client-teste-microsservicos ping -c 2 serva
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

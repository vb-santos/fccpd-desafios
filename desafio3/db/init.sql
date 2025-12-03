CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100) DEFAULT 'Anônimo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO posts (title, content, author) VALUES
    ('Introdução ao Docker', 'Docker é uma plataforma que permite empacotar aplicações e suas dependências em containers.', 'Carlos Silva'),
    ('Microservices Architecture', 'A arquitetura de microservices divide uma aplicação em serviços independentes e escaláveis.', 'Ana Oliveira'),
    ('Cache com Redis', 'Redis é um banco de dados em memória usado para cache e sessões de alta performance.', 'Roberto Santos'),
    ('Deploy com Kubernetes', 'Kubernetes orquestra containers Docker em ambientes de produção complexos.', 'Fernanda Costa'),
    ('Monitoramento de Aplicações', 'Ferramentas como Prometheus e Grafana ajudam no monitoramento de aplicações em tempo real.', 'Lucas Pereira'),
    ('CI/CD Pipelines', 'Pipelines de integração e entrega contínua automatizam o processo de desenvolvimento.', 'Mariana Lima'),
    ('Segurança em Containers', 'Boas práticas para garantir a segurança de aplicações em containers Docker.', 'Ricardo Almeida'),
    ('Escalabilidade Horizontal', 'Como escalar aplicações horizontalmente para lidar com aumento de tráfego.', 'Patricia Souza');
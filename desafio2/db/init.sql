CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
    ('Alex Juninho', 'alex.juninho@gmail.com'),
    ('Sarah Cleiton', 'sarah.cleiton@gmail.com'),

INSERT INTO logs (message) VALUES
    ('Banco de dados inicializado com sucesso'),
    ('Tabela de usuarios criada'),
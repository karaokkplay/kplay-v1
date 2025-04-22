# Instruções de Implantação - Aplicativo Web de Karaokê com Acordes Sincronizados

Este documento fornece instruções detalhadas para implantar o Aplicativo Web de Karaokê com Acordes Sincronizados em diferentes ambientes.

## Requisitos do Sistema

### Backend
- Python 3.8 ou superior
- Flask e dependências (instaladas via pip)
- MySQL ou SQLite para banco de dados
- Bibliotecas music21 e pychord para análise musical

### Frontend
- Servidor web para arquivos estáticos (Nginx, Apache, etc.)
- Navegador moderno com suporte a JavaScript ES6
- Suporte a Web Audio API

## Opções de Implantação

Existem várias maneiras de implantar o aplicativo, dependendo das suas necessidades:

1. **Implantação Local**: Para desenvolvimento ou uso pessoal
2. **Implantação em Servidor**: Para uso em pequena escala
3. **Implantação em Nuvem**: Para uso em larga escala

## 1. Implantação Local

### Configuração do Backend

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/karaoke-app.git
cd karaoke-app
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:
   - Para SQLite (padrão para desenvolvimento):
     - Não é necessária configuração adicional
   - Para MySQL:
     - Crie um banco de dados MySQL
     - Configure as credenciais no arquivo `.env`

4. Inicie o servidor backend:
```bash
cd backend
python app.py
```
O servidor estará disponível em `http://localhost:5000`

### Configuração do Frontend

1. Abra um novo terminal e navegue até a pasta do frontend:
```bash
cd karaoke-app/frontend
```

2. Inicie um servidor web simples:
```bash
# Usando Python
python -m http.server 8000
```
O frontend estará disponível em `http://localhost:8000`

## 2. Implantação em Servidor

### Configuração do Backend com Gunicorn e Nginx

1. Instale o Gunicorn:
```bash
pip install gunicorn
```

2. Crie um arquivo de serviço systemd para o backend:
```bash
sudo nano /etc/systemd/system/karaoke-backend.service
```

3. Adicione o seguinte conteúdo:
```
[Unit]
Description=Karaoke App Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/caminho/para/karaoke-app/backend
ExecStart=/caminho/para/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Ative e inicie o serviço:
```bash
sudo systemctl enable karaoke-backend
sudo systemctl start karaoke-backend
```

### Configuração do Nginx

1. Instale o Nginx:
```bash
sudo apt-get install nginx
```

2. Crie uma configuração para o site:
```bash
sudo nano /etc/nginx/sites-available/karaoke-app
```

3. Adicione o seguinte conteúdo:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /caminho/para/karaoke-app/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /data {
        alias /caminho/para/karaoke-app/data;
    }
}
```

4. Ative a configuração e reinicie o Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/karaoke-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 3. Implantação em Nuvem

### Opção 1: Render

1. Backend:
   - Crie uma conta no Render (render.com)
   - Crie um novo Web Service
   - Conecte ao repositório Git
   - Configure o comando de build: `pip install -r requirements.txt`
   - Configure o comando de início: `cd backend && gunicorn app:app`
   - Defina as variáveis de ambiente necessárias

2. Frontend:
   - Crie um novo Static Site no Render
   - Conecte ao mesmo repositório Git
   - Configure o diretório de publicação: `frontend`
   - Configure o comando de build (se necessário)

### Opção 2: Railway

1. Crie uma conta no Railway (railway.app)
2. Crie um novo projeto
3. Adicione um serviço a partir do repositório Git
4. Configure as variáveis de ambiente
5. Railway detectará automaticamente o tipo de aplicação e configurará o build

### Opção 3: Vercel + PythonAnywhere

1. Frontend (Vercel):
   - Crie uma conta no Vercel (vercel.com)
   - Importe o repositório Git
   - Configure o diretório raiz como `frontend`
   - Configure variáveis de ambiente para apontar para o backend

2. Backend (PythonAnywhere):
   - Crie uma conta no PythonAnywhere (pythonanywhere.com)
   - Crie um novo aplicativo web
   - Configure o WSGI para apontar para o arquivo app.py
   - Configure as variáveis de ambiente necessárias

## Configuração do Banco de Dados

### SQLite (Desenvolvimento)

Não é necessária configuração adicional. O banco de dados será criado automaticamente na pasta `data`.

### MySQL (Produção)

1. Crie um banco de dados MySQL:
```sql
CREATE DATABASE karaoke_app;
CREATE USER 'karaoke_user'@'localhost' IDENTIFIED BY 'sua_senha';
GRANT ALL PRIVILEGES ON karaoke_app.* TO 'karaoke_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Configure as variáveis de ambiente:
```
DB_HOST=localhost
DB_USER=karaoke_user
DB_PASSWORD=sua_senha
DB_NAME=karaoke_app
```

## Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend` com as seguintes variáveis:

```
# Configuração do Servidor
DEBUG=False
PORT=5000
HOST=0.0.0.0

# Configuração do Banco de Dados
DB_HOST=localhost
DB_USER=karaoke_user
DB_PASSWORD=sua_senha
DB_NAME=karaoke_app
```

## Verificação da Implantação

Após a implantação, verifique se:

1. O backend está respondendo em `/api/songs`
2. O frontend está carregando corretamente
3. É possível fazer upload de arquivos MIDI e letras
4. A extração de acordes está funcionando
5. A sincronização de letras e acordes está funcionando

## Solução de Problemas

### Problemas Comuns

1. **Erro de conexão com o banco de dados**:
   - Verifique as credenciais no arquivo `.env`
   - Verifique se o banco de dados está em execução
   - Verifique se o usuário tem permissões adequadas

2. **Erro 404 ao acessar a API**:
   - Verifique se o servidor backend está em execução
   - Verifique a configuração do proxy no Nginx

3. **Erro ao processar arquivos MIDI**:
   - Verifique se as bibliotecas music21 e pychord estão instaladas
   - Verifique se o arquivo MIDI está em um formato compatível

4. **Problemas de CORS**:
   - Verifique se o CORS está configurado corretamente no backend
   - Verifique se as URLs do frontend e backend estão configuradas corretamente

## Manutenção

### Backup do Banco de Dados

Para MySQL:
```bash
mysqldump -u karaoke_user -p karaoke_app > backup.sql
```

### Atualização do Aplicativo

1. Pare os serviços:
```bash
sudo systemctl stop karaoke-backend
```

2. Atualize o código:
```bash
git pull origin main
```

3. Reinicie os serviços:
```bash
sudo systemctl start karaoke-backend
```

## Segurança

- Mantenha o sistema operacional e todas as dependências atualizadas
- Use HTTPS para proteger a comunicação entre cliente e servidor
- Limite o tamanho dos arquivos de upload para evitar ataques de negação de serviço
- Implemente autenticação se o aplicativo for usado em um ambiente público

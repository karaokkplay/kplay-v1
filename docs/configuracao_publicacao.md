# Guia de Configuração e Publicação do K-Play

Este documento fornece instruções detalhadas para configurar, hospedar e publicar o aplicativo K-Play na Google Play Store.

## Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Opções de Hospedagem](#opções-de-hospedagem)
3. [Configuração do Backend](#configuração-do-backend)
4. [Configuração do Frontend](#configuração-do-frontend)
5. [Configuração de Autenticação](#configuração-de-autenticação)
6. [Configuração de Pagamentos](#configuração-de-pagamentos)
7. [Configuração de Email (PHPMail)](#configuração-de-email-phpmail)
8. [Geração do APK para Android](#geração-do-apk-para-android)
9. [Publicação na Google Play Store](#publicação-na-google-play-store)
10. [Ajustes Finais e Otimizações](#ajustes-finais-e-otimizações)

## Requisitos do Sistema

### Backend
- Python 3.8 ou superior
- Flask 2.0 ou superior
- MySQL 8.0 ou superior
- Bibliotecas: music21, pychord, flask-cors, mysql-connector-python

### Frontend
- Node.js 14.0 ou superior
- React 17.0 ou superior
- Bibliotecas: Tone.js, React Router, Axios

### Ferramentas de Desenvolvimento
- Visual Studio Code (recomendado para edição)
- Android Studio (para compilação do APK)
- JDK 17 ou superior
- Capacitor para empacotamento do aplicativo web como aplicativo Android

## Opções de Hospedagem

### Backend

#### Opção 1: Render
- **Vantagens**: Fácil implantação, suporte nativo para Python/Flask, plano gratuito disponível
- **Configuração**:
  1. Crie uma conta em [render.com](https://render.com)
  2. Crie um novo Web Service
  3. Conecte ao repositório Git do projeto
  4. Selecione o tipo "Python"
  5. Configure o comando de inicialização: `gunicorn app:app`
  6. Defina as variáveis de ambiente necessárias

#### Opção 2: Railway
- **Vantagens**: Implantação simples, bom desempenho, plano gratuito generoso
- **Configuração**:
  1. Crie uma conta em [railway.app](https://railway.app)
  2. Inicie um novo projeto
  3. Adicione um serviço Python
  4. Conecte ao repositório Git
  5. Configure o comando de inicialização: `gunicorn app:app`
  6. Configure as variáveis de ambiente

#### Opção 3: PythonAnywhere
- **Vantagens**: Especializado em Python, fácil configuração de banco de dados
- **Configuração**:
  1. Crie uma conta em [pythonanywhere.com](https://pythonanywhere.com)
  2. Crie uma nova aplicação web
  3. Selecione Flask como framework
  4. Configure o WSGI file para apontar para sua aplicação
  5. Configure o banco de dados MySQL

### Frontend

#### Opção 1: Netlify
- **Vantagens**: Otimizado para aplicações React, implantação contínua, CDN global
- **Configuração**:
  1. Crie uma conta em [netlify.com](https://netlify.com)
  2. Conecte ao repositório Git
  3. Configure o comando de build: `npm run build`
  4. Defina o diretório de publicação: `build` ou `dist`
  5. Configure variáveis de ambiente para apontar para o backend

#### Opção 2: Vercel
- **Vantagens**: Excelente para React, implantação automática, bom desempenho
- **Configuração**:
  1. Crie uma conta em [vercel.com](https://vercel.com)
  2. Importe o projeto do Git
  3. Configure as opções de build
  4. Defina variáveis de ambiente

#### Opção 3: GitHub Pages
- **Vantagens**: Gratuito, fácil integração com GitHub Actions
- **Configuração**:
  1. Configure o GitHub Actions para build automático
  2. Adicione um arquivo de configuração para SPA (single-page application)
  3. Configure o domínio personalizado (opcional)

## Configuração do Backend

### 1. Configuração do Banco de Dados

```python
# config.py
import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'kplay_db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sua_chave_jwt_aqui')

# Configurações de email
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'seu_email@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'sua_senha_de_app')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'seu_email@gmail.com')
```

### 2. Script de Inicialização do Banco de Dados

Crie um arquivo `init_db.py` para inicializar o banco de dados:

```python
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def init_database():
    # Conectar ao MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    # Criar banco de dados se não existir
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    
    # Criar tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255),
        auth_provider VARCHAR(20),
        auth_id VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        plan VARCHAR(20) NOT NULL,
        status VARCHAR(20) NOT NULL,
        start_date TIMESTAMP NOT NULL,
        end_date TIMESTAMP NOT NULL,
        payment_method VARCHAR(20),
        transaction_id VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(100) NOT NULL,
        artist VARCHAR(100),
        midi_file VARCHAR(255),
        lyrics_file VARCHAR(255),
        chords_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database()
```

### 3. Configuração do Servidor WSGI para Produção

Crie um arquivo `wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### 4. Arquivo de Dependências

Crie um arquivo `requirements.txt`:

```
Flask==2.0.1
flask-cors==3.0.10
mysql-connector-python==8.0.26
music21==7.1.0
pychord==1.1.0
gunicorn==20.1.0
python-dotenv==0.19.0
Flask-JWT-Extended==4.3.1
Flask-Mail==0.9.1
bcrypt==3.2.0
```

## Configuração do Frontend

### 1. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto frontend:

```
REACT_APP_API_URL=https://sua-api.render.com
REACT_APP_GOOGLE_CLIENT_ID=seu_google_client_id
REACT_APP_FACEBOOK_APP_ID=seu_facebook_app_id
REACT_APP_DISCORD_CLIENT_ID=seu_discord_client_id
```

### 2. Configuração para Build de Produção

Atualize o arquivo `package.json` para incluir scripts de build:

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "build:android": "react-scripts build && npx cap sync android",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

### 3. Configuração do Service Worker para PWA

Atualize o arquivo `service-worker.js` para incluir cache de recursos importantes:

```javascript
const CACHE_NAME = 'kplay-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/js/main.chunk.js',
  '/static/js/0.chunk.js',
  '/static/js/bundle.js',
  '/static/css/main.chunk.css',
  '/manifest.json',
  '/logo192.png',
  '/logo512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
```

## Configuração de Autenticação

### 1. Google Authentication

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Vá para "APIs & Services" > "Credentials"
4. Crie um "OAuth 2.0 Client ID" para aplicativo web
5. Adicione os domínios autorizados e URIs de redirecionamento
6. Copie o Client ID e atualize no frontend

### 2. Facebook Authentication

1. Acesse o [Facebook Developers](https://developers.facebook.com/)
2. Crie um novo aplicativo
3. Adicione o produto "Facebook Login"
4. Configure os domínios válidos e URIs de redirecionamento
5. Copie o App ID e atualize no frontend

### 3. Discord Authentication

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá para "OAuth2"
4. Adicione os redirecionamentos
5. Copie o Client ID e atualize no frontend

## Configuração de Pagamentos

### 1. Integração com Gateway de Pagamento

Para integrar com um gateway de pagamento real como o Stripe:

1. Crie uma conta no [Stripe](https://stripe.com)
2. Obtenha as chaves de API (pública e secreta)
3. Instale a biblioteca Stripe no backend:

```bash
pip install stripe
```

4. Configure o backend para processar pagamentos:

```python
# payment.py
import stripe
from flask import Blueprint, request, jsonify
from config import STRIPE_SECRET_KEY

payment_bp = Blueprint('payment', __name__)
stripe.api_key = STRIPE_SECRET_KEY

@payment_bp.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.json
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='brl',
            metadata={'user_id': data['user_id'], 'plan': data['plan']}
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

5. Integre o Stripe no frontend:

```bash
npm install @stripe/react-stripe-js @stripe/stripe-js
```

## Configuração de Email (PHPMail)

### 1. Configuração no Backend

Para usar PHPMail no backend Python, você pode usar a biblioteca Flask-Mail:

```python
# mail.py
from flask import Flask
from flask_mail import Mail, Message
from config import (
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS,
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
)

def configure_mail(app):
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
    
    return Mail(app)

def send_email(mail, subject, recipient, template):
    msg = Message(
        subject,
        recipients=[recipient],
        html=template
    )
    mail.send(msg)
```

### 2. Exemplo de Uso para Confirmação de Pagamento

```python
@payment_bp.route('/confirm-payment', methods=['POST'])
def confirm_payment():
    data = request.json
    user_email = data['email']
    plan = data['plan']
    
    # Enviar email de confirmação
    template = f"""
    <h1>Confirmação de Pagamento - K-Play</h1>
    <p>Olá,</p>
    <p>Seu pagamento para o plano {plan} foi confirmado com sucesso!</p>
    <p>Agora você tem acesso a todos os recursos premium do K-Play.</p>
    <p>Obrigado por escolher nosso aplicativo!</p>
    <p>Equipe K-Play</p>
    """
    
    send_email(mail, "Confirmação de Pagamento - K-Play", user_email, template)
    
    return jsonify({'success': True})
```

## Geração do APK para Android

### 1. Preparação do Ambiente

1. Instale o Android Studio
2. Instale o JDK 17 ou superior
3. Configure as variáveis de ambiente ANDROID_SDK_ROOT e JAVA_HOME

### 2. Configuração do Capacitor

1. Instale o Capacitor no projeto:

```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "K-Play" "com.kplay.app" --web-dir="build"
```

2. Crie um arquivo `capacitor.config.json` na raiz do projeto:

```json
{
  "appId": "com.kplay.app",
  "appName": "K-Play",
  "webDir": "build",
  "bundledWebRuntime": false,
  "server": {
    "androidScheme": "https"
  }
}
```

3. Adicione a plataforma Android:

```bash
npm run build
npx cap add android
```

### 3. Personalização do Aplicativo Android

1. Abra o projeto Android no Android Studio:

```bash
npx cap open android
```

2. Substitua o ícone do aplicativo:
   - Coloque o arquivo `K-Play.png` em `android/app/src/main/res/drawable`
   - Gere ícones em diferentes resoluções usando o [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/icons-launcher.html)
   - Substitua os arquivos em `android/app/src/main/res/mipmap-*`

3. Atualize o nome e as cores do aplicativo em `android/app/src/main/res/values/strings.xml`:

```xml
<resources>
    <string name="app_name">K-Play</string>
    <color name="colorPrimary">#FF8C00</color>
    <color name="colorPrimaryDark">#000000</color>
    <color name="colorAccent">#FFFFFF</color>
</resources>
```

### 4. Geração do APK

1. No Android Studio, vá para Build > Build Bundle(s) / APK(s) > Build APK(s)
2. Ou use o comando via terminal:

```bash
cd android
./gradlew assembleDebug
```

3. O APK será gerado em `android/app/build/outputs/apk/debug/app-debug.apk`

### 5. Script de Geração Automatizada

Crie um arquivo `generate_apk.sh` na raiz do projeto:

```bash
#!/bin/bash

# Definir variáveis
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ANDROID_SDK_ROOT=/usr/lib/android-sdk
export JAVA_HOME
export ANDROID_SDK_ROOT

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando geração do APK para K-Play...${NC}"

# Verificar se o JDK está instalado
if [ ! -d "$JAVA_HOME" ]; then
    echo -e "${RED}JDK não encontrado. Instalando JDK 17...${NC}"
    sudo apt-get update
    sudo apt-get install -y openjdk-17-jdk
fi

# Verificar se o Android SDK está instalado
if [ ! -d "$ANDROID_SDK_ROOT" ]; then
    echo -e "${RED}Android SDK não encontrado. Por favor, instale o Android Studio.${NC}"
    exit 1
fi

# Aceitar licenças do Android SDK
echo -e "${YELLOW}Aceitando licenças do Android SDK...${NC}"
yes | sudo $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --licenses

# Construir o projeto React
echo -e "${YELLOW}Construindo o projeto React...${NC}"
npm run build

# Sincronizar com o Capacitor
echo -e "${YELLOW}Sincronizando com o Capacitor...${NC}"
npx cap sync android

# Construir o APK
echo -e "${YELLOW}Construindo o APK...${NC}"
cd android
./gradlew assembleDebug

# Verificar se o APK foi gerado
if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
    # Copiar o APK para a raiz do projeto
    cp app/build/outputs/apk/debug/app-debug.apk ../k-play-debug.apk
    echo -e "${GREEN}APK gerado com sucesso: k-play-debug.apk${NC}"
    echo -e "${YELLOW}Para gerar um APK de release, use o Android Studio para assinar o aplicativo.${NC}"
else
    echo -e "${RED}Falha ao gerar o APK.${NC}"
    exit 1
fi

cd ..
echo -e "${GREEN}Processo concluído!${NC}"
```

Torne o script executável:

```bash
chmod +x generate_apk.sh
```

## Publicação na Google Play Store

### 1. Preparação para Publicação

1. Crie uma conta de desenvolvedor na [Google Play Console](https://play.google.com/console/signup) (taxa única de $25)
2. Prepare os recursos gráficos:
   - Ícone de alta resolução (512x512 px)
   - Imagem de destaque (1024x500 px)
   - Pelo menos 2 capturas de tela do aplicativo
   - Vídeo promocional (opcional)

3. Prepare a descrição do aplicativo:
   - Título: K-Play
   - Descrição curta (até 80 caracteres)
   - Descrição completa (até 4000 caracteres)
   - Categoria: Música e Áudio
   - Tags relevantes

### 2. Geração do APK de Release

1. No Android Studio, vá para Build > Generate Signed Bundle / APK
2. Selecione APK
3. Crie uma nova keystore ou use uma existente
   - **IMPORTANTE**: Guarde a keystore e a senha em local seguro. Você precisará da mesma keystore para todas as atualizações futuras.
4. Selecione o tipo de release (release)
5. Finalize o processo

### 3. Envio para a Google Play Store

1. Acesse a [Google Play Console](https://play.google.com/console)
2. Crie um novo aplicativo
3. Preencha todas as informações necessárias:
   - Detalhes do aplicativo
   - Classificação de conteúdo
   - Preço e distribuição
4. Faça o upload do APK assinado
5. Envie para revisão

### 4. Configuração de Compras no Aplicativo

1. Na Google Play Console, vá para "Monetização" > "Produtos"
2. Configure as assinaturas:
   - Mensal: R$ 9,90
   - Trimestral: R$ 24,90
   - Anual: R$ 89,90
3. Defina os detalhes de cada plano
4. Integre a biblioteca Google Play Billing no aplicativo

## Ajustes Finais e Otimizações

### 1. Otimização de Desempenho

1. Comprima imagens e recursos estáticos
2. Implemente lazy loading para componentes pesados
3. Otimize o tamanho do bundle JavaScript:

```bash
npm install --save-dev source-map-explorer
```

Adicione ao package.json:

```json
"scripts": {
  "analyze": "source-map-explorer 'build/static/js/*.js'"
}
```

Execute após o build:

```bash
npm run analyze
```

### 2. Testes Finais

1. Teste o aplicativo em diferentes dispositivos Android
2. Verifique a responsividade em diferentes tamanhos de tela
3. Teste todas as funcionalidades principais:
   - Upload e processamento de arquivos MIDI
   - Extração de acordes
   - Visualização no teclado virtual
   - Autenticação com diferentes provedores
   - Processo de pagamento

### 3. Monitoramento e Analytics

1. Integre o Google Analytics para monitorar o uso do aplicativo:

```bash
npm install react-ga
```

2. Configure no arquivo principal:

```javascript
import ReactGA from 'react-ga';
ReactGA.initialize('UA-XXXXXXXXX-X');
ReactGA.pageview(window.location.pathname + window.location.search);
```

### 4. Backup e Recuperação

1. Configure backups automáticos do banco de dados
2. Implemente um sistema de logs para rastrear erros
3. Crie um plano de recuperação de desastres

---

## Conclusão

Este guia fornece todas as informações necessárias para configurar, hospedar e publicar o aplicativo K-Play na Google Play Store. Siga as etapas cuidadosamente e consulte a documentação oficial das ferramentas mencionadas para obter informações mais detalhadas.

Para qualquer dúvida ou suporte adicional, entre em contato com a equipe de desenvolvimento.

**Lembre-se**: Mantenha suas chaves de API, senhas e arquivos de keystore em local seguro. Nunca compartilhe essas informações ou as inclua em repositórios públicos.

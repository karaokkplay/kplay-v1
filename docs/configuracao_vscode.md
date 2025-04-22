# Guia de Configuração do Visual Studio Code para o Projeto K-Play

Este documento fornece instruções detalhadas para configurar o Visual Studio Code (VS Code) para desenvolvimento do aplicativo K-Play no Linux, incluindo extensões recomendadas, configurações e dicas para maximizar sua produtividade.

## Índice

1. [Instalação do VS Code no Linux](#instalação-do-vs-code-no-linux)
2. [Extensões Recomendadas](#extensões-recomendadas)
3. [Configurações Personalizadas](#configurações-personalizadas)
4. [Integração com Git](#integração-com-git)
5. [Configuração para Python (Backend)](#configuração-para-python-backend)
6. [Configuração para JavaScript/React (Frontend)](#configuração-para-javascriptreact-frontend)
7. [Depuração](#depuração)
8. [Atalhos de Teclado Úteis](#atalhos-de-teclado-úteis)
9. [Dicas para Produtividade](#dicas-para-produtividade)

## Instalação do VS Code no Linux

### Usando apt (Debian, Ubuntu, Linux Mint)

```bash
# Atualizar repositórios
sudo apt update

# Instalar dependências
sudo apt install -y software-properties-common apt-transport-https wget

# Baixar e instalar a chave GPG da Microsoft
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -

# Adicionar o repositório do VS Code
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

# Atualizar repositórios novamente
sudo apt update

# Instalar o VS Code
sudo apt install -y code
```

### Usando snap (Ubuntu e outras distribuições compatíveis)

```bash
sudo snap install code --classic
```

### Usando flatpak (Fedora, CentOS, RHEL)

```bash
# Instalar flatpak se ainda não estiver instalado
sudo dnf install flatpak

# Adicionar o repositório Flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Instalar o VS Code
flatpak install flathub com.visualstudio.code
```

## Extensões Recomendadas

### Essenciais para o Projeto K-Play

1. **Python** (ms-python.python)
   - Suporte completo para desenvolvimento Python
   - Linting, debugging, IntelliSense

2. **Pylance** (ms-python.vscode-pylance)
   - Servidor de linguagem Python aprimorado
   - Análise de tipo, autocompletar avançado

3. **JavaScript and TypeScript** (ms-vscode.vscode-typescript-next)
   - Suporte aprimorado para JavaScript e TypeScript
   - IntelliSense, navegação de código

4. **ESLint** (dbaeumer.vscode-eslint)
   - Linting para JavaScript/React
   - Identifica problemas de código

5. **Prettier** (esbenp.prettier-vscode)
   - Formatação consistente para JavaScript, HTML, CSS
   - Configurável para seguir padrões de código

6. **React Extension Pack** (dsznajder.es7-react-js-snippets)
   - Snippets para React
   - Atalhos para componentes e hooks

7. **Live Server** (ritwickdey.liveserver)
   - Servidor local com recarga automática
   - Útil para testar o frontend

8. **REST Client** (humao.rest-client)
   - Testar APIs REST diretamente no VS Code
   - Útil para testar o backend

9. **SQLite** (alexcvzz.vscode-sqlite)
   - Visualizar e editar bancos de dados SQLite
   - Útil para desenvolvimento local

10. **Material Icon Theme** (pkief.material-icon-theme)
    - Ícones para diferentes tipos de arquivos
    - Melhora a navegação visual do projeto

### Para instalar todas as extensões de uma vez

Abra o terminal e execute:

```bash
code --install-extension ms-python.python \
     --install-extension ms-python.vscode-pylance \
     --install-extension ms-vscode.vscode-typescript-next \
     --install-extension dbaeumer.vscode-eslint \
     --install-extension esbenp.prettier-vscode \
     --install-extension dsznajder.es7-react-js-snippets \
     --install-extension ritwickdey.liveserver \
     --install-extension humao.rest-client \
     --install-extension alexcvzz.vscode-sqlite \
     --install-extension pkief.material-icon-theme
```

## Configurações Personalizadas

Crie um arquivo `.vscode/settings.json` na raiz do projeto com as seguintes configurações:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.rulers": [100],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.colorTheme": "Default Dark+",
  "workbench.iconTheme": "material-icon-theme",
  "terminal.integrated.defaultProfile.linux": "bash",
  "terminal.integrated.fontFamily": "monospace",
  "terminal.integrated.fontSize": 14,
  
  // Configurações Python
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.extraPaths": ["${workspaceFolder}/backend"],
  
  // Configurações JavaScript/React
  "javascript.updateImportsOnFileMove.enabled": "always",
  "javascript.format.enable": false, // Usar Prettier em vez disso
  "typescript.format.enable": false, // Usar Prettier em vez disso
  "prettier.singleQuote": true,
  "prettier.semi": true,
  "prettier.printWidth": 100,
  "prettier.trailingComma": "es5",
  
  // Configurações específicas para o projeto K-Play
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true,
    "editor.tabSize": 4
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  
  // Cores personalizadas para o tema K-Play (preto, laranja, branco)
  "workbench.colorCustomizations": {
    "activityBar.background": "#111111",
    "activityBar.foreground": "#ff8c00",
    "activityBarBadge.background": "#ff8c00",
    "activityBarBadge.foreground": "#000000",
    "titleBar.activeBackground": "#111111",
    "titleBar.activeForeground": "#ff8c00",
    "statusBar.background": "#111111",
    "statusBar.foreground": "#ff8c00",
    "editorCursor.foreground": "#ff8c00"
  }
}
```

## Integração com Git

### Configuração do Git no VS Code

1. Instale a extensão **GitLens** (eamodio.gitlens) para recursos Git avançados:

```bash
code --install-extension eamodio.gitlens
```

2. Configure o Git para o projeto:

```bash
# Na raiz do projeto
git init
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

3. Crie um arquivo `.gitignore` na raiz do projeto:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/
.env

# JavaScript/React
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
.pnp/
.pnp.js
coverage/
build/
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# Banco de dados
*.sqlite
*.db

# Arquivos de mídia
*.mid
*.midi
*.mp3
*.wav

# Arquivos de ambiente
.env
.env.local
.env.development
.env.production

# Arquivos de build Android
android/app/build/
android/app/release/
android/app/debug/
android/app/src/main/assets/
android/app/src/main/res/drawable-*/
android/app/src/main/res/mipmap-*/
android/app/src/main/res/raw/
android/app/src/main/res/values/strings.xml
android/app/src/main/res/xml/
android/build/
android/captures/
android/gradle/
android/gradlew
android/gradlew.bat
android/local.properties
android/.gradle/
```

## Configuração para Python (Backend)

### Ambiente Virtual Python

1. Crie um ambiente virtual para o backend:

```bash
# Na pasta do backend
cd /home/ubuntu/karaoke-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure o VS Code para usar este ambiente virtual:

Pressione `Ctrl+Shift+P`, digite "Python: Select Interpreter" e selecione o interpretador do ambiente virtual (`./venv/bin/python`).

### Configuração de Depuração Python

Crie um arquivo `.vscode/launch.json` na raiz do projeto:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
      },
      "args": [
        "run",
        "--no-debugger",
        "--no-reload"
      ],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Chord Extractor Test",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/test_chord_extraction.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

## Configuração para JavaScript/React (Frontend)

### Configuração do ESLint e Prettier

1. Crie um arquivo `.eslintrc.js` na pasta frontend:

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks'],
  rules: {
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

2. Crie um arquivo `.prettierrc` na pasta frontend:

```json
{
  "singleQuote": true,
  "semi": true,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "jsxBracketSameLine": false,
  "arrowParens": "avoid"
}
```

### Configuração de Depuração React

Adicione ao arquivo `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    // ... configurações Python existentes ...
    
    {
      "name": "Chrome: Launch React",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend",
      "sourceMapPathOverrides": {
        "webpack:///src/*": "${webRoot}/*"
      }
    }
  ]
}
```

## Depuração

### Depuração do Backend (Flask)

1. Abra o VS Code na pasta raiz do projeto
2. Vá para a aba "Run and Debug" (Ctrl+Shift+D)
3. Selecione "Python: Flask" na lista suspensa
4. Clique no botão de play verde ou pressione F5
5. O servidor Flask será iniciado com depuração ativada
6. Defina pontos de interrupção clicando à esquerda dos números de linha

### Depuração do Frontend (React)

1. Inicie o servidor de desenvolvimento React:

```bash
cd /home/ubuntu/karaoke-app/frontend
npm start
```

2. Vá para a aba "Run and Debug" (Ctrl+Shift+D)
3. Selecione "Chrome: Launch React" na lista suspensa
4. Clique no botão de play verde ou pressione F5
5. O Chrome será iniciado com depuração ativada
6. Defina pontos de interrupção no código React

## Atalhos de Teclado Úteis

### Geral
- `Ctrl+P`: Navegação rápida de arquivos
- `Ctrl+Shift+P`: Paleta de comandos
- `Ctrl+,`: Configurações do VS Code
- `Ctrl+B`: Alternar barra lateral
- `Ctrl+J`: Alternar terminal integrado
- `Ctrl+K Ctrl+S`: Atalhos de teclado

### Edição
- `Ctrl+Space`: Sugestões de código
- `Ctrl+Shift+Space`: Dicas de parâmetros
- `F12`: Ir para definição
- `Alt+F12`: Peek definição
- `Shift+F12`: Mostrar referências
- `F2`: Renomear símbolo
- `Ctrl+F`: Pesquisar
- `Ctrl+H`: Substituir
- `Alt+Up/Down`: Mover linha para cima/baixo
- `Shift+Alt+Up/Down`: Duplicar linha para cima/baixo
- `Ctrl+/`: Comentar/descomentar linha

### Depuração
- `F5`: Iniciar/Continuar depuração
- `F9`: Alternar ponto de interrupção
- `F10`: Passar por cima (Step over)
- `F11`: Passar para dentro (Step into)
- `Shift+F11`: Passar para fora (Step out)
- `Shift+F5`: Parar depuração

## Dicas para Produtividade

### Snippets Personalizados

Crie snippets personalizados para o projeto K-Play:

1. Pressione `Ctrl+Shift+P` e digite "Snippets"
2. Selecione "Preferences: Configure User Snippets"
3. Escolha "New Global Snippets file..." ou selecione um arquivo de linguagem específico
4. Crie snippets para componentes React, funções Python, etc.

Exemplo para React:

```json
{
  "K-Play React Component": {
    "prefix": "krc",
    "body": [
      "import React, { useState, useEffect } from 'react';",
      "import './${1:ComponentName}.css';",
      "",
      "const ${1:ComponentName} = ({ ${2:props} }) => {",
      "  const [state, setState] = useState(${3:initialState});",
      "",
      "  useEffect(() => {",
      "    $4",
      "  }, []);",
      "",
      "  return (",
      "    <div className=\"${5:${1/(.*)/${1:/downcase}/}-container}\">",
      "      $6",
      "    </div>",
      "  );",
      "};",
      "",
      "export default ${1:ComponentName};"
    ],
    "description": "Create a K-Play React component"
  }
}
```

### Workspace Personalizado

Crie um arquivo de workspace para o projeto K-Play:

1. Vá para File > Save Workspace As...
2. Salve como `k-play.code-workspace` na raiz do projeto
3. Edite o arquivo para incluir configurações específicas:

```json
{
  "folders": [
    {
      "name": "K-Play",
      "path": "."
    },
    {
      "name": "Backend",
      "path": "backend"
    },
    {
      "name": "Frontend",
      "path": "frontend"
    }
  ],
  "settings": {
    // Configurações específicas do workspace
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "dsznajder.es7-react-js-snippets",
      "ritwickdey.liveserver",
      "eamodio.gitlens",
      "pkief.material-icon-theme"
    ]
  }
}
```

### Tarefas Personalizadas

Crie um arquivo `.vscode/tasks.json` para automatizar tarefas comuns:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd ${workspaceFolder}/backend && source venv/bin/activate && python app.py",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "cd ${workspaceFolder}/frontend && npm start",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Start Full Stack",
      "dependsOn": ["Start Backend", "Start Frontend"],
      "problemMatcher": []
    },
    {
      "label": "Build APK",
      "type": "shell",
      "command": "${workspaceFolder}/generate_apk.sh",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "cd ${workspaceFolder}/backend && source venv/bin/activate && python -m unittest discover",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "problemMatcher": []
    }
  ]
}
```

Para executar estas tarefas:
1. Pressione `Ctrl+Shift+P`
2. Digite "Tasks: Run Task"
3. Selecione a tarefa desejada

---

## Conclusão

Este guia fornece uma configuração completa do Visual Studio Code para o desenvolvimento do aplicativo K-Play no Linux. Seguindo estas instruções, você terá um ambiente de desenvolvimento otimizado com todas as ferramentas necessárias para trabalhar eficientemente no projeto.

Para qualquer dúvida ou suporte adicional na configuração do VS Code, entre em contato com a equipe de desenvolvimento.

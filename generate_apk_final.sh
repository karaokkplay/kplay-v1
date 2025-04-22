#!/bin/bash

# Script para gerar APK Android do aplicativo de karaokê
# Este script deve ser executado na raiz do projeto karaoke-app

echo "=== Iniciando processo de geração do APK Android ==="

# Verificar se as ferramentas necessárias estão instaladas
command -v java >/dev/null 2>&1 || { echo "Java não encontrado. Instale o JDK 17."; exit 1; }
command -v gradle >/dev/null 2>&1 || { echo "Gradle não encontrado. Instale o Gradle."; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "NPX não encontrado. Instale o Node.js e npm."; exit 1; }

# Configurar variáveis de ambiente para o Android SDK e Java 17
export ANDROID_SDK_ROOT=/usr/lib/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

echo "Usando Java: $(java -version 2>&1 | head -n 1)"
echo "JAVA_HOME: $JAVA_HOME"

# Aceitar licenças do Android SDK automaticamente
echo "Tentando aceitar licenças do Android SDK..."
mkdir -p "$ANDROID_SDK_ROOT/licenses"
echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$ANDROID_SDK_ROOT/licenses/android-sdk-license"
echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> "$ANDROID_SDK_ROOT/licenses/android-sdk-license"
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > "$ANDROID_SDK_ROOT/licenses/android-sdk-preview-license"

# Criar ícones para o aplicativo se não existirem
if [ ! -f "frontend/assets/icon-512x512.png" ]; then
  echo "Criando ícones padrão para o aplicativo..."
  mkdir -p frontend/assets
  # Usar um ícone padrão ou criar um básico
  convert -size 512x512 xc:navy -fill white -gravity center -pointsize 40 -annotate 0 "Karaokê\nAcordes" frontend/assets/icon-512x512.png
  
  # Criar versões em diferentes tamanhos
  for size in 72 96 128 144 152 192 384; do
    convert frontend/assets/icon-512x512.png -resize ${size}x${size} frontend/assets/icon-${size}x${size}.png
  done
fi

# Sincronizar os arquivos da PWA com o projeto Android
echo "Sincronizando arquivos com o projeto Android..."
npx cap sync android

# Entrar no diretório do projeto Android
cd android

# Configurar o arquivo local.properties com o caminho do SDK
echo "sdk.dir=/usr/lib/android-sdk" > local.properties

# Configurar o arquivo gradle.properties para evitar problemas de memória
echo "org.gradle.jvmargs=-Xmx2048m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8" > gradle.properties
echo "android.useAndroidX=true" >> gradle.properties
echo "android.enableJetifier=true" >> gradle.properties
echo "org.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64" >> gradle.properties

# Modificar o arquivo build.gradle para usar versões do SDK disponíveis
echo "Ajustando configurações do build.gradle..."
if [ -f "app/build.gradle" ]; then
  # Usar SDK 29 que geralmente já está disponível no sistema
  sed -i 's/compileSdk 30/compileSdk 29/g' app/build.gradle
  sed -i 's/targetSdk 30/targetSdk 29/g' app/build.gradle
fi

# Compilar o APK em modo debug (mais rápido e não requer assinatura)
echo "Compilando o APK em modo debug..."
./gradlew assembleDebug

# Verificar se a compilação foi bem-sucedida
if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
  # Copiar o APK para a raiz do projeto para facilitar o acesso
  cp app/build/outputs/apk/debug/app-debug.apk ../karaoke-app-debug.apk
  echo "=== APK gerado com sucesso! ==="
  echo "O APK está disponível em: $(cd .. && pwd)/karaoke-app-debug.apk"
else
  echo "=== Erro na geração do APK ==="
  echo "Verifique os logs acima para identificar o problema."
  echo ""
  echo "Se o problema persistir, você pode precisar aceitar as licenças manualmente:"
  echo "1. Instale o Android Studio, ou"
  echo "2. Execute: yes | sudo \$ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --licenses"
fi

# Voltar para o diretório raiz
cd ..

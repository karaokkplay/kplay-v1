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
# Removido o parâmetro MaxPermSize que não é mais suportado no Java 17
echo "org.gradle.jvmargs=-Xmx2048m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8" > gradle.properties
echo "android.useAndroidX=true" >> gradle.properties
echo "android.enableJetifier=true" >> gradle.properties
echo "org.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64" >> gradle.properties

# Modificar o arquivo build.gradle para garantir compatibilidade
sed -i 's/compileSdkVersion.*/compileSdkVersion 30/' app/build.gradle
sed -i 's/targetSdkVersion.*/targetSdkVersion 30/' app/build.gradle
sed -i 's/minSdkVersion.*/minSdkVersion 21/' app/build.gradle

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
fi

# Voltar para o diretório raiz
cd ..

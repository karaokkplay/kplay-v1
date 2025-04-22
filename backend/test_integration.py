#!/usr/bin/env python3
import os
import sys
import time
import subprocess

def test_backend_server():
    """
    Testa o servidor backend iniciando-o e verificando se está respondendo
    """
    print("Iniciando o servidor backend para teste...")
    
    # Caminho para o arquivo app.py
    app_path = "/home/ubuntu/karaoke-app/backend/app.py"
    
    # Iniciar o servidor em um processo separado
    server_process = subprocess.Popen(
        ["python3", app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguardar um pouco para o servidor iniciar
    print("Aguardando o servidor iniciar...")
    time.sleep(3)
    
    # Verificar se o servidor está rodando
    try:
        # Testar conexão com o servidor
        import requests
        response = requests.get("http://localhost:5000/api/songs")
        
        if response.status_code == 200:
            print("✅ Servidor backend está rodando e respondendo corretamente!")
            print(f"Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Servidor respondeu com código de status: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Erro ao conectar ao servidor: {e}")
        return False
    
    finally:
        # Encerrar o servidor
        print("Encerrando o servidor de teste...")
        server_process.terminate()
        server_process.wait()

def test_frontend_files():
    """
    Testa se todos os arquivos necessários do frontend estão presentes
    """
    print("\nVerificando arquivos do frontend...")
    
    # Lista de arquivos essenciais
    essential_files = [
        "/home/ubuntu/karaoke-app/frontend/index.html",
        "/home/ubuntu/karaoke-app/frontend/css/styles.css",
        "/home/ubuntu/karaoke-app/frontend/js/app.js",
        "/home/ubuntu/karaoke-app/frontend/js/midi-player.js",
        "/home/ubuntu/karaoke-app/frontend/js/lyrics-sync.js"
    ]
    
    # Verificar cada arquivo
    all_files_present = True
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"✅ Arquivo encontrado: {file_path}")
        else:
            print(f"❌ Arquivo não encontrado: {file_path}")
            all_files_present = False
    
    return all_files_present

def test_integration():
    """
    Testa a integração entre backend e frontend
    """
    print("\nTestando integração entre backend e frontend...")
    
    # Verificar se os arquivos de teste estão presentes
    midi_path = "/home/ubuntu/karaoke-app/data/midi/musica_exemplo.mid"
    lyrics_path = "/home/ubuntu/karaoke-app/data/lyrics/musica_exemplo.txt"
    
    if not os.path.exists(midi_path) or not os.path.exists(lyrics_path):
        print("❌ Arquivos de teste não encontrados!")
        return False
    
    print("✅ Arquivos de teste encontrados")
    
    # Verificar se o backend pode processar os arquivos
    print("\nVerificando se o backend pode processar os arquivos...")
    
    # Testar extração de acordes
    try:
        import music21
        midi = music21.converter.parse(midi_path)
        print("✅ Backend pode processar arquivos MIDI")
    except Exception as e:
        print(f"❌ Erro ao processar MIDI: {e}")
        return False
    
    # Verificar se o frontend pode carregar os arquivos
    print("\nVerificando se o frontend pode carregar os arquivos...")
    
    # Verificar se as bibliotecas necessárias estão referenciadas no HTML
    with open("/home/ubuntu/karaoke-app/frontend/index.html", "r") as f:
        html_content = f.read()
        
        if "tone" in html_content.lower() and "midi" in html_content.lower():
            print("✅ Frontend referencia as bibliotecas necessárias")
        else:
            print("❌ Frontend não referencia todas as bibliotecas necessárias")
            return False
    
    print("\nTestes de integração concluídos com sucesso!")
    return True

def run_all_tests():
    """
    Executa todos os testes
    """
    print("=== INICIANDO TESTES DA APLICAÇÃO ===\n")
    
    # Testar backend
    backend_ok = test_backend_server()
    
    # Testar frontend
    frontend_ok = test_frontend_files()
    
    # Testar integração
    integration_ok = test_integration()
    
    # Resumo dos testes
    print("\n=== RESUMO DOS TESTES ===")
    print(f"Backend: {'✅ OK' if backend_ok else '❌ Falhou'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ Falhou'}")
    print(f"Integração: {'✅ OK' if integration_ok else '❌ Falhou'}")
    
    # Resultado final
    if backend_ok and frontend_ok and integration_ok:
        print("\n✅ TODOS OS TESTES PASSARAM! A aplicação está funcionando corretamente.")
        return True
    else:
        print("\n❌ ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    # Instalar requests se necessário
    try:
        import requests
    except ImportError:
        print("Instalando dependência: requests")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    # Executar todos os testes
    run_all_tests()

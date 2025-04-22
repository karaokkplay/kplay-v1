import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'karaoke_app')
}

# Configuração de pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')

# Pastas para armazenamento de arquivos
MIDI_FOLDER = os.path.join(DATA_DIR, 'midi')
LYRICS_FOLDER = os.path.join(DATA_DIR, 'lyrics')
CHORDS_FOLDER = os.path.join(DATA_DIR, 'chords')

# Criar diretórios se não existirem
for folder in [MIDI_FOLDER, LYRICS_FOLDER, CHORDS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Configuração da aplicação
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# Tamanho máximo de upload (16MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Extensões permitidas
ALLOWED_EXTENSIONS = {
    'midi': {'mid', 'midi'},
    'lyrics': {'txt'}
}

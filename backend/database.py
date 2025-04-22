from flask import Flask
from flask_cors import CORS
import backend.config as configd.config as config
import os
import json
import mysql.connector
from mysql.connector import Error

def create_db_connection():
    """Cria uma conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(
            host=config.DB_CONFIG['host'],
            user=config.DB_CONFIG['user'],
            password=config.DB_CONFIG['password'],
            database=config.DB_CONFIG['database']
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def create_database_if_not_exists():
    """Cria o banco de dados se não existir"""
    try:
        # Conectar sem especificar o banco de dados
        connection = mysql.connector.connect(
            host=config.DB_CONFIG['host'],
            user=config.DB_CONFIG['user'],
            password=config.DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Criar banco de dados se não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_CONFIG['database']}")
            
            # Usar o banco de dados
            cursor.execute(f"USE {config.DB_CONFIG['database']}")
            
            # Criar tabelas
            create_tables(cursor)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print("Banco de dados e tabelas criados com sucesso!")
            return True
    
    except Error as e:
        print(f"Erro ao criar banco de dados: {e}")
        return False

def create_tables(cursor):
    """Cria as tabelas necessárias no banco de dados"""
    
    # Tabela songs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        midi_path VARCHAR(255) NOT NULL,
        lyrics_path VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabela lyrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lyrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        song_id INT NOT NULL,
        text TEXT NOT NULL,
        start_time INT NOT NULL,
        FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
    )
    """)
    
    # Tabela chords
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        song_id INT NOT NULL,
        chord_name VARCHAR(50) NOT NULL,
        start_time INT NOT NULL,
        components TEXT,
        FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
    )
    """)

def init_app():
    """Inicializa a aplicação Flask"""
    app = Flask(__name__)
    CORS(app)
    
    # Configurações da aplicação
    app.config['UPLOAD_FOLDER'] = config.DATA_DIR
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    
    return app

def save_song_to_db(title, artist, midi_path, lyrics_path):
    """Salva informações da música no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Inserir na tabela songs
            query = """
            INSERT INTO songs (title, artist, midi_path, lyrics_path)
            VALUES (%s, %s, %s, %s)
            """
            values = (title, artist, midi_path, lyrics_path)
            
            cursor.execute(query, values)
            connection.commit()
            
            # Obter o ID da música inserida
            song_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            return song_id
        
        except Error as e:
            print(f"Erro ao salvar música no banco de dados: {e}")
            return None
    
    return None

def save_lyrics_to_db(song_id, lyrics_data):
    """Salva as linhas da letra no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Inserir na tabela lyrics
            query = """
            INSERT INTO lyrics (song_id, text, start_time)
            VALUES (%s, %s, %s)
            """
            
            for lyric in lyrics_data:
                values = (song_id, lyric['text'], lyric['time'])
                cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Error as e:
            print(f"Erro ao salvar letras no banco de dados: {e}")
            return False
    
    return False

def save_chords_to_db(song_id, chords_data):
    """Salva os acordes no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Inserir na tabela chords
            query = """
            INSERT INTO chords (song_id, chord_name, start_time, components)
            VALUES (%s, %s, %s, %s)
            """
            
            for chord in chords_data:
                components_json = json.dumps(chord.get('components', []))
                values = (song_id, chord['chord'], chord['time'], components_json)
                cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Error as e:
            print(f"Erro ao salvar acordes no banco de dados: {e}")
            return False
    
    return False

def get_song_by_id(song_id):
    """Obtém informações de uma música pelo ID"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Consultar tabela songs
            query = """
            SELECT * FROM songs WHERE id = %s
            """
            cursor.execute(query, (song_id,))
            song = cursor.fetchone()
            
            if not song:
                cursor.close()
                connection.close()
                return None
            
            # Consultar letras
            query = """
            SELECT text, start_time FROM lyrics
            WHERE song_id = %s
            ORDER BY start_time
            """
            cursor.execute(query, (song_id,))
            lyrics = cursor.fetchall()
            
            # Consultar acordes
            query = """
            SELECT chord_name, start_time, components FROM chords
            WHERE song_id = %s
            ORDER BY start_time
            """
            cursor.execute(query, (song_id,))
            chords = cursor.fetchall()
            
            # Processar acordes para o formato esperado
            processed_chords = []
            for chord in chords:
                components = json.loads(chord['components']) if chord['components'] else []
                processed_chords.append({
                    'time': chord['start_time'],
                    'chord': chord['chord_name'],
                    'components': components
                })
            
            # Processar letras para o formato esperado
            processed_lyrics = []
            for lyric in lyrics:
                processed_lyrics.append({
                    'time': lyric['start_time'],
                    'text': lyric['text']
                })
            
            # Montar resposta
            result = {
                'song_id': song_id,
                'title': song['title'],
                'artist': song['artist'],
                'lyrics': processed_lyrics,
                'chords': processed_chords
            }
            
            cursor.close()
            connection.close()
            
            return result
        
        except Error as e:
            print(f"Erro ao obter música do banco de dados: {e}")
            return None
    
    return None

from flask import Flask
from flask_cors import CORS
import backend.config as config
import os
import json
import psycopg2
from psycopg2 import sql, extras

def create_db_connection():
    try:
        connection = psycopg2.connect(
            host=config.DB_CONFIG['dpg-d03kh9idbo4c738frj3g-a'],
            user=config.DB_CONFIG['kplay_v2_user'],
            password=config.DB_CONFIG['5z1XDigq8UyDvtZbyKCLXMXWSE12gnpp'],
            database=config.DB_CONFIG['kplay_v2']
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def create_tables():
    """Cria as tabelas necessárias no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                midi_path VARCHAR(255) NOT NULL,
                lyrics_path VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS lyrics (
                id SERIAL PRIMARY KEY,
                song_id INT NOT NULL,
                text TEXT NOT NULL,
                start_time INT NOT NULL,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chords (
                id SERIAL PRIMARY KEY,
                song_id INT NOT NULL,
                chord_name VARCHAR(50) NOT NULL,
                start_time INT NOT NULL,
                components TEXT,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            )
            """)

            connection.commit()
            cursor.close()
            connection.close()
            print("Tabelas criadas com sucesso.")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            connection.close()

def init_app():
    """Inicializa a aplicação Flask"""
    app = Flask(__name__)
    CORS(app)
    
    app.config['UPLOAD_FOLDER'] = config.DATA_DIR
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    
    return app

def save_song_to_db(title, artist, midi_path, lyrics_path):
    """Salva informações da música no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO songs (title, artist, midi_path, lyrics_path)
            VALUES (%s, %s, %s, %s)
            """
            values = (title, artist, midi_path, lyrics_path)
            cursor.execute(query, values)

            # Pega o último ID inserido
            cursor.execute("SELECT LASTVAL()")
            song_id = cursor.fetchone()[0]

            connection.commit()
            cursor.close()
            connection.close()
            return song_id
        except Exception as e:
            print(f"Erro ao salvar música no banco de dados: {e}")
            connection.close()
            return None
    return None

def save_lyrics_to_db(song_id, lyrics_data):
    """Salva as linhas da letra no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
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
        except Exception as e:
            print(f"Erro ao salvar letras no banco de dados: {e}")
            connection.close()
            return False
    return False

def save_chords_to_db(song_id, chords_data):
    """Salva os acordes no banco de dados"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
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
        except Exception as e:
            print(f"Erro ao salvar acordes no banco de dados: {e}")
            connection.close()
            return False
    return False

def get_song_by_id(song_id):
    """Obtém informações de uma música pelo ID"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("SELECT * FROM songs WHERE id = %s", (song_id,))
            song = cursor.fetchone()
            if not song:
                cursor.close()
                connection.close()
                return None

            cursor.execute("""
                SELECT text, start_time FROM lyrics
                WHERE song_id = %s
                ORDER BY start_time
            """, (song_id,))
            lyrics = cursor.fetchall()

            cursor.execute("""
                SELECT chord_name, start_time, components FROM chords
                WHERE song_id = %s
                ORDER BY start_time
            """, (song_id,))
            chords = cursor.fetchall()

            processed_lyrics = [
                {'time': lyric['start_time'], 'text': lyric['text']} for lyric in lyrics
            ]

            processed_chords = [
                {
                    'time': chord['start_time'],
                    'chord': chord['chord_name'],
                    'components': json.loads(chord['components']) if chord['components'] else []
                }
                for chord in chords
            ]

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
        except Exception as e:
            print(f"Erro ao obter música do banco de dados: {e}")
            connection.close()
            return None
    return None

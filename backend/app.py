from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import json
from music21 import converter, chord
from pychord import Chord
import backend.database as database
import config

# Inicializar a aplicação Flask
app = Flask(__name__)
CORS(app)

# Configurações da aplicação
app.config['UPLOAD_FOLDER'] = config.DATA_DIR
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

@app.route('/api/upload_song', methods=['POST'])
def upload_song():
    """
    Endpoint para upload de arquivos MIDI e letras
    Recebe: arquivos 'midi' e 'lyrics' via multipart/form-data, e metadados 'title' e 'artist'
    Retorna: JSON com caminhos dos arquivos salvos e ID da música
    """
    if 'midi' not in request.files or 'lyrics' not in request.files:
        return jsonify({'error': 'Arquivos MIDI e letra são obrigatórios'}), 400
    
    midi_file = request.files['midi']
    lyrics_file = request.files['lyrics']
    
    # Obter metadados
    title = request.form.get('title', 'Sem título')
    artist = request.form.get('artist', 'Desconhecido')
    
    # Verificar se os arquivos são válidos
    if midi_file.filename == '' or lyrics_file.filename == '':
        return jsonify({'error': 'Nomes de arquivos inválidos'}), 400
    
    if not allowed_file(midi_file.filename, config.ALLOWED_EXTENSIONS['midi']):
        return jsonify({'error': 'Formato de arquivo MIDI não permitido'}), 400
    
    if not allowed_file(lyrics_file.filename, config.ALLOWED_EXTENSIONS['lyrics']):
        return jsonify({'error': 'Formato de arquivo de letra não permitido'}), 400
    
    # Salvar os arquivos
    midi_filename = secure_filename(midi_file.filename)
    lyrics_filename = secure_filename(lyrics_file.filename)
    
    # Usar o mesmo nome base para ambos os arquivos
    base_name = os.path.splitext(midi_filename)[0]
    
    midi_path = os.path.join(config.MIDI_FOLDER, f"{base_name}.mid")
    lyrics_path = os.path.join(config.LYRICS_FOLDER, f"{base_name}.txt")
    
    midi_file.save(midi_path)
    lyrics_file.save(lyrics_path)
    
    # Salvar no banco de dados
    song_id = database.save_song_to_db(title, artist, midi_path, lyrics_path)
    
    if not song_id:
        return jsonify({'error': 'Erro ao salvar música no banco de dados'}), 500
    
    return jsonify({
        'success': True,
        'midi_path': midi_path,
        'lyrics_path': lyrics_path,
        'song_id': song_id
    })

@app.route('/api/generate_chords', methods=['POST'])
def generate_chords():
    """
    Endpoint para extrair acordes de um arquivo MIDI
    Recebe: JSON com 'song_id' ou 'midi_path'
    Retorna: JSON com acordes extraídos e seus timestamps
    """
    data = request.json
    
    if not data:
        return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
    
    # Obter o caminho do arquivo MIDI
    midi_path = None
    song_id = None
    
    if 'midi_path' in data:
        midi_path = data['midi_path']
    elif 'song_id' in data:
        song_id = data['song_id']
        # Obter informações da música do banco de dados
        song_data = database.get_song_by_id(song_id)
        if song_data:
            midi_path = song_data.get('midi_path')
        else:
            return jsonify({'error': f'Música não encontrada com ID: {song_id}'}), 404
    else:
        return jsonify({'error': 'midi_path ou song_id é obrigatório'}), 400
    
    if not os.path.exists(midi_path):
        return jsonify({'error': f'Arquivo MIDI não encontrado: {midi_path}'}), 404
    
    try:
        # Extrair acordes do arquivo MIDI
        chords_data = extract_chords_from_midi(midi_path)
        
        # Salvar os acordes extraídos
        file_base_name = os.path.splitext(os.path.basename(midi_path))[0]
        chords_path = os.path.join(config.CHORDS_FOLDER, f"{file_base_name}.json")
        
        with open(chords_path, 'w') as f:
            json.dump(chords_data, f)
        
        # Salvar acordes no banco de dados se tiver song_id
        if song_id:
            database.save_chords_to_db(song_id, chords_data)
        
        return jsonify({
            'success': True,
            'chords': chords_data,
            'chords_path': chords_path
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao extrair acordes: {str(e)}'}), 500

@app.route('/api/get_song_data', methods=['GET'])
def get_song_data():
    """
    Endpoint para obter dados completos de uma música (letra + acordes)
    Recebe: Parâmetro 'id' na URL
    Retorna: JSON com letra e acordes sincronizados
    """
    song_id = request.args.get('id')
    
    if not song_id:
        return jsonify({'error': 'ID da música é obrigatório'}), 400
    
    # Obter dados do banco de dados
    song_data = database.get_song_by_id(song_id)
    
    if song_data:
        return jsonify(song_data)
    
    # Se não encontrou no banco, tentar ler dos arquivos
    lyrics_path = os.path.join(config.LYRICS_FOLDER, f"{song_id}.txt")
    chords_path = os.path.join(config.CHORDS_FOLDER, f"{song_id}.json")
    
    if not os.path.exists(lyrics_path):
        return jsonify({'error': f'Arquivo de letra não encontrado para o ID: {song_id}'}), 404
    
    if not os.path.exists(chords_path):
        return jsonify({'error': f'Arquivo de acordes não encontrado para o ID: {song_id}'}), 404
    
    try:
        # Ler o arquivo de letra
        with open(lyrics_path, 'r') as f:
            lyrics_content = f.readlines()
        
        # Processar as linhas da letra com timestamps
        lyrics_data = []
        for line in lyrics_content:
            line = line.strip()
            if line:
                # Verificar se a linha tem formato de timestamp [00:00:00]
                if line.startswith('[') and ']' in line:
                    time_str = line[1:line.index(']')]
                    text = line[line.index(']')+1:].strip()
                    
                    # Converter timestamp para milissegundos
                    try:
                        parts = time_str.split(':')
                        if len(parts) == 3:  # hh:mm:ss
                            hours, minutes, seconds = map(float, parts)
                            time_ms = int((hours * 3600 + minutes * 60 + seconds) * 1000)
                        elif len(parts) == 2:  # mm:ss
                            minutes, seconds = map(float, parts)
                            time_ms = int((minutes * 60 + seconds) * 1000)
                        else:
                            time_ms = 0
                        
                        lyrics_data.append({
                            'time': time_ms,
                            'text': text
                        })
                    except:
                        # Se falhar na conversão, adicionar com tempo 0
                        lyrics_data.append({
                            'time': 0,
                            'text': line
                        })
                else:
                    # Linha sem timestamp, adicionar com tempo 0
                    lyrics_data.append({
                        'time': 0,
                        'text': line
                    })
        
        # Ler o arquivo de acordes
        with open(chords_path, 'r') as f:
            chords_data = json.load(f)
        
        # Ordenar os dados por tempo
        lyrics_data.sort(key=lambda x: x['time'])
        
        # Montar resposta
        response = {
            'song_id': song_id,
            'title': 'Desconhecido',  # Não temos essa informação nos arquivos
            'artist': 'Desconhecido',  # Não temos essa informação nos arquivos
            'lyrics': lyrics_data,
            'chords': chords_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Erro ao processar dados da música: {str(e)}'}), 500

@app.route('/api/songs', methods=['GET'])
def get_songs():
    """
    Endpoint para listar todas as músicas disponíveis
    Retorna: JSON com lista de músicas
    """
    # Implementar busca no banco de dados
    # Por enquanto, retornar lista vazia
    return jsonify([])

def allowed_file(filename, allowed_extensions):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_chords_from_midi(midi_path):
    """
    Função para extrair acordes de um arquivo MIDI
    Retorna: Lista de dicionários com nome do acorde e timestamp
    """
    # Carregar o arquivo MIDI com music21
    midi = converter.parse(midi_path)
    
    # Lista para armazenar os acordes extraídos
    extracted_chords = []
    
    # Extrair todos os elementos que são acordes
    for element in midi.recurse():
        if isinstance(element, chord.Chord):
            # Obter o tempo em milissegundos
            time_in_ms = int(element.offset * 1000)  # Converter para milissegundos
            
            try:
                # Obter a nota raiz e a qualidade do acorde
                root = element.root().name
                quality = element.quality
                
                # Formatar o símbolo do acorde
                if quality == 'major':
                    symbol = root
                elif quality == 'minor':
                    symbol = f"{root}m"
                else:
                    # Tentar criar um símbolo mais genérico
                    symbol = f"{root}{quality[0] if quality else ''}"
                
                # Criar objeto Chord para validar e obter componentes
                try:
                    ch = Chord(symbol)
                    components = ch.components()
                    
                    # Adicionar à lista de acordes extraídos
                    extracted_chords.append({
                        'time': time_in_ms,
                        'chord': symbol,
                        'components': components
                    })
                except:
                    # Se falhar ao criar o objeto Chord, usar apenas o símbolo básico
                    extracted_chords.append({
                        'time': time_in_ms,
                        'chord': symbol,
                        'components': []
                    })
            
            except Exception as e:
                # Se houver erro na extração, registrar o tempo e um acorde genérico
                extracted_chords.append({
                    'time': time_in_ms,
                    'chord': 'N/C',  # No Chord
                    'components': []
                })
    
    # Ordenar os acordes por tempo
    extracted_chords.sort(key=lambda x: x['time'])
    
    return extracted_chords
from flask import send_from_directory
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../frontend/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../frontend/js', filename)


if __name__ == '__main__':
    # Criar banco de dados e tabelas se não existirem
    database.create_database_if_not_exists()
    
    # Iniciar a aplicação
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

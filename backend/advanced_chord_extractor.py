import music21
import numpy as np
from collections import Counter
import json
import os

class AdvancedChordExtractor:
    """
    Classe para extração avançada de acordes de arquivos MIDI,
    inspirada nas técnicas do MidiVoyager e Musicca.
    """
    
    def __init__(self, chord_db_path=None):
        """
        Inicializa o extrator de acordes avançado.
        
        Args:
            chord_db_path (str, optional): Caminho para o banco de dados de progressões harmônicas
        """
        self.chord_db_path = chord_db_path
        self.chord_db = self._load_chord_db()
        
        # Configurações para análise de acordes
        self.min_notes_for_chord = 2  # Mínimo de notas para considerar um acorde
        self.time_window = 0.25       # Janela de tempo para agrupar notas (em quartos de nota)
        self.confidence_threshold = 0.6  # Limiar de confiança para identificação de acordes
        
    def _load_chord_db(self):
        """
        Carrega o banco de dados de progressões harmônicas.
        """
        if not self.chord_db_path or not os.path.exists(self.chord_db_path):
            # Banco de dados padrão se nenhum for fornecido
            return {
                "progressions": {
                    "pop": [
                        ["C", "G", "Am", "F"],
                        ["C", "F", "G", "C"],
                        ["C", "Am", "F", "G"]
                    ],
                    "rock": [
                        ["C", "G", "F", "G"],
                        ["Am", "F", "C", "G"],
                        ["D", "A", "G", "A"]
                    ],
                    "jazz": [
                        ["Dm7", "G7", "Cmaj7"],
                        ["Cmaj7", "Am7", "Dm7", "G7"],
                        ["Dm7", "G7", "Cmaj7", "A7", "Dm7", "G7"]
                    ]
                },
                "chord_types": {
                    "major": [0, 4, 7],
                    "minor": [0, 3, 7],
                    "dominant7": [0, 4, 7, 10],
                    "major7": [0, 4, 7, 11],
                    "minor7": [0, 3, 7, 10],
                    "diminished": [0, 3, 6],
                    "augmented": [0, 4, 8],
                    "sus4": [0, 5, 7],
                    "sus2": [0, 2, 7]
                }
            }
        
        try:
            with open(self.chord_db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar banco de dados de acordes: {e}")
            return {}
    
    def extract_chords(self, midi_file_path):
        """
        Extrai acordes de um arquivo MIDI usando técnicas avançadas.
        
        Args:
            midi_file_path (str): Caminho para o arquivo MIDI
            
        Returns:
            list: Lista de acordes extraídos com tempos e durações
        """
        try:
            # Carregar o arquivo MIDI
            midi = music21.converter.parse(midi_file_path)
            
            # Extrair todas as notas
            all_notes = []
            for part in midi.parts:
                for note in part.flat.notes:
                    if isinstance(note, music21.note.Note):
                        all_notes.append({
                            'pitch': note.pitch.midi,
                            'start': note.offset,
                            'duration': note.duration.quarterLength,
                            'end': note.offset + note.duration.quarterLength
                        })
                    elif isinstance(note, music21.chord.Chord):
                        for pitch in note.pitches:
                            all_notes.append({
                                'pitch': pitch.midi,
                                'start': note.offset,
                                'duration': note.duration.quarterLength,
                                'end': note.offset + note.duration.quarterLength
                            })
            
            # Ordenar notas por tempo de início
            all_notes.sort(key=lambda x: x['start'])
            
            # Encontrar todos os tempos únicos onde acordes podem começar ou terminar
            unique_times = sorted(list(set([note['start'] for note in all_notes] + 
                                          [note['end'] for note in all_notes])))
            
            # Extrair acordes em cada janela de tempo
            chords = []
            for i in range(len(unique_times) - 1):
                start_time = unique_times[i]
                end_time = unique_times[i+1]
                
                # Pular janelas muito pequenas
                if end_time - start_time < self.time_window:
                    continue
                
                # Encontrar notas ativas nesta janela de tempo
                active_notes = []
                for note in all_notes:
                    if note['start'] <= start_time and note['end'] > start_time:
                        active_notes.append(note['pitch'])
                
                # Remover duplicatas e ordenar
                active_notes = sorted(list(set(active_notes)))
                
                # Pular se não houver notas suficientes para um acorde
                if len(active_notes) < self.min_notes_for_chord:
                    continue
                
                # Identificar o acorde
                chord_info = self._identify_chord(active_notes)
                if chord_info:
                    chord_info['start'] = start_time
                    chord_info['end'] = end_time
                    chord_info['duration'] = end_time - start_time
                    chords.append(chord_info)
            
            # Pós-processamento: combinar acordes idênticos consecutivos
            combined_chords = self._combine_consecutive_chords(chords)
            
            # Pós-processamento: aplicar conhecimento de progressões harmônicas
            refined_chords = self._refine_with_progressions(combined_chords)
            
            return refined_chords
            
        except Exception as e:
            print(f"Erro ao extrair acordes: {e}")
            return []
    
    def _identify_chord(self, pitches):
        """
        Identifica o acorde a partir de um conjunto de notas MIDI.
        
        Args:
            pitches (list): Lista de valores MIDI das notas
            
        Returns:
            dict: Informações sobre o acorde identificado
        """
        if not pitches or len(pitches) < self.min_notes_for_chord:
            return None
        
        # Converter pitches MIDI para classes de altura (0-11)
        pitch_classes = [p % 12 for p in pitches]
        pitch_classes = sorted(list(set(pitch_classes)))  # Remover duplicatas
        
        # Tentar todas as possíveis notas fundamentais
        best_match = None
        best_score = -1
        
        for root in range(12):
            # Normalizar para que a fundamental seja 0
            normalized = [(pc - root) % 12 for pc in pitch_classes]
            normalized.sort()
            
            # Verificar correspondência com cada tipo de acorde
            for chord_type, intervals in self.chord_db.get("chord_types", {}).items():
                # Calcular pontuação de correspondência
                score = self._calculate_match_score(normalized, intervals)
                
                if score > best_score and score >= self.confidence_threshold:
                    best_score = score
                    root_note = music21.pitch.Pitch(midi=root).name
                    best_match = {
                        'root': root_note,
                        'type': chord_type,
                        'name': self._format_chord_name(root_note, chord_type),
                        'notes': [music21.pitch.Pitch(midi=p).name for p in pitches],
                        'confidence': score
                    }
        
        return best_match
    
    def _calculate_match_score(self, normalized_pitches, chord_intervals):
        """
        Calcula a pontuação de correspondência entre um conjunto de notas e um tipo de acorde.
        
        Args:
            normalized_pitches (list): Classes de altura normalizadas (0-11)
            chord_intervals (list): Intervalos que definem o tipo de acorde
            
        Returns:
            float: Pontuação de correspondência (0-1)
        """
        # Contar quantos intervalos do acorde estão presentes
        matches = sum(1 for interval in chord_intervals if interval in normalized_pitches)
        
        # Contar quantas notas não pertencem ao acorde
        non_chord_tones = sum(1 for pitch in normalized_pitches if pitch not in chord_intervals)
        
        # Calcular pontuação
        if len(chord_intervals) == 0:
            return 0
        
        # Fórmula de pontuação: prioriza correspondência de intervalos e penaliza notas estranhas
        score = (matches / len(chord_intervals)) - (0.2 * non_chord_tones / len(normalized_pitches))
        
        return max(0, min(1, score))  # Limitar entre 0 e 1
    
    def _format_chord_name(self, root, chord_type):
        """
        Formata o nome do acorde com base na fundamental e no tipo.
        
        Args:
            root (str): Nome da nota fundamental
            chord_type (str): Tipo de acorde
            
        Returns:
            str: Nome formatado do acorde
        """
        # Mapeamento de tipos de acorde para símbolos
        type_symbols = {
            "major": "",
            "minor": "m",
            "dominant7": "7",
            "major7": "maj7",
            "minor7": "m7",
            "diminished": "dim",
            "augmented": "aug",
            "sus4": "sus4",
            "sus2": "sus2"
        }
        
        return root + type_symbols.get(chord_type, "")
    
    def _combine_consecutive_chords(self, chords):
        """
        Combina acordes idênticos consecutivos.
        
        Args:
            chords (list): Lista de acordes extraídos
            
        Returns:
            list: Lista de acordes combinados
        """
        if not chords:
            return []
        
        combined = [chords[0]]
        
        for i in range(1, len(chords)):
            current = chords[i]
            previous = combined[-1]
            
            # Se o acorde atual é o mesmo que o anterior, estenda a duração
            if (current['name'] == previous['name'] and 
                abs(current['start'] - previous['end']) < 0.01):  # Pequena tolerância
                previous['end'] = current['end']
                previous['duration'] = previous['end'] - previous['start']
            else:
                combined.append(current)
        
        return combined
    
    def _refine_with_progressions(self, chords):
        """
        Refina a detecção de acordes usando conhecimento de progressões harmônicas.
        
        Args:
            chords (list): Lista de acordes extraídos
            
        Returns:
            list: Lista de acordes refinados
        """
        if not chords or len(chords) < 2:
            return chords
        
        # Extrair apenas os nomes dos acordes
        chord_names = [chord['name'] for chord in chords]
        
        # Verificar se a progressão corresponde a alguma progressão conhecida
        progressions = self.chord_db.get("progressions", {})
        all_progressions = []
        for genre, genre_progressions in progressions.items():
            all_progressions.extend(genre_progressions)
        
        # Verificar correspondências parciais com progressões conhecidas
        for i in range(len(chord_names) - 1):
            for progression in all_progressions:
                if len(progression) >= 2:
                    for j in range(len(progression) - 1):
                        # Se dois acordes consecutivos correspondem a uma progressão conhecida
                        if (chord_names[i].startswith(progression[j]) and 
                            chord_names[i+1].startswith(progression[j+1])):
                            # Aumentar a confiança desses acordes
                            chords[i]['confidence'] = min(1.0, chords[i]['confidence'] + 0.1)
                            chords[i+1]['confidence'] = min(1.0, chords[i+1]['confidence'] + 0.1)
        
        return chords
    
    def analyze_key(self, chords):
        """
        Analisa a tonalidade provável com base nos acordes extraídos.
        
        Args:
            chords (list): Lista de acordes extraídos
            
        Returns:
            dict: Informações sobre a tonalidade
        """
        if not chords:
            return {"key": "Indeterminado", "confidence": 0}
        
        # Extrair apenas os nomes dos acordes
        chord_names = [chord['name'] for chord in chords]
        
        # Mapear tonalidades e seus acordes diatônicos
        key_signatures = {
            "C maior": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
            "G maior": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
            "D maior": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
            "A maior": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
            "E maior": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
            "B maior": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
            "F# maior": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
            "C# maior": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
            "F maior": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
            "Bb maior": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
            "Eb maior": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
            "Ab maior": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
            "Db maior": ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
            "Gb maior": ["Gb", "Abm", "Bbm", "Cb", "Db", "Ebm", "Fdim"],
            "A menor": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
            "E menor": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
            "B menor": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
            "F# menor": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
            "C# menor": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
            "G# menor": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
            "D# menor": ["D#m", "E#dim", "F#", "G#m", "A#m", "B", "C#"],
            "A# menor": ["A#m", "B#dim", "C#", "D#m", "E#m", "F#", "G#"],
            "D menor": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
            "G menor": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
            "C menor": ["Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"],
            "F menor": ["Fm", "Gdim", "Ab", "Bbm", "Cm", "Db", "Eb"],
            "Bb menor": ["Bbm", "Cdim", "Db", "Ebm", "Fm", "Gb", "Ab"],
            "Eb menor": ["Ebm", "Fdim", "Gb", "Abm", "Bbm", "Cb", "Db"]
        }
        
        # Contar correspondências para cada tonalidade
        key_matches = {}
        for key, key_chords in key_signatures.items():
            matches = 0
            for chord in chord_names:
                # Verificar se o acorde está na tonalidade (considerando apenas a tríade básica)
                chord_root = chord[0]  # Primeira letra do nome do acorde
                if len(chord) > 1 and chord[1] in ['#', 'b']:
                    chord_root += chord[1]
                
                chord_type = chord[len(chord_root):]  # Tipo de acorde (m, 7, etc.)
                
                # Verificar se o acorde básico está na tonalidade
                for key_chord in key_chords:
                    if key_chord.startswith(chord_root):
                        # Verificar compatibilidade de tipo
                        if ('m' in key_chord and 'm' in chord_type) or ('dim' in key_chord and 'dim' in chord_type) or \
                           ('m' not in key_chord and 'dim' not in key_chord and 'm' not in cho
(Content truncated due to size limit. Use line ranges to read in chunks)
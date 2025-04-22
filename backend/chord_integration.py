import requests
from bs4 import BeautifulSoup
import json

class MusiccaIntegration:
    """
    Classe para integração com o site Musicca para extração de acordes e progressões harmônicas.
    """
    
    def __init__(self):
        self.base_url = "https://www.musicca.com/pt"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Banco de dados de progressões harmônicas comuns por gênero
        self.chord_progressions = {
            "pop": [
                ["C", "G", "Am", "F"],
                ["C", "F", "G", "C"],
                ["C", "F", "Gsus4", "G"],
                ["C", "Am", "Dm", "G"],
                ["C", "Dm", "F", "G"],
                ["C", "G/B", "Am", "G"],
                ["Am", "Dm", "E", "Am"],
                ["Am", "C", "Dm", "Em"]
            ],
            "rock": [
                ["C", "Am", "F", "G"],
                ["C", "F", "C", "G"],
                ["C", "C", "Eb", "F"],
                ["C", "E", "F", "Fm"],
                ["Dm", "C", "G", "Bb"],
                ["G", "G", "F", "C"],
                ["Am", "F", "C", "G"],
                ["Am", "E7", "D", "G7"]
            ],
            "jazz": [
                ["Dm7", "G7", "CΔ", "CΔ"],
                ["Dm7", "G7", "CΔ", "A7"],
                ["CΔ", "Am7", "Dm7", "G7"],
                ["CΔ", "C♯o7", "Dm7", "G7"],
                ["CΔ", "C7", "FΔ", "Fm7"],
                ["Am7(♭5)", "Dm7", "G7", "CΔ"],
                ["Dm7(♭5)", "G7", "Cm7", "Cm7"],
                ["Cm7", "G7", "Cm7", "G7"]
            ],
            "blues": [
                ["C7", "C7", "C7", "C7", "F7", "F7", "C7", "C7", "G7", "F7", "C7", "C7"]
            ]
        }
        
    def get_chord_progressions(self, genre):
        """
        Retorna progressões harmônicas comuns para um gênero específico.
        
        Args:
            genre (str): O gênero musical (pop, rock, jazz, blues)
            
        Returns:
            list: Lista de progressões harmônicas para o gênero
        """
        genre = genre.lower()
        if genre in self.chord_progressions:
            return self.chord_progressions[genre]
        else:
            return []
    
    def fetch_chord_data(self, chord_name):
        """
        Busca informações sobre um acorde específico do Musicca.
        
        Args:
            chord_name (str): Nome do acorde (ex: "C", "Dm7", "G7")
            
        Returns:
            dict: Informações sobre o acorde
        """
        try:
            # Esta é uma implementação simulada, pois o site não tem uma API pública
            # Em uma implementação real, seria necessário fazer web scraping
            chord_data = {
                "name": chord_name,
                "notes": self._get_chord_notes(chord_name),
                "intervals": self._get_chord_intervals(chord_name),
                "type": self._get_chord_type(chord_name)
            }
            return chord_data
        except Exception as e:
            print(f"Erro ao buscar dados do acorde {chord_name}: {str(e)}")
            return None
    
    def _get_chord_notes(self, chord_name):
        """
        Retorna as notas de um acorde com base no nome.
        Implementação simplificada para demonstração.
        """
        # Dicionário de notas básicas
        chord_notes = {
            "C": ["C", "E", "G"],
            "Cm": ["C", "Eb", "G"],
            "C7": ["C", "E", "G", "Bb"],
            "Cm7": ["C", "Eb", "G", "Bb"],
            "CΔ": ["C", "E", "G", "B"],
            "D": ["D", "F#", "A"],
            "Dm": ["D", "F", "A"],
            "D7": ["D", "F#", "A", "C"],
            "Dm7": ["D", "F", "A", "C"],
            "E": ["E", "G#", "B"],
            "Em": ["E", "G", "B"],
            "E7": ["E", "G#", "B", "D"],
            "F": ["F", "A", "C"],
            "Fm": ["F", "Ab", "C"],
            "F7": ["F", "A", "C", "Eb"],
            "G": ["G", "B", "D"],
            "Gm": ["G", "Bb", "D"],
            "G7": ["G", "B", "D", "F"],
            "A": ["A", "C#", "E"],
            "Am": ["A", "C", "E"],
            "A7": ["A", "C#", "E", "G"],
            "Am7": ["A", "C", "E", "G"],
            "B": ["B", "D#", "F#"],
            "Bm": ["B", "D", "F#"],
            "B7": ["B", "D#", "F#", "A"]
        }
        
        if chord_name in chord_notes:
            return chord_notes[chord_name]
        else:
            # Retorna um acorde genérico se não encontrado
            return ["?"]
    
    def _get_chord_intervals(self, chord_name):
        """
        Retorna os intervalos de um acorde com base no nome.
        Implementação simplificada para demonstração.
        """
        chord_intervals = {
            # Tríades
            "C": ["1", "3", "5"],
            "Cm": ["1", "b3", "5"],
            "Csus4": ["1", "4", "5"],
            "Caug": ["1", "3", "#5"],
            "Cdim": ["1", "b3", "b5"],
            
            # Tétrades
            "C7": ["1", "3", "5", "b7"],
            "Cm7": ["1", "b3", "5", "b7"],
            "CΔ": ["1", "3", "5", "7"],
            "Cm7(b5)": ["1", "b3", "b5", "b7"],
            "C7sus4": ["1", "4", "5", "b7"],
            "C6": ["1", "3", "5", "6"]
        }
        
        # Extrai o tipo de acorde do nome
        chord_type = self._get_chord_type(chord_name)
        root_note = chord_name[0]
        if len(chord_name) > 1 and chord_name[1] in ["#", "b"]:
            root_note += chord_name[1]
        
        # Constrói o nome do acorde genérico (C + tipo)
        generic_chord = "C" + chord_name[len(root_note):]
        
        if generic_chord in chord_intervals:
            return chord_intervals[generic_chord]
        else:
            # Retorna intervalos genéricos se não encontrado
            return ["?"]
    
    def _get_chord_type(self, chord_name):
        """
        Determina o tipo de acorde com base no nome.
        """
        if "m7(b5)" in chord_name or "m7(♭5)" in chord_name:
            return "meio-diminuto"
        elif "m7" in chord_name:
            return "menor com sétima"
        elif "Δ" in chord_name or "maj7" in chord_name:
            return "maior com sétima maior"
        elif "7" in chord_name:
            return "dominante"
        elif "dim" in chord_name or "o" in chord_name:
            return "diminuto"
        elif "aug" in chord_name or "+" in chord_name:
            return "aumentado"
        elif "sus4" in chord_name:
            return "suspenso"
        elif "m" in chord_name:
            return "menor"
        else:
            return "maior"
    
    def suggest_chord_progression(self, midi_chords, genre=None):
        """
        Sugere uma progressão harmônica com base nos acordes extraídos do MIDI.
        
        Args:
            midi_chords (list): Lista de acordes extraídos do arquivo MIDI
            genre (str, optional): Gênero musical para sugestões específicas
            
        Returns:
            dict: Sugestões de progressões harmônicas
        """
        suggestions = {
            "original": midi_chords,
            "suggestions": []
        }
        
        # Se o gênero for especificado, busca progressões daquele gênero
        if genre and genre.lower() in self.chord_progressions:
            suggestions["suggestions"].extend(self.chord_progressions[genre.lower()])
        else:
            # Caso contrário, sugere progressões de todos os gêneros
            for genre_progressions in self.chord_progressions.values():
                suggestions["suggestions"].extend(genre_progressions)
        
        # Limita a 5 sugestões para não sobrecarregar
        suggestions["suggestions"] = suggestions["suggestions"][:5]
        
        return suggestions


class MidiVoyagerIntegration:
    """
    Classe para integração com o MidiVoyager para extração de acordes de arquivos MIDI.
    Esta é uma implementação simulada, já que não temos acesso direto ao MidiVoyager.
    """
    
    def __init__(self):
        self.chord_detection_enabled = True
    
    def extract_chords_from_midi(self, midi_file_path):
        """
        Simula a extração de acordes de um arquivo MIDI usando técnicas similares ao MidiVoyager.
        
        Args:
            midi_file_path (str): Caminho para o arquivo MIDI
            
        Returns:
            list: Lista de acordes extraídos com seus tempos
        """
        try:
            # Em uma implementação real, usaríamos bibliotecas como music21 ou mido
            # para analisar o arquivo MIDI e extrair os acordes
            
            # Esta é uma implementação simulada para demonstração
            from music21 import converter, chord, note
            
            # Carrega o arquivo MIDI
            midi_data = converter.parse(midi_file_path)
            
            # Lista para armazenar os acordes extraídos
            extracted_chords = []
            
            # Itera pelas partes do MIDI
            for part in midi_data.parts:
                # Itera pelos compassos
                for measure in part.getElementsByClass('Measure'):
                    # Itera pelos elementos do compasso
                    for element in measure.notes:
                        # Se for um acorde
                        if isinstance(element, chord.Chord):
                            # Obtém o nome do acorde
                            chord_name = element.commonName
                            # Obtém o tempo do acorde
                            offset = element.offset
                            # Adiciona à lista de acordes extraídos
                            extracted_chords.append({
                                "name": chord_name,
                                "time": offset,
                                "duration": element.duration.quarterLength
                            })
                        # Se for uma nota (pode ser parte de um acorde implícito)
                        elif isinstance(element, note.Note):
                            # Adiciona à lista como uma nota individual
                            extracted_chords.append({
                                "name": element.name,
                                "time": element.offset,
                                "duration": element.duration.quarterLength,
                                "is_note": True
                            })
            
            return extracted_chords
            
        except Exception as e:
            print(f"Erro ao extrair acordes do arquivo MIDI: {str(e)}")
            return []
    
    def analyze_chord_progression(self, chord_list):
        """
        Analisa uma progressão de acordes para identificar padrões comuns.
        
        Args:
            chord_list (list): Lista de acordes extraídos
            
        Returns:
            dict: Análise da progressão de acordes
        """
        # Implementação simulada
        analysis = {
            "chord_count": len(chord_list),
            "unique_chords": len(set([c["name"] for c in chord_list if "name" in c])),
            "possible_key": self._determine_possible_key(chord_list),
            "common_patterns": self._find_common_patterns(chord_list)
        }
        
        return analysis
    
    def _determine_possible_key(self, chord_list):
        """
        Tenta determinar a tonalidade da música com base nos acordes.
        Implementação simplificada para demonstração.
        """
        # Em uma implementação real, usaríamos algoritmos mais sofisticados
        # Esta é uma implementação muito simplificada
        
        # Extrai apenas os nomes dos acordes
        chord_names = [c["name"] for c in chord_list if "name" in c]
        
        # Dicionário de tonalidades comuns e seus acordes
        key_signatures = {
            "C maior": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
            "G maior": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
            "D maior": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
            "A maior": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
            "E maior": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
            "Am menor": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
            "Em menor": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"]
        }
        
        # Conta quantos acordes de cada tonalidade estão presentes
        key_matches = {}
        for key, key_chords in key_signatures.items():
            matches = sum(1 for chord in chord_names if any(chord.startswith(kc) for kc in key_chords))
            key_matches[key] = matches
        
        # Retorna a tonalidade com mais correspondências
        if key_matches:
            return max(key_matches.items(), key=lambda x: x[1])[0]
        else:
            return "Indeterminado"
    
    def _find_common_patterns(self, chord_list):
        """
        Identifica padrões comuns na progressão de acordes.
        Implementação simplificada para demonstração.
        """
        # Extrai apenas os nomes dos acordes
        chord_names = [c["name"] for c in chord_list if "name" in c]
        
        # Padrões comuns a procurar
        common_patterns = {
            "I-IV-V": ["C-F-G", "G-C-D", "D-G-A", "A-D-E"],
            "I-V-vi-IV": ["C-G-Am-F", "G-D-Em-C", "D-A-Bm-G"],
            "ii-V-I": ["Dm-G-C", "Am-D-G", "Em-A-D"],
            "I-vi-IV-V": ["C-Am-F-G", "G-Em-C-D", "D-Bm-G-A"],
            "12-bar blues": ["C7-C7-C7-C7-F7-F7-C7-C7-G7-F7-C7-C7"]
        }
        
        # Converte a lista de acordes em uma string para facilitar a busca
        chord_string = "-".join(chord_names)
        
        # Procura por padrões
        found_patterns = []
        for pattern_name, pattern_examples in common_patterns.items():
            for example in pattern_examples:
                if example in chord_string:
                    found_patterns.append(pattern_name)
                    break
        
        return found_patterns if found_patterns else ["Nenhum padrão comum identificado"]


# Exemplo de uso
if __name__ == "__main__":
    # Integração com Musicca
    musicca = MusiccaIntegration()
    
    # Obtém progressões harmônicas para pop
    pop_progressions = musicca.get_chord_progressions("pop")
    print("Progressões de Pop:", pop_progressions)
    
    # Obtém informações sobre um acorde
    c_major_info = musicca.fetch_chord_data("C")
    print("Informações do acorde C:", c_major_info)
    
    # Integração com MidiVoyager
    midi_voyager = MidiVoyagerIntegration()
    
    # Exemplo de extração de acordes (simulado)
    # Em um caso real, você forneceria o caminho para um arquivo MIDI
    extracted_chords = midi_voyager.extract_chords_from_midi("/home/ubuntu/karaoke-app/data/midi/musica_exemplo.mid")
    print("Acordes extraídos:", extracted_chords)
    
    # Análise da progressão de acordes
    chord_analysis = midi_voyager.analyze_chord_progression(extracted_chords)
    print("Análise da progressão:", chord_analysis)
    
    # Sugestão de progressão harmônica
    chord_suggestions = musicca.suggest_chord_progression(
        [c["name"] for c in extracted_chords if "name" in c], 
        "pop"
    )
    print("Sugestões de progressões:", chord_suggestions)

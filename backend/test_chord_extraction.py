#!/usr/bin/env python3
import os
import json
import sys
from music21 import converter, chord

def test_chord_extraction(midi_path):
    """
    Testa a extração de acordes de um arquivo MIDI
    """
    print(f"Testando extração de acordes do arquivo: {midi_path}")
    
    try:
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
                    
                    # Adicionar à lista de acordes extraídos
                    extracted_chords.append({
                        'time': time_in_ms,
                        'chord': symbol,
                        'notes': [n.nameWithOctave for n in element.notes]
                    })
                
                except Exception as e:
                    print(f"Erro ao processar acorde: {e}")
                    # Se houver erro na extração, registrar o tempo e um acorde genérico
                    extracted_chords.append({
                        'time': time_in_ms,
                        'chord': 'N/C',  # No Chord
                        'notes': []
                    })
        
        # Ordenar os acordes por tempo
        extracted_chords.sort(key=lambda x: x['time'])
        
        # Salvar os acordes extraídos em um arquivo JSON
        output_path = os.path.splitext(midi_path)[0] + "_chords.json"
        with open(output_path, 'w') as f:
            json.dump(extracted_chords, f, indent=2)
        
        print(f"Extração concluída. {len(extracted_chords)} acordes encontrados.")
        print(f"Acordes salvos em: {output_path}")
        
        # Exibir os primeiros 5 acordes (ou todos, se houver menos)
        print("\nPrimeiros acordes extraídos:")
        for i, chord_data in enumerate(extracted_chords[:5]):
            print(f"{i+1}. Tempo: {chord_data['time']}ms, Acorde: {chord_data['chord']}, Notas: {chord_data['notes']}")
        
        return extracted_chords
    
    except Exception as e:
        print(f"Erro ao extrair acordes: {e}")
        return None

if __name__ == "__main__":
    # Verificar se o caminho do arquivo MIDI foi fornecido
    if len(sys.argv) > 1:
        midi_path = sys.argv[1]
    else:
        # Usar o arquivo de exemplo
        midi_path = "/home/ubuntu/karaoke-app/data/midi/musica_exemplo.mid"
    
    # Testar a extração de acordes
    test_chord_extraction(midi_path)

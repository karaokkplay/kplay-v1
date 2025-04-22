#!/usr/bin/env python3
import os
import json
import sys

def test_lyrics_sync(lyrics_path, chords_path):
    """
    Testa a sincronização entre letras e acordes
    """
    print(f"Testando sincronização entre letras e acordes")
    print(f"Arquivo de letras: {lyrics_path}")
    print(f"Arquivo de acordes: {chords_path}")
    
    try:
        # Carregar o arquivo de letras
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
                    except Exception as e:
                        print(f"Erro ao processar timestamp: {e}")
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
        
        # Carregar o arquivo de acordes
        with open(chords_path, 'r') as f:
            chords_data = json.load(f)
        
        # Ordenar os dados por tempo
        lyrics_data.sort(key=lambda x: x['time'])
        
        # Criar uma simulação de sincronização
        print("\nSimulação de sincronização:")
        
        # Criar uma linha do tempo combinada
        timeline = []
        
        # Adicionar letras à linha do tempo
        for lyric in lyrics_data:
            timeline.append({
                'time': lyric['time'],
                'type': 'lyric',
                'content': lyric['text']
            })
        
        # Adicionar acordes à linha do tempo
        for chord in chords_data:
            timeline.append({
                'time': chord['time'],
                'type': 'chord',
                'content': chord['chord']
            })
        
        # Ordenar a linha do tempo por tempo
        timeline.sort(key=lambda x: x['time'])
        
        # Exibir os primeiros 10 eventos da linha do tempo (ou todos, se houver menos)
        for i, event in enumerate(timeline[:10]):
            event_type = "Letra" if event['type'] == 'lyric' else "Acorde"
            print(f"{i+1}. Tempo: {event['time']}ms, Tipo: {event_type}, Conteúdo: {event['content']}")
        
        # Salvar a linha do tempo em um arquivo JSON
        output_path = os.path.join(os.path.dirname(lyrics_path), "timeline_sync.json")
        with open(output_path, 'w') as f:
            json.dump(timeline, f, indent=2)
        
        print(f"\nLinha do tempo de sincronização salva em: {output_path}")
        print(f"Total de eventos: {len(timeline)} ({len(lyrics_data)} letras, {len(chords_data)} acordes)")
        
        return timeline
    
    except Exception as e:
        print(f"Erro ao testar sincronização: {e}")
        return None

if __name__ == "__main__":
    # Usar os arquivos de exemplo
    lyrics_path = "/home/ubuntu/karaoke-app/data/lyrics/musica_exemplo.txt"
    chords_path = "/home/ubuntu/karaoke-app/data/midi/musica_exemplo_chords.json"
    
    # Testar a sincronização
    test_lyrics_sync(lyrics_path, chords_path)

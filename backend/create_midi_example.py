#!/usr/bin/env python3
from midiutil import MIDIFile
import os

# Criar um arquivo MIDI de exemplo com acordes
def create_example_midi():
    # Criar um objeto MIDI com 1 faixa
    midi = MIDIFile(1)
    
    # Nome da faixa e tempo
    track = 0
    time = 0
    
    # Configurar nome da faixa e tempo
    midi.addTrackName(track, time, "Música Exemplo")
    midi.addTempo(track, time, 120)
    
    # Definir acordes para a música
    # Cada acorde é uma lista de notas MIDI (C=60, D=62, E=64, F=65, G=67, A=69, B=71)
    chords = [
        # C Major (C-E-G)
        [60, 64, 67],
        # G Major (G-B-D)
        [67, 71, 62],
        # A Minor (A-C-E)
        [69, 60, 64],
        # F Major (F-A-C)
        [65, 69, 60],
        
        # Repetir sequência
        [60, 64, 67],
        [67, 71, 62],
        [69, 60, 64],
        [65, 69, 60],
        
        # Variação
        [62, 66, 69],  # D Minor
        [67, 71, 62],  # G Major
        [60, 64, 67],  # C Major
        [65, 69, 60],  # F Major
        
        # Final
        [60, 64, 67],  # C Major
        [67, 71, 62],  # G Major
        [69, 60, 64],  # A Minor
        [60, 64, 67],  # C Major
    ]
    
    # Adicionar acordes ao arquivo MIDI
    # Cada acorde dura 4 tempos (1 compasso em 4/4)
    for i, chord in enumerate(chords):
        # Tempo de início do acorde (em tempos)
        chord_time = i * 4
        
        # Duração do acorde (em tempos)
        duration = 4
        
        # Volume (0-127)
        volume = 100
        
        # Adicionar cada nota do acorde
        for note in chord:
            midi.addNote(track, 0, note, chord_time, duration, volume)
    
    # Caminho para salvar o arquivo
    output_path = "/home/ubuntu/karaoke-app/data/midi/musica_exemplo.mid"
    
    # Salvar o arquivo MIDI
    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)
    
    print(f"Arquivo MIDI criado: {output_path}")
    return output_path

if __name__ == "__main__":
    create_example_midi()

import React, { useState, useEffect, useRef } from 'react';
import './VirtualKeyboard.css';

const VirtualKeyboard = ({ chords, currentChord, onKeyPress }) => {
  const [showNoteNames, setShowNoteNames] = useState(true);
  const [highlightChord, setHighlightChord] = useState(true);
  const [octaves, setOctaves] = useState(2);
  const [startOctave, setStartOctave] = useState(3);
  const keyboardRef = useRef(null);

  // Mapeamento de notas para teclas do teclado do computador (2 oitavas)
  const keyboardMapping = {
    // Primeira oitava - teclas brancas
    'a': { note: 'C', octave: 0 },
    's': { note: 'D', octave: 0 },
    'd': { note: 'E', octave: 0 },
    'f': { note: 'F', octave: 0 },
    'g': { note: 'G', octave: 0 },
    'h': { note: 'A', octave: 0 },
    'j': { note: 'B', octave: 0 },
    // Primeira oitava - teclas pretas
    'w': { note: 'C#', octave: 0 },
    'e': { note: 'D#', octave: 0 },
    't': { note: 'F#', octave: 0 },
    'y': { note: 'G#', octave: 0 },
    'u': { note: 'A#', octave: 0 },
    // Segunda oitava - teclas brancas
    'k': { note: 'C', octave: 1 },
    'l': { note: 'D', octave: 1 },
    ';': { note: 'E', octave: 1 },
    "'": { note: 'F', octave: 1 },
    // Segunda oitava - teclas pretas
    'o': { note: 'C#', octave: 1 },
    'p': { note: 'D#', octave: 1 },
  };

  // Notas do teclado
  const whiteNotes = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
  const blackNotes = ['C#', 'D#', 'F#', 'G#', 'A#'];
  const blackNotePositions = {
    'C#': 1,
    'D#': 2,
    'F#': 4,
    'G#': 5,
    'A#': 6
  };

  // Estado para teclas pressionadas
  const [pressedKeys, setPressedKeys] = useState({});

  // Função para converter nome de acorde em notas
  const chordToNotes = (chordName) => {
    if (!chordName) return [];

    // Extrair a nota raiz e o tipo de acorde
    let rootNote = chordName.charAt(0);
    let chordType = chordName.substring(1);
    
    // Verificar se há um acidente (# ou b)
    if (chordName.length > 1 && (chordName.charAt(1) === '#' || chordName.charAt(1) === 'b')) {
      rootNote += chordName.charAt(1);
      chordType = chordName.substring(2);
    }

    // Mapeamento de notas para índices
    const noteIndices = {
      'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
      'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
      'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    };

    // Mapeamento de tipos de acorde para intervalos
    const chordIntervals = {
      '': [0, 4, 7],                // Maior
      'm': [0, 3, 7],               // Menor
      '7': [0, 4, 7, 10],           // Dominante 7
      'maj7': [0, 4, 7, 11],        // Maior 7
      'm7': [0, 3, 7, 10],          // Menor 7
      'dim': [0, 3, 6],             // Diminuto
      'aug': [0, 4, 8],             // Aumentado
      'sus4': [0, 5, 7],            // Suspenso 4
      '6': [0, 4, 7, 9],            // Sexta
      'm6': [0, 3, 7, 9],           // Menor com sexta
      '9': [0, 4, 7, 10, 14],       // Nona
      'maj9': [0, 4, 7, 11, 14],    // Maior com nona
      'm9': [0, 3, 7, 10, 14],      // Menor com nona
      'add9': [0, 4, 7, 14],        // Adicionada nona
      'm7b5': [0, 3, 6, 10],        // Meio-diminuto
      '7sus4': [0, 5, 7, 10],       // Dominante 7 suspenso
      '7b9': [0, 4, 7, 10, 13],     // Dominante 7 com nona bemol
      '7#9': [0, 4, 7, 10, 15],     // Dominante 7 com nona sustenida
      '13': [0, 4, 7, 10, 14, 21],  // Décima terceira
    };

    // Obter os intervalos para o tipo de acorde
    let intervals = chordIntervals[chordType] || chordIntervals[''];
    
    // Obter o índice da nota raiz
    const rootIndex = noteIndices[rootNote] || 0;
    
    // Calcular as notas do acorde
    return intervals.map(interval => {
      const noteIndex = (rootIndex + interval) % 12;
      const octave = Math.floor((rootIndex + interval) / 12) + startOctave;
      
      // Converter índice de volta para nome de nota
      const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
      return { note: noteNames[noteIndex], octave };
    });
  };

  // Efeito para lidar com eventos de teclado
  useEffect(() => {
    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();
      if (keyboardMapping[key] && !pressedKeys[key]) {
        const { note, octave } = keyboardMapping[key];
        const fullNote = `${note}${startOctave + octave}`;
        
        // Atualizar estado de teclas pressionadas
        setPressedKeys(prev => ({ ...prev, [key]: true }));
        
        // Chamar callback se fornecido
        if (onKeyPress) {
          onKeyPress(fullNote, true);
        }
        
        // Reproduzir som (implementação opcional)
        playNote(note, startOctave + octave);
      }
    };

    const handleKeyUp = (e) => {
      const key = e.key.toLowerCase();
      if (keyboardMapping[key]) {
        const { note, octave } = keyboardMapping[key];
        const fullNote = `${note}${startOctave + octave}`;
        
        // Atualizar estado de teclas pressionadas
        setPressedKeys(prev => {
          const newState = { ...prev };
          delete newState[key];
          return newState;
        });
        
        // Chamar callback se fornecido
        if (onKeyPress) {
          onKeyPress(fullNote, false);
        }
        
        // Parar som (implementação opcional)
        stopNote(note, startOctave + octave);
      }
    };

    // Adicionar event listeners
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // Limpar event listeners
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [pressedKeys, startOctave, onKeyPress]);

  // Função para verificar se uma nota está no acorde atual
  const isNoteInCurrentChord = (note, octave) => {
    if (!currentChord || !highlightChord) return false;
    
    const chordNotes = chordToNotes(currentChord);
    return chordNotes.some(chordNote => 
      chordNote.note === note && (chordNote.octave === octave || chordNote.octave === undefined)
    );
  };

  // Função para verificar se uma tecla está pressionada
  const isKeyPressed = (note, octave) => {
    return Object.keys(pressedKeys).some(key => {
      const keyInfo = keyboardMapping[key];
      return keyInfo && keyInfo.note === note && keyInfo.octave + startOctave === octave;
    });
  };

  // Funções para reproduzir e parar sons (implementação básica)
  const audioContext = useRef(null);
  const oscillators = useRef({});

  const playNote = (note, octave) => {
    try {
      if (!audioContext.current) {
        audioContext.current = new (window.AudioContext || window.webkitAudioContext)();
      }

      const noteFrequencies = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
      };

      const baseFreq = noteFrequencies[note];
      const freq = baseFreq * Math.pow(2, octave - 4);

      const oscillator = audioContext.current.createOscillator();
      const gainNode = audioContext.current.createGain();
      
      oscillator.type = 'sine';
      oscillator.frequency.value = freq;
      
      gainNode.gain.value = 0.3;
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.current.destination);
      
      oscillator.start();
      oscillators.current[`${note}${octave}`] = { oscillator, gainNode };
    } catch (error) {
      console.error('Error playing note:', error);
    }
  };

  const stopNote = (note, octave) => {
    try {
      const key = `${note}${octave}`;
      if (oscillators.current[key]) {
        const { oscillator, gainNode } = oscillators.current[key];
        
        // Fade out para evitar cliques
        gainNode.gain.setValueAtTime(gainNode.gain.value, audioContext.current.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.current.currentTime + 0.03);
        
        // Parar após fade out
        setTimeout(() => {
          oscillator.stop();
          delete oscillators.current[key];
        }, 30);
      }
    } catch (error) {
      console.error('Error stopping note:', error);
    }
  };

  // Renderizar teclas brancas
  const renderWhiteKeys = () => {
    const keys = [];
    
    for (let octave = 0; octave < octaves; octave++) {
      whiteNotes.forEach(note => {
        const octaveNum = startOctave + octave;
        const isInChord = isNoteInCurrentChord(note, octaveNum);
        const isPressed = isKeyPressed(note, octaveNum);
        
        keys.push(
          <div 
            key={`${note}${octaveNum}`}
            className={`white-key ${isInChord ? 'in-chord' : ''} ${isPressed ? 'pressed' : ''}`}
            onMouseDown={() => {
              playNote(note, octaveNum);
              if (onKeyPress) onKeyPress(`${note}${octaveNum}`, true);
            }}
            onMouseUp={() => {
              stopNote(note, octaveNum);
              if (onKeyPress) onKeyPress(`${note}${octaveNum}`, false);
            }}
            onMouseLeave={() => {
              if (isPressed) {
                stopNote(note, octaveNum);
                if (onKeyPress) onKeyPress(`${note}${octaveNum}`, false);
              }
            }}
          >
            {showNoteNames && <span className="note-name">{note}{octaveNum}</span>}
          </div>
        );
      });
    }
    
    return keys;
  };

  // Renderizar teclas pretas
  const renderBlackKeys = () => {
    const keys = [];
    
    for (let octave = 0; octave < octaves; octave++) {
      blackNotes.forEach(note => {
        const octaveNum = startOctave + octave;
        const position = blackNotePositions[note];
        const isInChord = isNoteInCurrentChord(note, octaveNum);
        const isPressed = isKeyPressed(note, octaveNum);
        
        keys.push(
          <div 
            key={`${note}${octaveNum}`}
            className={`black-key ${isInChord ? 'in-chord' : ''} ${isPressed ? 'pressed' : ''}`}
            style={{ 
              left: `calc(${(octave * 7 + position) * (100 / (octaves * 7))}% - 1.5%)` 
            }}
            onMouseDown={() => {
              playNote(note, octaveNum);
              if (onKeyPress) onKeyPress(`${note}${octaveNum}`, true);
            }}
            onMouseUp={() => {
              stopNote(note, octaveNum);
              if (onKeyPress) onKeyPress(`${note}${octaveNum}`, false);
            }}
            onMouseLeave={() => {
              if (isPressed) {
                stopNote(note, octaveNum);
                if (onKeyPress) onKeyPress(`${note}${octaveNum}`, false);
              }
            }}
          >
            {showNoteNames && <span className="note-name">{note}{octaveNum}</span>}
          </div>
        );
      });
    }
    
    return keys;
  };

  // Renderizar controles
  const renderControls = () => {
    return (
      <div className="keyboard-controls">
        <div className="control-group">
          <label>
            <input 
              type="checkbox" 
              checked={showNoteNames} 
              onChange={() => setShowNoteNames(!showNoteNames)} 
            />
            Mostrar nomes das notas
          </label>
        </div>
        
        <div className="control-group">
          <label>
            <input 
              type="checkbox" 
              checked={highlightChord} 
              onChange={() => setHighlightChord(!highlightChord)} 
            />
            Destacar acorde atual
          </label>
        </div>
        
        <div className="control-group">
          <label>
            Oitava inicial:
            <select 
              value={startOctave} 
              onChange={(e) => setStartOctave(parseInt(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map(octave => (
                <option key={octave} value={octave}>
                  {octave}
                </option>
              ))}
            </select>
          </label>
        </div>
        
        <div className="control-group">
          <label>
            Número de oitavas:
            <select 
              value={octaves} 
              onChange={(e) => setOctaves(parseInt(e.target.value))}
            >
              {[1, 2, 3].map(num => (
                <option key={num} value={num}>
                  {num}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>
    );
  };

  // Renderizar informações do acorde atual
  const renderChordInfo = () => {
    if (!currentChord) return null;
    
    const chordNotes = chordToNotes(currentChord);
    
    return (
      <div className="chord-info">
        <h3>Acorde Atual: {currentChord}</h3>
        <div className="chord-notes">
          <span>Notas: </span>
          {chordNotes.map((noteInfo, index) => (
            <span key={index} className="chord-note">
              {noteInfo.note}
              {index < chordNotes.length - 1 ? ', ' : ''}
            </span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="virtual-keyboard-container">
      {renderChordInfo()}
      {renderControls()}
      
      <div className="keyboard" ref={keyboardRef}>
        <div className="white-keys">
          {renderWhiteKeys()}
        </div>
        <div className="black-keys">
          {renderBlackKeys()}
        </div>
      </div>
      
      <div className="keyboard-help">
        <p>Use o teclado do computador para tocar: A-J para a primeira oitava, K-' para a segunda.</p>
        <p>Teclas pretas: W, E, T, Y, U (primeira oitava) e O, P (segunda oitava).</p>
      </div>
    </div>
  );
};

export default VirtualKeyboard;

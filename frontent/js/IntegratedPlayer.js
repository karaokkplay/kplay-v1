import React, { useState, useEffect } from 'react';
import './IntegratedPlayer.css';
import VirtualKeyboard from './VirtualKeyboard';

const IntegratedPlayer = () => {
  const [midiFile, setMidiFile] = useState(null);
  const [lyricsFile, setLyricsFile] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [chords, setChords] = useState([]);
  const [currentChord, setCurrentChord] = useState(null);
  const [lyrics, setLyrics] = useState([]);
  const [currentLyric, setCurrentLyric] = useState(null);
  const [showKeyboard, setShowKeyboard] = useState(true);
  const [processingStatus, setProcessingStatus] = useState('');
  const [error, setError] = useState('');

  // Efeito para carregar dados de exemplo para demonstração
  useEffect(() => {
    // Dados de exemplo para demonstração
    const exampleChords = [
      { name: 'C', start: 0, end: 4, confidence: 0.9 },
      { name: 'G', start: 4, end: 8, confidence: 0.85 },
      { name: 'Am', start: 8, end: 12, confidence: 0.8 },
      { name: 'F', start: 12, end: 16, confidence: 0.9 },
      { name: 'C', start: 16, end: 20, confidence: 0.95 },
      { name: 'G7', start: 20, end: 24, confidence: 0.75 },
      { name: 'Cmaj7', start: 24, end: 28, confidence: 0.7 },
      { name: 'Dm7', start: 28, end: 32, confidence: 0.8 }
    ];
    
    const exampleLyrics = [
      { text: 'Olá, ', start: 0, end: 2 },
      { text: 'mundo ', start: 2, end: 4 },
      { text: 'da ', start: 4, end: 6 },
      { text: 'música! ', start: 6, end: 8 },
      { text: 'Este ', start: 8, end: 10 },
      { text: 'é ', start: 10, end: 12 },
      { text: 'um ', start: 12, end: 14 },
      { text: 'exemplo ', start: 14, end: 16 },
      { text: 'de ', start: 16, end: 18 },
      { text: 'letra ', start: 18, end: 20 },
      { text: 'sincronizada ', start: 20, end: 24 },
      { text: 'com ', start: 24, end: 26 },
      { text: 'acordes. ', start: 26, end: 28 },
      { text: 'K-Play!', start: 28, end: 32 }
    ];
    
    setChords(exampleChords);
    setLyrics(exampleLyrics);
    setDuration(32);
  }, []);

  // Efeito para atualizar o acorde atual com base no tempo
  useEffect(() => {
    if (chords.length > 0) {
      const current = chords.find(chord => 
        currentTime >= chord.start && currentTime < chord.end
      );
      setCurrentChord(current ? current.name : null);
    }
  }, [currentTime, chords]);

  // Efeito para atualizar a letra atual com base no tempo
  useEffect(() => {
    if (lyrics.length > 0) {
      const current = lyrics.find(lyric => 
        currentTime >= lyric.start && currentTime < lyric.end
      );
      setCurrentLyric(current ? current.text : null);
    }
  }, [currentTime, lyrics]);

  // Simulação de reprodução
  useEffect(() => {
    let timer;
    if (isPlaying && duration > 0) {
      timer = setInterval(() => {
        setCurrentTime(prevTime => {
          const newTime = prevTime + 0.1 * playbackSpeed;
          if (newTime >= duration) {
            setIsPlaying(false);
            return 0;
          }
          return newTime;
        });
      }, 100);
    }
    
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isPlaying, duration, playbackSpeed]);

  // Manipuladores de eventos para upload de arquivos
  const handleMidiUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setMidiFile(file);
      setProcessingStatus('Processando arquivo MIDI...');
      
      // Simulação de processamento do arquivo MIDI
      setTimeout(() => {
        setProcessingStatus('Arquivo MIDI processado com sucesso!');
        // Em uma implementação real, aqui você enviaria o arquivo para o backend
        // e receberia os acordes extraídos como resposta
      }, 1500);
    }
  };

  const handleLyricsUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLyricsFile(file);
      
      // Ler o conteúdo do arquivo de letras
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        // Em uma implementação real, você processaria o conteúdo para extrair as letras
        // e seus tempos de sincronização
        setProcessingStatus('Arquivo de letras carregado com sucesso!');
      };
      reader.onerror = () => {
        setError('Erro ao ler o arquivo de letras.');
      };
      reader.readAsText(file);
    }
  };

  // Manipuladores para controles de reprodução
  const handlePlay = () => {
    setIsPlaying(true);
  };

  const handlePause = () => {
    setIsPlaying(false);
  };

  const handleStop = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const handleSeek = (event) => {
    const newTime = parseFloat(event.target.value);
    setCurrentTime(newTime);
  };

  const handleSpeedChange = (event) => {
    setPlaybackSpeed(parseFloat(event.target.value));
  };

  const handleKeyboardToggle = () => {
    setShowKeyboard(!showKeyboard);
  };

  // Função para formatar o tempo em MM:SS
  const formatTime = (timeInSeconds) => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  // Renderizar letras com destaque para a letra atual
  const renderLyrics = () => {
    return (
      <div className="lyrics-container">
        <div className="lyrics-scroll">
          {lyrics.map((lyric, index) => (
            <span 
              key={index} 
              className={currentTime >= lyric.start && currentTime < lyric.end ? 'current-lyric' : ''}
            >
              {lyric.text}
            </span>
          ))}
        </div>
      </div>
    );
  };

  // Renderizar acordes com destaque para o acorde atual
  const renderChords = () => {
    return (
      <div className="chords-container">
        <div className="chords-scroll">
          {chords.map((chord, index) => (
            <div 
              key={index} 
              className={`chord-item ${currentTime >= chord.start && currentTime < chord.end ? 'current-chord' : ''}`}
              style={{
                left: `${(chord.start / duration) * 100}%`,
                width: `${((chord.end - chord.start) / duration) * 100}%`
              }}
            >
              {chord.name}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="integrated-player">
      <h1>K-Play <span className="subtitle">Karaokê com Acordes</span></h1>
      
      {/* Área de upload de arquivos */}
      <div className="upload-section">
        <div className="upload-group">
          <label htmlFor="midi-upload">Arquivo MIDI:</label>
          <input 
            type="file" 
            id="midi-upload" 
            accept=".mid,.midi,.kar" 
            onChange={handleMidiUpload} 
          />
          <span className="file-name">{midiFile ? midiFile.name : 'Nenhum arquivo selecionado'}</span>
        </div>
        
        <div className="upload-group">
          <label htmlFor="lyrics-upload">Arquivo de Letras:</label>
          <input 
            type="file" 
            id="lyrics-upload" 
            accept=".txt,.lrc" 
            onChange={handleLyricsUpload} 
          />
          <span className="file-name">{lyricsFile ? lyricsFile.name : 'Nenhum arquivo selecionado'}</span>
        </div>
      </div>
      
      {/* Status de processamento */}
      {processingStatus && (
        <div className="processing-status">
          {processingStatus}
        </div>
      )}
      
      {/* Mensagem de erro */}
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {/* Visualização de acordes e letras */}
      <div className="visualization-section">
        {renderChords()}
        {renderLyrics()}
      </div>
      
      {/* Controles de reprodução */}
      <div className="playback-controls">
        <div className="time-display">
          <span>{formatTime(currentTime)}</span>
          <span> / </span>
          <span>{formatTime(duration)}</span>
        </div>
        
        <input 
          type="range" 
          min="0" 
          max={duration} 
          step="0.1" 
          value={currentTime} 
          onChange={handleSeek} 
          className="seek-bar" 
        />
        
        <div className="control-buttons">
          <button onClick={handlePlay} disabled={isPlaying}>
            <i className="fas fa-play"></i> Play
          </button>
          <button onClick={handlePause} disabled={!isPlaying}>
            <i className="fas fa-pause"></i> Pause
          </button>
          <button onClick={handleStop}>
            <i className="fas fa-stop"></i> Stop
          </button>
          
          <div className="speed-control">
            <label htmlFor="speed">Velocidade:</label>
            <select 
              id="speed" 
              value={playbackSpeed} 
              onChange={handleSpeedChange}
            >
              <option value="0.5">0.5x</option>
              <option value="0.75">0.75x</option>
              <option value="1.0">1.0x</option>
              <option value="1.25">1.25x</option>
              <option value="1.5">1.5x</option>
            </select>
          </div>
          
          <button onClick={handleKeyboardToggle} className="toggle-keyboard">
            {showKeyboard ? 'Ocultar Teclado' : 'Mostrar Teclado'}
          </button>
        </div>
      </div>
      
      {/* Teclado virtual */}
      {showKeyboard && (
        <div className="keyboard-section">
          <VirtualKeyboard 
            chords={chords}
            currentChord={currentChord}
            onKeyPress={(note, isPressed) => {
              // Implementação opcional para responder a teclas pressionadas
              console.log(`Nota ${note} ${isPressed ? 'pressionada' : 'liberada'}`);
            }}
          />
        </div>
      )}
      
      {/* Informações do acorde atual */}
      <div className="current-chord-info">
        <h3>Acorde Atual: {currentChord || '-'}</h3>
      </div>
    </div>
  );
};

export default IntegratedPlayer;

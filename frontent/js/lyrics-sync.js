/**
 * lyrics-sync.js
 * Responsável pela sincronização de letras e acordes com o player MIDI
 */

class LyricsSync {
    constructor(midiPlayer) {
        this.midiPlayer = midiPlayer;
        this.lyrics = [];
        this.chords = [];
        this.currentLyricIndex = -1;
        this.currentChordIndex = -1;
        this.lyricsContainer = document.getElementById('lyrics-container');
        this.chordDisplay = document.getElementById('chord-display');
        
        // Adicionar ouvintes de eventos ao player MIDI
        this.midiPlayer.addEventListener('timeUpdate', this.onTimeUpdate.bind(this));
        this.midiPlayer.addEventListener('stop', this.onStop.bind(this));
    }

    /**
     * Carrega dados de letras e acordes
     * @param {Array} lyrics - Array de objetos de letra com tempo e texto
     * @param {Array} chords - Array de objetos de acorde com tempo e nome
     */
    loadData(lyrics, chords) {
        this.lyrics = lyrics || [];
        this.chords = chords || [];
        this.currentLyricIndex = -1;
        this.currentChordIndex = -1;
        
        // Renderizar letras iniciais
        this.renderLyrics();
        
        // Limpar display de acordes
        this.updateChordDisplay('');
    }

    /**
     * Renderiza as letras no container
     */
    renderLyrics() {
        // Limpar o container
        this.lyricsContainer.innerHTML = '';
        
        // Adicionar cada linha de letra
        this.lyrics.forEach((lyric, index) => {
            const line = document.createElement('div');
            line.className = 'lyrics-line';
            line.id = `lyric-${index}`;
            line.textContent = lyric.text;
            this.lyricsContainer.appendChild(line);
        });
    }

    /**
     * Atualiza o display de acordes
     * @param {string} chordName - Nome do acorde a ser exibido
     */
    updateChordDisplay(chordName) {
        this.chordDisplay.textContent = chordName || '';
    }

    /**
     * Destaca a linha de letra atual
     * @param {number} index - Índice da linha a ser destacada
     */
    highlightLyric(index) {
        // Remover destaque de todas as linhas
        const lines = this.lyricsContainer.querySelectorAll('.lyrics-line');
        lines.forEach(line => line.classList.remove('active'));
        
        // Adicionar destaque à linha atual
        if (index >= 0 && index < lines.length) {
            lines[index].classList.add('active');
            
            // Rolar para a linha atual
            this.scrollToLyric(index);
        }
    }

    /**
     * Rola a visualização para a linha de letra atual
     * @param {number} index - Índice da linha para rolar
     */
    scrollToLyric(index) {
        const line = document.getElementById(`lyric-${index}`);
        if (!line) return;
        
        // Calcular posição de rolagem
        const containerHeight = this.lyricsContainer.clientHeight;
        const lineTop = line.offsetTop;
        const lineHeight = line.clientHeight;
        
        // Centralizar a linha na visualização
        const scrollPosition = lineTop - (containerHeight / 2) + (lineHeight / 2);
        
        // Aplicar rolagem suave
        this.lyricsContainer.scrollTo({
            top: Math.max(0, scrollPosition),
            behavior: 'smooth'
        });
    }

    /**
     * Manipulador de evento de atualização de tempo
     * @param {Object} data - Dados do evento com tempo atual
     */
    onTimeUpdate(data) {
        const currentTime = data.currentTime * 1000; // Converter para milissegundos
        
        // Atualizar letra atual
        this.updateCurrentLyric(currentTime);
        
        // Atualizar acorde atual
        this.updateCurrentChord(currentTime);
    }

    /**
     * Atualiza a letra atual com base no tempo
     * @param {number} currentTime - Tempo atual em milissegundos
     */
    updateCurrentLyric(currentTime) {
        // Encontrar a letra atual com base no tempo
        let newIndex = -1;
        
        for (let i = 0; i < this.lyrics.length; i++) {
            if (this.lyrics[i].time <= currentTime) {
                newIndex = i;
            } else {
                break;
            }
        }
        
        // Se a letra mudou, atualizar a visualização
        if (newIndex !== this.currentLyricIndex) {
            this.currentLyricIndex = newIndex;
            this.highlightLyric(newIndex);
        }
    }

    /**
     * Atualiza o acorde atual com base no tempo
     * @param {number} currentTime - Tempo atual em milissegundos
     */
    updateCurrentChord(currentTime) {
        // Encontrar o acorde atual com base no tempo
        let newIndex = -1;
        let chordName = '';
        
        for (let i = 0; i < this.chords.length; i++) {
            if (this.chords[i].time <= currentTime) {
                newIndex = i;
                chordName = this.chords[i].chord;
            } else {
                break;
            }
        }
        
        // Se o acorde mudou, atualizar a visualização
        if (newIndex !== this.currentChordIndex) {
            this.currentChordIndex = newIndex;
            this.updateChordDisplay(chordName);
        }
    }

    /**
     * Manipulador de evento de parada
     */
    onStop() {
        // Resetar índices
        this.currentLyricIndex = -1;
        this.currentChordIndex = -1;
        
        // Limpar destaques
        this.highlightLyric(-1);
        
        // Limpar display de acordes
        this.updateChordDisplay('');
        
        // Rolar para o topo
        this.lyricsContainer.scrollTop = 0;
    }
}

// Exportar a classe para uso global
window.LyricsSync = LyricsSync;

/**
 * midi-player.js
 * Responsável pela reprodução de arquivos MIDI usando Tone.js
 */

class MidiPlayer {
    constructor() {
        this.midi = null;
        this.synths = [];
        this.isPlaying = false;
        this.currentTime = 0;
        this.startTime = 0;
        this.playbackRate = 1.0;
        this.eventListeners = {};
    }

    /**
     * Carrega um arquivo MIDI a partir de uma URL ou ArrayBuffer
     * @param {string|ArrayBuffer} source - URL ou ArrayBuffer do arquivo MIDI
     * @returns {Promise} - Promise que resolve quando o MIDI é carregado
     */
    async loadMidi(source) {
        try {
            // Limpar sintetizadores anteriores
            this.stop();
            this.synths.forEach(synth => synth.dispose());
            this.synths = [];
            
            // Carregar o arquivo MIDI
            if (typeof source === 'string') {
                // Carregar de URL
                const response = await fetch(source);
                const arrayBuffer = await response.arrayBuffer();
                this.midi = new Midi(arrayBuffer);
            } else {
                // Carregar de ArrayBuffer
                this.midi = new Midi(source);
            }
            
            // Configurar sintetizadores para cada faixa
            this.midi.tracks.forEach(track => {
                const synth = new Tone.PolySynth(Tone.Synth).toDestination();
                this.synths.push(synth);
            });
            
            // Disparar evento de MIDI carregado
            this.dispatchEvent('midiLoaded', this.midi);
            
            return this.midi;
        } catch (error) {
            console.error('Erro ao carregar MIDI:', error);
            this.dispatchEvent('error', { message: 'Erro ao carregar arquivo MIDI', error });
            throw error;
        }
    }

    /**
     * Inicia a reprodução do MIDI
     */
    play() {
        if (!this.midi || this.isPlaying) return;
        
        // Iniciar o contexto de áudio se estiver suspenso
        if (Tone.context.state !== 'running') {
            Tone.context.resume();
        }
        
        // Configurar o tempo de início
        this.startTime = Tone.now() - (this.currentTime / this.playbackRate);
        this.isPlaying = true;
        
        // Programar todas as notas para tocar
        this.midi.tracks.forEach((track, trackIndex) => {
            const synth = this.synths[trackIndex];
            
            // Programar cada nota da faixa
            track.notes.forEach(note => {
                const startTime = this.startTime + (note.time / this.playbackRate);
                const duration = note.duration / this.playbackRate;
                
                // Verificar se a nota ainda não foi tocada
                if (startTime > Tone.now()) {
                    synth.triggerAttackRelease(
                        note.name,
                        duration,
                        startTime,
                        note.velocity
                    );
                }
            });
        });
        
        // Iniciar o loop de atualização de tempo
        this.scheduleTimeUpdate();
        
        // Disparar evento de reprodução iniciada
        this.dispatchEvent('play', { currentTime: this.currentTime });
    }

    /**
     * Pausa a reprodução do MIDI
     */
    pause() {
        if (!this.isPlaying) return;
        
        // Parar todas as notas
        this.synths.forEach(synth => {
            synth.releaseAll();
        });
        
        // Atualizar o tempo atual
        this.currentTime = (Tone.now() - this.startTime) * this.playbackRate;
        this.isPlaying = false;
        
        // Cancelar o loop de atualização de tempo
        if (this.timeUpdateInterval) {
            clearInterval(this.timeUpdateInterval);
            this.timeUpdateInterval = null;
        }
        
        // Disparar evento de pausa
        this.dispatchEvent('pause', { currentTime: this.currentTime });
    }

    /**
     * Para a reprodução do MIDI e volta ao início
     */
    stop() {
        if (!this.midi) return;
        
        // Parar todas as notas
        this.synths.forEach(synth => {
            synth.releaseAll();
        });
        
        // Resetar o tempo
        this.currentTime = 0;
        this.isPlaying = false;
        
        // Cancelar o loop de atualização de tempo
        if (this.timeUpdateInterval) {
            clearInterval(this.timeUpdateInterval);
            this.timeUpdateInterval = null;
        }
        
        // Disparar evento de parada
        this.dispatchEvent('stop', { currentTime: 0 });
    }

    /**
     * Define a velocidade de reprodução
     * @param {number} rate - Taxa de reprodução (0.5 a 2.0)
     */
    setPlaybackRate(rate) {
        if (rate < 0.5 || rate > 2.0) return;
        
        const wasPlaying = this.isPlaying;
        
        // Pausar a reprodução atual
        if (wasPlaying) {
            this.pause();
        }
        
        // Atualizar a taxa de reprodução
        this.playbackRate = rate;
        
        // Retomar a reprodução se estava tocando
        if (wasPlaying) {
            this.play();
        }
        
        // Disparar evento de mudança de velocidade
        this.dispatchEvent('rateChange', { playbackRate: this.playbackRate });
    }

    /**
     * Agenda a atualização periódica do tempo atual
     */
    scheduleTimeUpdate() {
        // Cancelar intervalo anterior se existir
        if (this.timeUpdateInterval) {
            clearInterval(this.timeUpdateInterval);
        }
        
        // Criar novo intervalo para atualizar o tempo
        this.timeUpdateInterval = setInterval(() => {
            if (this.isPlaying) {
                this.currentTime = (Tone.now() - this.startTime) * this.playbackRate;
                
                // Disparar evento de atualização de tempo
                this.dispatchEvent('timeUpdate', { 
                    currentTime: this.currentTime,
                    duration: this.midi ? this.midi.duration : 0
                });
                
                // Verificar se chegou ao fim
                if (this.midi && this.currentTime >= this.midi.duration) {
                    this.stop();
                    this.dispatchEvent('ended', {});
                }
            }
        }, 100); // Atualizar a cada 100ms
    }

    /**
     * Adiciona um ouvinte de evento
     * @param {string} event - Nome do evento
     * @param {function} callback - Função de callback
     */
    addEventListener(event, callback) {
        if (!this.eventListeners[event]) {
            this.eventListeners[event] = [];
        }
        this.eventListeners[event].push(callback);
    }

    /**
     * Remove um ouvinte de evento
     * @param {string} event - Nome do evento
     * @param {function} callback - Função de callback a ser removida
     */
    removeEventListener(event, callback) {
        if (!this.eventListeners[event]) return;
        this.eventListeners[event] = this.eventListeners[event].filter(cb => cb !== callback);
    }

    /**
     * Dispara um evento
     * @param {string} event - Nome do evento
     * @param {object} data - Dados do evento
     */
    dispatchEvent(event, data) {
        if (!this.eventListeners[event]) return;
        this.eventListeners[event].forEach(callback => {
            callback(data);
        });
    }

    /**
     * Obtém a duração total do MIDI em segundos
     * @returns {number} - Duração em segundos
     */
    getDuration() {
        return this.midi ? this.midi.duration : 0;
    }

    /**
     * Obtém o tempo atual de reprodução em segundos
     * @returns {number} - Tempo atual em segundos
     */
    getCurrentTime() {
        return this.currentTime;
    }

    /**
     * Verifica se está reproduzindo
     * @returns {boolean} - true se estiver reproduzindo
     */
    getIsPlaying() {
        return this.isPlaying;
    }

    /**
     * Obtém a taxa de reprodução atual
     * @returns {number} - Taxa de reprodução
     */
    getPlaybackRate() {
        return this.playbackRate;
    }
}

// Exportar a classe para uso global
window.MidiPlayer = MidiPlayer;

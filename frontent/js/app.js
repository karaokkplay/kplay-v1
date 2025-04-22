/**
 * app.js
 * Arquivo principal que integra todos os componentes do aplicativo
 */

// Variáveis globais
const API_URL = 'http://localhost:5000/api';
let midiPlayer;
let lyricsSync;
let currentSongId = null;

// Elementos DOM
const uploadForm = document.getElementById('upload-form');
const uploadSection = document.querySelector('.upload-section');
const playerSection = document.querySelector('.player-section');
const songList = document.getElementById('song-list');
const songTitle = document.getElementById('song-title');
const songArtist = document.getElementById('song-artist');
const playBtn = document.getElementById('play-btn');
const pauseBtn = document.getElementById('pause-btn');
const stopBtn = document.getElementById('stop-btn');
const speedSlider = document.getElementById('speed-slider');
const speedValue = document.getElementById('speed-value');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar o player MIDI
    midiPlayer = new MidiPlayer();
    
    // Inicializar o sincronizador de letras
    lyricsSync = new LyricsSync(midiPlayer);
    
    // Configurar ouvintes de eventos
    setupEventListeners();
    
    // Carregar lista de músicas
    loadSongList();
});

/**
 * Configura todos os ouvintes de eventos
 */
function setupEventListeners() {
    // Formulário de upload
    uploadForm.addEventListener('submit', handleUpload);
    
    // Controles do player
    playBtn.addEventListener('click', () => midiPlayer.play());
    pauseBtn.addEventListener('click', () => midiPlayer.pause());
    stopBtn.addEventListener('click', () => midiPlayer.stop());
    
    // Controle de velocidade
    speedSlider.addEventListener('input', handleSpeedChange);
    
    // Eventos do player MIDI
    midiPlayer.addEventListener('play', () => {
        playBtn.disabled = true;
        pauseBtn.disabled = false;
        stopBtn.disabled = false;
    });
    
    midiPlayer.addEventListener('pause', () => {
        playBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = false;
    });
    
    midiPlayer.addEventListener('stop', () => {
        playBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = true;
    });
    
    midiPlayer.addEventListener('ended', () => {
        playBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = true;
    });
    
    midiPlayer.addEventListener('error', (data) => {
        alert(`Erro: ${data.message}`);
    });
}

/**
 * Manipula o envio do formulário de upload
 * @param {Event} event - Evento de envio do formulário
 */
async function handleUpload(event) {
    event.preventDefault();
    
    // Obter dados do formulário
    const formData = new FormData(uploadForm);
    
    try {
        // Enviar arquivos para o backend
        const response = await fetch(`${API_URL}/upload_song`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Erro ao fazer upload da música');
        }
        
        // Gerar acordes a partir do MIDI
        await generateChords(data.song_id);
        
        // Carregar a música
        await loadSong(data.song_id);
        
        // Atualizar a lista de músicas
        loadSongList();
        
        // Mostrar mensagem de sucesso
        alert('Música carregada com sucesso!');
        
    } catch (error) {
        console.error('Erro no upload:', error);
        alert(`Erro ao fazer upload: ${error.message}`);
    }
}

/**
 * Gera acordes a partir do arquivo MIDI
 * @param {string|number} songId - ID da música
 */
async function generateChords(songId) {
    try {
        const response = await fetch(`${API_URL}/generate_chords`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song_id: songId })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Erro ao gerar acordes');
        }
        
        return data;
        
    } catch (error) {
        console.error('Erro ao gerar acordes:', error);
        throw error;
    }
}

/**
 * Carrega uma música pelo ID
 * @param {string|number} songId - ID da música
 */
async function loadSong(songId) {
    try {
        // Obter dados da música do backend
        const response = await fetch(`${API_URL}/get_song_data?id=${songId}`);
        const songData = await response.json();
        
        if (songData.error) {
            throw new Error(songData.error);
        }
        
        // Atualizar informações da música
        songTitle.textContent = songData.title || 'Sem título';
        songArtist.textContent = songData.artist || 'Artista desconhecido';
        
        // Carregar o arquivo MIDI
        const midiResponse = await fetch(`/data/midi/${songId}.mid`);
        const midiArrayBuffer = await midiResponse.arrayBuffer();
        await midiPlayer.loadMidi(midiArrayBuffer);
        
        // Carregar letras e acordes no sincronizador
        lyricsSync.loadData(songData.lyrics, songData.chords);
        
        // Mostrar a seção do player
        uploadSection.style.display = 'none';
        playerSection.style.display = 'block';
        
        // Atualizar ID da música atual
        currentSongId = songId;
        
        // Resetar controles
        playBtn.disabled = false;
        pauseBtn.disabled = true;
        stopBtn.disabled = true;
        
    } catch (error) {
        console.error('Erro ao carregar música:', error);
        alert(`Erro ao carregar música: ${error.message}`);
    }
}

/**
 * Manipula a mudança de velocidade
 */
function handleSpeedChange() {
    const rate = parseFloat(speedSlider.value);
    midiPlayer.setPlaybackRate(rate);
    speedValue.textContent = `${rate.toFixed(1)}x`;
}

/**
 * Carrega a lista de músicas disponíveis
 */
async function loadSongList() {
    try {
        const response = await fetch(`${API_URL}/songs`);
        const songs = await response.json();
        
        // Limpar lista atual
        songList.innerHTML = '';
        
        if (songs.length === 0) {
            // Mostrar mensagem de lista vazia
            const emptyMessage = document.createElement('p');
            emptyMessage.className = 'empty-message';
            emptyMessage.textContent = 'Nenhuma música disponível. Faça upload de uma música para começar.';
            songList.appendChild(emptyMessage);
            return;
        }
        
        // Adicionar cada música à lista
        songs.forEach(song => {
            const songItem = document.createElement('div');
            songItem.className = 'song-item';
            songItem.innerHTML = `
                <h3>${song.title || 'Sem título'}</h3>
                <p>${song.artist || 'Artista desconhecido'}</p>
            `;
            
            // Adicionar evento de clique para carregar a música
            songItem.addEventListener('click', () => loadSong(song.id));
            
            songList.appendChild(songItem);
        });
        
    } catch (error) {
        console.error('Erro ao carregar lista de músicas:', error);
        
        // Mostrar mensagem de erro
        songList.innerHTML = '<p class="empty-message">Erro ao carregar músicas. Tente novamente mais tarde.</p>';
    }
}

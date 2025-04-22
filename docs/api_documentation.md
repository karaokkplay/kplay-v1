# Documentação da API - Aplicativo Web de Karaokê com Acordes Sincronizados

## Visão Geral

Esta documentação descreve a API RESTful do backend do aplicativo web de karaokê com acordes sincronizados. A API permite o upload de arquivos MIDI e letras, extração de acordes, e sincronização de letras e acordes para criar uma experiência de karaokê interativa.

## Base URL

```
http://localhost:5000/api
```

## Endpoints

### 1. Upload de Música

**Endpoint:** `/upload_song`

**Método:** `POST`

**Descrição:** Faz upload de arquivos MIDI e letras para o servidor.

**Parâmetros:**
- `midi` (arquivo, obrigatório): Arquivo MIDI (.mid ou .midi)
- `lyrics` (arquivo, obrigatório): Arquivo de letra (.txt)
- `title` (string, obrigatório): Título da música
- `artist` (string, obrigatório): Nome do artista

**Formato da Resposta:**
```json
{
  "success": true,
  "midi_path": "/caminho/para/arquivo.mid",
  "lyrics_path": "/caminho/para/arquivo.txt",
  "song_id": 1
}
```

**Códigos de Status:**
- `200 OK`: Upload bem-sucedido
- `400 Bad Request`: Parâmetros inválidos ou faltando
- `500 Internal Server Error`: Erro no servidor

### 2. Gerar Acordes

**Endpoint:** `/generate_chords`

**Método:** `POST`

**Descrição:** Extrai acordes de um arquivo MIDI.

**Parâmetros (JSON):**
```json
{
  "song_id": 1
}
```
OU
```json
{
  "midi_path": "/caminho/para/arquivo.mid"
}
```

**Formato da Resposta:**
```json
{
  "success": true,
  "chords": [
    {
      "time": 0,
      "chord": "C",
      "components": ["C", "E", "G"]
    },
    {
      "time": 4000,
      "chord": "G",
      "components": ["G", "B", "D"]
    }
  ],
  "chords_path": "/caminho/para/acordes.json"
}
```

**Códigos de Status:**
- `200 OK`: Extração bem-sucedida
- `400 Bad Request`: Parâmetros inválidos ou faltando
- `404 Not Found`: Arquivo MIDI não encontrado
- `500 Internal Server Error`: Erro no servidor

### 3. Obter Dados da Música

**Endpoint:** `/get_song_data`

**Método:** `GET`

**Descrição:** Obtém dados completos de uma música (letra + acordes).

**Parâmetros:**
- `id` (query string, obrigatório): ID da música

**Formato da Resposta:**
```json
{
  "song_id": 1,
  "title": "Título da Música",
  "artist": "Nome do Artista",
  "lyrics": [
    {
      "time": 10000,
      "text": "Quando você vem"
    },
    {
      "time": 14000,
      "text": "O meu mundo muda de cor"
    }
  ],
  "chords": [
    {
      "time": 0,
      "chord": "C",
      "components": ["C", "E", "G"]
    },
    {
      "time": 4000,
      "chord": "G",
      "components": ["G", "B", "D"]
    }
  ]
}
```

**Códigos de Status:**
- `200 OK`: Dados obtidos com sucesso
- `400 Bad Request`: Parâmetros inválidos ou faltando
- `404 Not Found`: Música não encontrada
- `500 Internal Server Error`: Erro no servidor

### 4. Listar Músicas

**Endpoint:** `/songs`

**Método:** `GET`

**Descrição:** Lista todas as músicas disponíveis.

**Formato da Resposta:**
```json
[
  {
    "id": 1,
    "title": "Título da Música 1",
    "artist": "Nome do Artista 1"
  },
  {
    "id": 2,
    "title": "Título da Música 2",
    "artist": "Nome do Artista 2"
  }
]
```

**Códigos de Status:**
- `200 OK`: Lista obtida com sucesso
- `500 Internal Server Error`: Erro no servidor

## Formato dos Arquivos

### Arquivo de Letra

O arquivo de letra deve estar no formato de texto (.txt) com timestamps no formato `[MM:SS]` ou `[HH:MM:SS]` no início de cada linha, seguido pelo texto da linha. Exemplo:

```
[00:00:10]Quando você vem
[00:00:14]O meu mundo muda de cor
[00:00:18]Como um raio de sol
```

### Arquivo MIDI

O arquivo MIDI (.mid ou .midi) deve conter as notas e acordes da música. O sistema extrairá automaticamente os acordes a partir das notas presentes no arquivo.

## Erros Comuns

- `Arquivos MIDI e letra são obrigatórios`: Certifique-se de enviar ambos os arquivos no upload.
- `Formato de arquivo não permitido`: Verifique se os arquivos estão nos formatos corretos (.mid/.midi para MIDI e .txt para letra).
- `Erro ao extrair acordes`: Pode ocorrer se o arquivo MIDI estiver corrompido ou não contiver informações de acordes.
- `Arquivo não encontrado`: Verifique se o ID da música está correto e se os arquivos existem no servidor.

## Exemplos de Uso

### Upload de Música

```javascript
const formData = new FormData();
formData.append('title', 'Minha Música');
formData.append('artist', 'Meu Artista');
formData.append('midi', midiFile);
formData.append('lyrics', lyricsFile);

fetch('http://localhost:5000/api/upload_song', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Gerar Acordes

```javascript
fetch('http://localhost:5000/api/generate_chords', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ song_id: 1 })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Obter Dados da Música

```javascript
fetch('http://localhost:5000/api/get_song_data?id=1')
.then(response => response.json())
.then(data => console.log(data));
```

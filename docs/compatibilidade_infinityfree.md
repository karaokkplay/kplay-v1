# Guia de Compatibilidade para InfinityFree

Este documento fornece informações específicas sobre a compatibilidade do K-Play com a hospedagem InfinityFree.

## Tecnologias Suportadas pelo InfinityFree

InfinityFree suporta apenas as seguintes tecnologias:
- PHP (versão 7.4)
- HTML
- CSS
- JavaScript
- MySQL

## Arquivos Compatíveis

Todos os arquivos do projeto K-Play foram desenvolvidos usando apenas as tecnologias suportadas:

### Arquivos PHP
- `index.php` - Página inicial
- `karaoke.php` - Funcionalidade de karaokê
- `partituras.php` - Editor de partituras
- `tools.php` - Ferramentas musicais (diapasão, metrônomo)
- `login.php` - Página de login
- `register.php` - Página de registro
- `profile.php` - Perfil do usuário
- `payment.php` - Sistema de pagamento
- `includes/db_connection.php` - Conexão com banco de dados
- `includes/config.php` - Configurações da aplicação
- `partials/header.php` - Cabeçalho reutilizável
- `partials/footer.php` - Rodapé reutilizável

### Arquivos CSS
- `css/styles.css` - Estilos principais
- `css/sheet-music.css` - Estilos para o editor de partituras
- `css/tools.css` - Estilos para ferramentas musicais
- `css/profile.css` - Estilos para perfil de usuário
- `css/payment.css` - Estilos para sistema de pagamento

### Arquivos JavaScript
- `js/app.js` - Funcionalidades gerais
- `js/sheet-music-editor.js` - Editor de partituras
- `js/music-tools.js` - Ferramentas musicais
- `js/midi-player.js` - Player MIDI para karaokê

### Banco de Dados
- `database.sql` - Esquema do banco de dados MySQL

## Limitações do InfinityFree a Considerar

1. **Sem acesso SSH** - Não é possível executar comandos de terminal
2. **Sem suporte para Node.js** - Apenas PHP é suportado para backend
3. **Sem suporte para WebSockets** - Comunicação em tempo real limitada
4. **Limite de execução PHP** - Scripts PHP têm limite de tempo de execução
5. **Limite de tamanho de arquivo** - Arquivos grandes podem não ser aceitos
6. **Limite de tráfego** - Considere o limite de banda mensal

## Adaptações Realizadas

Para garantir compatibilidade com InfinityFree:

1. **Backend em PHP puro** - Sem dependência de outros ambientes de servidor
2. **JavaScript no lado do cliente** - Processamento de MIDI e áudio no navegador
3. **Bibliotecas JavaScript externas** - Carregadas via CDN quando necessário
4. **Armazenamento em MySQL** - Banco de dados compatível com InfinityFree
5. **Arquivos otimizados** - Tamanhos reduzidos para respeitar limites

## Verificação de Compatibilidade

Antes de fazer upload para o InfinityFree, verifique:

1. Todos os arquivos são PHP, HTML, CSS ou JavaScript
2. Não há dependências de Node.js, Python ou outras linguagens
3. O esquema do banco de dados é compatível com MySQL
4. Os caminhos de arquivo usam barras (/) e não contrabarras (\)
5. Permissões de arquivo estão corretas (644 para arquivos, 755 para diretórios)

## Solução de Problemas Comuns

Se encontrar problemas após o upload:

1. **Erro 500** - Verifique a sintaxe PHP e permissões de arquivo
2. **Erro de conexão com banco de dados** - Verifique credenciais em `db_connection.php`
3. **Arquivos não encontrados** - Verifique caminhos e estrutura de diretórios
4. **Problemas de permissão** - Verifique se diretórios de upload têm permissão 755
5. **Tempo limite excedido** - Otimize scripts PHP que possam estar demorando muito

Todos os arquivos fornecidos foram verificados e são compatíveis com as limitações do InfinityFree.

import os
from PIL import Image, ImageDraw, ImageFont

# Configurações
ICON_SIZE = (512, 512)
BACKGROUND_COLOR = (0, 0, 0)  # Preto
TEXT_COLOR = (255, 140, 0)    # Laranja
FONT_SIZE = 200
OUTPUT_PATH = "/home/ubuntu/karaoke-app/frontend/assets/K-Play.png"

def create_app_icon():
    """Cria o ícone do aplicativo K-Play com as cores solicitadas."""
    
    # Criar uma nova imagem com fundo preto
    icon = Image.new('RGB', ICON_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(icon)
    
    # Tentar carregar uma fonte, ou usar a fonte padrão
    try:
        # Tentar encontrar uma fonte instalada no sistema
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            # Alternativa para outras distribuições Linux
            font_path = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
        
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, FONT_SIZE)
        else:
            # Usar fonte padrão se não encontrar a fonte específica
            font = ImageFont.load_default()
            print("Usando fonte padrão, fonte personalizada não encontrada.")
    except Exception as e:
        print(f"Erro ao carregar fonte: {e}")
        font = ImageFont.load_default()
    
    # Texto a ser desenhado
    text = "K"
    
    # Calcular posição para centralizar o texto
    # Usando o método correto para versões mais recentes do Pillow
    left, top, right, bottom = font.getbbox(text)
    text_width = right - left
    text_height = bottom - top
    position = ((ICON_SIZE[0] - text_width) // 2, (ICON_SIZE[1] - text_height) // 2 - 20)
    
    # Desenhar o texto principal "K" em laranja
    draw.text(position, text, fill=TEXT_COLOR, font=font)
    
    # Adicionar o texto "Play" em tamanho menor
    play_text = "Play"
    play_font_size = FONT_SIZE // 2
    
    try:
        if os.path.exists(font_path):
            play_font = ImageFont.truetype(font_path, play_font_size)
        else:
            play_font = ImageFont.load_default()
    except:
        play_font = ImageFont.load_default()
    
    # Calcular posição para o texto "Play"
    play_left, play_top, play_right, play_bottom = play_font.getbbox(play_text)
    play_width = play_right - play_left
    play_height = play_bottom - play_top
    play_position = ((ICON_SIZE[0] - play_width) // 2, position[1] + text_height - 10)
    
    # Desenhar o texto "Play" em branco
    draw.text(play_position, play_text, fill=(255, 255, 255), font=play_font)
    
    # Garantir que o diretório de destino existe
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Salvar a imagem
    icon.save(OUTPUT_PATH)
    print(f"Ícone criado com sucesso em: {OUTPUT_PATH}")
    
    return OUTPUT_PATH

if __name__ == "__main__":
    create_app_icon()

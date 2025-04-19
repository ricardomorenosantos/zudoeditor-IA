#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Seleção de Fundo Visual para o ZudoEditor
Este módulo implementa funcionalidades para selecionar e preparar fundos visuais
para os vídeos gerados automaticamente.
"""

import os
import sys
import time
import random
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import urllib.request
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zudo_background')

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    from moviepy.editor import VideoFileClip, ImageClip, ColorClip
except ImportError as e:
    logger.error(f"Erro ao importar dependências: {e}")
    logger.error("Instale as dependências necessárias: pip install numpy pillow moviepy")
    sys.exit(1)

class BackgroundType:
    """Tipos de fundo disponíveis."""
    SOLID_COLOR = "solid_color"
    IMAGE = "image"
    VIDEO = "video"
    GRADIENT = "gradient"


class BackgroundManager:
    """Gerenciador de fundos visuais para vídeos."""
    
    def __init__(self, resources_dir: str = None):
        """
        Inicializa o gerenciador de fundos.
        
        Args:
            resources_dir: Diretório para recursos visuais (imagens, vídeos)
        """
        # Definir diretório de recursos
        self.resources_dir = resources_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "resources", 
            "backgrounds"
        )
        
        # Criar diretórios se não existirem
        os.makedirs(os.path.join(self.resources_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.resources_dir, "videos"), exist_ok=True)
        
        # Cores predefinidas (nome: valor hexadecimal)
        self.predefined_colors = {
            "Azul escuro": "#1a237e",
            "Azul": "#2196f3",
            "Azul claro": "#bbdefb",
            "Verde escuro": "#1b5e20",
            "Verde": "#4caf50",
            "Verde claro": "#c8e6c9",
            "Vermelho escuro": "#b71c1c",
            "Vermelho": "#f44336",
            "Vermelho claro": "#ffcdd2",
            "Amarelo": "#ffeb3b",
            "Laranja": "#ff9800",
            "Roxo": "#9c27b0",
            "Rosa": "#e91e63",
            "Cinza escuro": "#212121",
            "Cinza": "#9e9e9e",
            "Cinza claro": "#f5f5f5",
            "Preto": "#000000",
            "Branco": "#ffffff",
        }
        
        # Gradientes predefinidos (nome: (cor inicial, cor final))
        self.predefined_gradients = {
            "Azul para Roxo": ("#2196f3", "#9c27b0"),
            "Verde para Azul": ("#4caf50", "#2196f3"),
            "Vermelho para Laranja": ("#f44336", "#ff9800"),
            "Amarelo para Verde": ("#ffeb3b", "#4caf50"),
            "Roxo para Rosa": ("#9c27b0", "#e91e63"),
            "Preto para Azul": ("#000000", "#2196f3"),
            "Branco para Cinza": ("#ffffff", "#9e9e9e"),
            "Azul escuro para Azul claro": ("#1a237e", "#bbdefb"),
        }
        
        # Carregar recursos disponíveis
        self.available_images = self._load_available_resources("images")
        self.available_videos = self._load_available_resources("videos")
        
        logger.info(f"BackgroundManager inicializado com {len(self.available_images)} imagens e {len(self.available_videos)} vídeos")
    
    def _load_available_resources(self, resource_type: str) -> List[str]:
        """
        Carrega a lista de recursos disponíveis.
        
        Args:
            resource_type: Tipo de recurso ("images" ou "videos")
            
        Returns:
            List[str]: Lista de caminhos para os recursos
        """
        resource_dir = os.path.join(self.resources_dir, resource_type)
        
        # Verificar se o diretório existe
        if not os.path.exists(resource_dir):
            os.makedirs(resource_dir, exist_ok=True)
            return []
        
        # Extensões válidas
        valid_extensions = {
            "images": [".jpg", ".jpeg", ".png", ".webp"],
            "videos": [".mp4", ".avi", ".mov", ".webm"]
        }
        
        # Listar arquivos com extensões válidas
        resources = []
        for file in os.listdir(resource_dir):
            file_path = os.path.join(resource_dir, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in valid_extensions.get(resource_type, []):
                    resources.append(file_path)
        
        return resources
    
    def get_predefined_colors(self) -> Dict[str, str]:
        """
        Retorna as cores predefinidas.
        
        Returns:
            Dict[str, str]: Dicionário de cores (nome: valor hexadecimal)
        """
        return self.predefined_colors
    
    def get_predefined_gradients(self) -> Dict[str, Tuple[str, str]]:
        """
        Retorna os gradientes predefinidos.
        
        Returns:
            Dict[str, Tuple[str, str]]: Dicionário de gradientes (nome: (cor inicial, cor final))
        """
        return self.predefined_gradients
    
    def get_available_images(self) -> List[str]:
        """
        Retorna a lista de imagens disponíveis.
        
        Returns:
            List[str]: Lista de caminhos para as imagens
        """
        # Recarregar para incluir novas imagens
        self.available_images = self._load_available_resources("images")
        return self.available_images
    
    def get_available_videos(self) -> List[str]:
        """
        Retorna a lista de vídeos disponíveis.
        
        Returns:
            List[str]: Lista de caminhos para os vídeos
        """
        # Recarregar para incluir novos vídeos
        self.available_videos = self._load_available_resources("videos")
        return self.available_videos
    
    def add_image(self, image_path: str) -> str:
        """
        Adiciona uma imagem à biblioteca de recursos.
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            str: Caminho para a imagem na biblioteca de recursos
        """
        if not os.path.exists(image_path):
            logger.error(f"Imagem não encontrada: {image_path}")
            return None
        
        # Verificar se é uma imagem válida
        try:
            img = Image.open(image_path)
            img.verify()  # Verificar se a imagem é válida
        except Exception as e:
            logger.error(f"Arquivo não é uma imagem válida: {e}")
            return None
        
        # Copiar para a biblioteca de recursos
        filename = os.path.basename(image_path)
        dest_path = os.path.join(self.resources_dir, "images", filename)
        
        try:
            import shutil
            shutil.copy2(image_path, dest_path)
            logger.info(f"Imagem adicionada: {dest_path}")
            
            # Atualizar lista de imagens disponíveis
            self.available_images = self._load_available_resources("images")
            
            return dest_path
        except Exception as e:
            logger.error(f"Erro ao adicionar imagem: {e}")
            return None
    
    def add_video(self, video_path: str) -> str:
        """
        Adiciona um vídeo à biblioteca de recursos.
        
        Args:
            video_path: Caminho para o vídeo
            
        Returns:
            str: Caminho para o vídeo na biblioteca de recursos
        """
        if not os.path.exists(video_path):
            logger.error(f"Vídeo não encontrado: {video_path}")
            return None
        
        # Verificar se é um vídeo válido
        try:
            video = VideoFileClip(video_path)
            video.close()
        except Exception as e:
            logger.error(f"Arquivo não é um vídeo válido: {e}")
            return None
        
        # Copiar para a biblioteca de recursos
        filename = os.path.basename(video_path)
        dest_path = os.path.join(self.resources_dir, "videos", filename)
        
        try:
            import shutil
            shutil.copy2(video_path, dest_path)
            logger.info(f"Vídeo adicionado: {dest_path}")
            
            # Atualizar lista de vídeos disponíveis
            self.available_videos = self._load_available_resources("videos")
            
            return dest_path
        except Exception as e:
            logger.error(f"Erro ao adicionar vídeo: {e}")
            return None
    
    def download_free_image(self, query: str = None) -> str:
        """
        Baixa uma imagem gratuita da internet.
        
        Args:
            query: Termo de busca (opcional)
            
        Returns:
            str: Caminho para a imagem baixada
        """
        # Usar Unsplash Source para imagens gratuitas
        # Nota: Este é um serviço gratuito com limites de uso
        if not query:
            # Termos genéricos para fundos
            terms = ["nature", "abstract", "texture", "gradient", "background", "minimal"]
            query = random.choice(terms)
        
        # Formatar query para URL
        query = query.replace(" ", "%20")
        
        # Gerar URL do Unsplash Source
        width, height = 1920, 1080  # Resolução HD
        url = f"https://source.unsplash.com/random/{width}x{height}/?{query}"
        
        try:
            # Criar nome de arquivo baseado na query e timestamp
            timestamp = int(time.time())
            filename = f"unsplash_{query.replace('%20', '_')}_{timestamp}.jpg"
            dest_path = os.path.join(self.resources_dir, "images", filename)
            
            # Baixar imagem
            logger.info(f"Baixando imagem de {url}")
            urllib.request.urlretrieve(url, dest_path)
            
            # Verificar se o download foi bem-sucedido
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                logger.info(f"Imagem baixada: {dest_path}")
                
                # Atualizar lista de imagens disponíveis
                self.available_images = self._load_available_resources("images")
                
                return dest_path
            else:
                logger.error("Falha ao baixar imagem")
                return None
        except Exception as e:
            logger.error(f"Erro ao baixar imagem: {e}")
            return None
    
    def create_solid_color_background(self, color: str, width: int = 1920, height: int = 1080, output_path: str = None) -> str:
        """
        Cria um fundo com cor sólida.
        
        Args:
            color: Cor em formato hexadecimal (#RRGGBB)
            width: Largura da imagem
            height: Altura da imagem
            output_path: Caminho para salvar a imagem (opcional)
            
        Returns:
            str: Caminho para a imagem gerada
        """
        try:
            # Verificar formato da cor
            if not color.startswith("#"):
                # Verificar se é um nome de cor predefinida
                if color in self.predefined_colors:
                    color = self.predefined_colors[color]
                else:
                    logger.warning(f"Cor não reconhecida: {color}. Usando preto.")
                    color = "#000000"
            
            # Criar imagem com cor sólida
            img = Image.new("RGB", (width, height), color)
            
            # Gerar caminho de saída se não especificado
            if not output_path:
                timestamp = int(time.time())
                color_hex = color.replace("#", "")
                output_path = os.path.join(
                    self.resources_dir, 
                    "images", 
                    f"solid_{color_hex}_{timestamp}.png"
                )
            
            # Salvar imagem
            img.save(output_path)
            logger.info(f"Fundo com cor sólida criado: {output_path}")
            
            # Atualizar lista de imagens disponíveis
            self.available_images = self._load_available_resources("images")
            
            return output_path
        except Exception as e:
            logger.error(f"Erro ao criar fundo com cor sólida: {e}")
            return None
    
    def create_gradient_background(self, start_color: str, end_color: str, direction: str = "horizontal", 
                                  width: int = 1920, height: int = 1080, output_path: str = None) -> str:
        """
        Cria um fundo com gradiente.
        
        Args:
            start_color: Cor inicial em formato hexadecimal (#RRGGBB)
            end_color: Cor final em formato hexadecimal (#RRGGBB)
            direction: Direção do gradiente ("horizontal", "vertical", "diagonal")
            width: Largura da imagem
            height: Altura da imagem
            output_path: Caminho para salvar a imagem (opcional)
            
        Returns:
            str: Caminho para a imagem gerada
        """
        try:
            # Verificar formato das cores
            for color_name, color in [("start_color", start_color), ("end_color", end_color)]:
                if not color.startswith("#"):
                    # Verificar se é um nome de cor predefinida
                    if color in self.predefined_colors:
                        if color_name == "start_color":
                            start_color = self.predefined_colors[color]
                        else:
                            end_color = self.predefined_colors[color]
                    else:
                        logger.warning(f"Cor não reconhecida: {color}. Usando preto.")
                        if color_name == "start_color":
                            start_color = "#000000"
                        else:
                            end_color = "#ffffff"
            
            # Converter cores hexadecimais para RGB
            start_rgb = tuple(int(start_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            end_rgb = tuple(int(end_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            
            # Criar imagem base
            img = Image.new("RGB", (width, height), start_rgb)
            draw = ImageDraw.Draw(img)
            
            # Criar gradiente
            if direction == "horizontal":
                for x in range(width):
                    # Calcular cor interpolada
                    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * x / width)
                    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * x / width)
                    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * x / width)
                    
                    # Desenhar linha vertical com a cor interpolada
                    draw.line([(x, 0), (x, height)], fill=(r, g, b))
            
            elif direction == "vertical":
                for y in range(height):
                    # Calcular cor interpolada
                    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * y / height)
                    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * y / height)
                    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * y / height)
                    
                    # Desenhar linha horizontal com a cor interpolada
                    draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            elif direction == "diagonal":
                # Criar array numpy para manipulação mais eficiente
                gradient = np.zeros((height, width, 3), dtype=np.uint8)
                
                for y in range(height):
                    for x in range(width):
                        # Calcular posição relativa na diagonal
                        pos = (x + y) / (width + height)
                        
                        # Calcular cor interpolada
                        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * pos)
                        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * pos)
                        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * pos)
                        
                        gradient[y, x] = [r, g, b]
                
                # Converter array numpy para imagem PIL
                img = Image.fromarray(gradient, "RGB")
            
            else:
                logger.warning(f"Direção de gradiente não reconhecida: {direction}. Usando horizontal.")
                return self.create_gradient_background(start_color, end_color, "horizontal", width, height, output_path)
            
            # Gerar caminho de saída se não especificado
            if not output_path:
                timestamp = int(time.time())
                start_hex = start_color.replace("#", "")
                end_hex = end_color.replace("#", "")
                output_path = os.path.join(
                    self.resources_dir, 
                    "images", 
                    f"gradient_{start_hex}_{end_hex}_{direction}_{timestamp}.png"
                )
            
            # Salvar imagem
            img.save(output_path)
            logger.info(f"Fundo com gradiente criado: {output_path}")
            
            # Atualizar lista de imagens disponíveis
            self.available_images = self._load_available_resources("images")
            
            return output_path
        except Exception as e:
            logger.error(f"Erro ao criar fundo com gradiente: {e}")
            return None
    
    def create_background_clip(self, background_type: str, background_source: str, duration: float, 
                              width: int = 1920, height: int = 1080, fps: int = 30) -> Union[ImageClip, ColorClip, VideoFileClip]:
        """
        Cria um clip de fundo para o vídeo.
        
        Args:
            background_type: Tipo de fundo (BackgroundType.SOLID_COLOR, BackgroundType.IMAGE, etc.)
            background_source: Fonte do fundo (caminho para imagem/vídeo ou cor)
            duration: Duração do clip em segundos
            width: Largura do clip
            height: Altura do clip
            fps: Frames por segundo
            
        Returns:
            Union[ImageClip, ColorClip, VideoFileClip]: Clip de fundo
        """
        try:
            if background_type == BackgroundType.SOLID_COLOR:
                # Verificar se é uma cor predefinida
                if background_source in self.predefined_colors:
                    background_source = self.predefined_colors[background_source]
                
                # Criar clip com cor sólida
                return ColorClip(size=(width, height), color=background_source, duration=duration)
            
            elif background_type == BackgroundType.GRADIENT:
                # Verificar se é um gradiente predefinido
                if background_source in self.predefined_gradients:
                    start_color, end_color = self.predefined_gradients[background_source]
                else:
                    # Formato esperado: "start_color,end_color,direction"
                    parts = background_source.split(",")
                    if len(parts) >= 2:
                        start_color, end_color = parts[0], parts[1]
                        direction = parts[2] if len(parts) > 2 else "horizontal"
                    else:
                        logger.warning(f"Formato de gradiente inválido: {background_source}. Usando padrão.")
                        start_color, end_color = "#000000", "#ffffff"
                        direction = "horizontal"
                
                # Criar imagem de gradiente
                gradient_path = self.create_gradient_background(start_color, end_color, direction, width, height)
                
                # Criar clip com a imagem de gradiente
                return ImageClip(gradient_path, duration=duration)
            
            elif background_type == BackgroundType.IMAGE:
                # Verificar se o arquivo existe
                if not os.path.exists(background_source):
                    logger.warning(f"Imagem não encontrada: {background_source}. Usando cor preta.")
                    return ColorClip(size=(width, height), color="#000000", duration=duration)
                
                # Criar clip com a imagem
                image_clip = ImageClip(background_source, duration=duration)
                
                # Redimensionar para preencher o frame
                image_clip = image_clip.resize(height=height) if image_clip.h < image_clip.w else image_clip.resize(width=width)
                
                # Centralizar
                image_clip = image_clip.set_position("center")
                
                return image_clip
            
            elif background_type == BackgroundType.VIDEO:
                # Verificar se o arquivo existe
                if not os.path.exists(background_source):
                    logger.warning(f"Vídeo não encontrado: {background_source}. Usando cor preta.")
                    return ColorClip(size=(width, height), color="#000000", duration=duration)
                
                # Criar clip com o vídeo
                video_clip = VideoFileClip(background_source)
                
                # Ajustar duração (loop se necessário)
                if video_clip.duration < duration:
                    # Calcular quantas vezes o vídeo precisa ser repetido
                    n_loops = int(duration / video_clip.duration) + 1
                    video_clip = video_clip.loop(n=n_loops)
                
                # Cortar para a duração desejada
                video_clip = video_clip.subclip(0, duration)
                
                # Redimensionar para preencher o frame
                video_clip = video_clip.resize(height=height) if video_clip.h < video_clip.w else video_clip.resize(width=width)
                
                # Centralizar
                video_clip = video_clip.set_position("center")
                
                return video_clip
            
            else:
                logger.warning(f"Tipo de fundo não reconhecido: {background_type}. Usando cor preta.")
                return ColorClip(size=(width, height), color="#000000", duration=duration)
        
        except Exception as e:
            logger.error(f"Erro ao criar clip de fundo: {e}")
            return ColorClip(size=(width, height), color="#000000", duration=duration)
    
    def get_random_background(self, background_type: str = None, duration: float = 30, 
                             width: int = 1920, height: int = 1080) -> Dict:
        """
        Seleciona um fundo aleatório.
        
        Args:
            background_type: Tipo de fundo (opcional)
            duration: Duração do clip em segundos
            width: Largura do clip
            height: Altura do clip
            
        Returns:
            Dict: Informações do fundo selecionado
        """
        # Se o tipo não for especificado, escolher aleatoriamente
        if not background_type:
            available_types = [
                BackgroundType.SOLID_COLOR,
                BackgroundType.GRADIENT,
                BackgroundType.IMAGE
            ]
            
            # Adicionar vídeo apenas se houver vídeos disponíveis
            if self.available_videos:
                available_types.append(BackgroundType.VIDEO)
            
            background_type = random.choice(available_types)
        
        # Selecionar fundo com base no tipo
        if background_type == BackgroundType.SOLID_COLOR:
            # Escolher uma cor aleatória
            color_name = random.choice(list(self.predefined_colors.keys()))
            color_value = self.predefined_colors[color_name]
            
            return {
                "type": BackgroundType.SOLID_COLOR,
                "source": color_value,
                "name": color_name
            }
        
        elif background_type == BackgroundType.GRADIENT:
            # Escolher um gradiente aleatório
            gradient_name = random.choice(list(self.predefined_gradients.keys()))
            start_color, end_color = self.predefined_gradients[gradient_name]
            
            return {
                "type": BackgroundType.GRADIENT,
                "source": f"{start_color},{end_color},horizontal",
                "name": gradient_name
            }
        
        elif background_type == BackgroundType.IMAGE:
            # Verificar se há imagens disponíveis
            if not self.available_images:
                # Tentar baixar uma imagem aleatória
                image_path = self.download_free_image()
                
                if not image_path:
                    # Fallback para cor sólida
                    logger.warning("Nenhuma imagem disponível. Usando cor sólida.")
                    return self.get_random_background(BackgroundType.SOLID_COLOR, duration, width, height)
            else:
                # Escolher uma imagem aleatória
                image_path = random.choice(self.available_images)
            
            return {
                "type": BackgroundType.IMAGE,
                "source": image_path,
                "name": os.path.basename(image_path)
            }
        
        elif background_type == BackgroundType.VIDEO:
            # Verificar se há vídeos disponíveis
            if not self.available_videos:
                # Fallback para imagem
                logger.warning("Nenhum vídeo disponível. Usando imagem.")
                return self.get_random_background(BackgroundType.IMAGE, duration, width, height)
            
            # Escolher um vídeo aleatório
            video_path = random.choice(self.available_videos)
            
            return {
                "type": BackgroundType.VIDEO,
                "source": video_path,
                "name": os.path.basename(video_path)
            }
        
        else:
            logger.warning(f"Tipo de fundo não reconhecido: {background_type}. Usando cor sólida.")
            return self.get_random_background(BackgroundType.SOLID_COLOR, duration, width, height)


# Função de teste
def test_background_manager():
    """Testa o gerenciador de fundos."""
    manager = BackgroundManager()
    
    print("Cores predefinidas:")
    for name, color in list(manager.get_predefined_colors().items())[:5]:  # Mostrar apenas as 5 primeiras
        print(f"- {name}: {color}")
    
    print("\nGradientes predefinidos:")
    for name, (start, end) in list(manager.get_predefined_gradients().items())[:5]:  # Mostrar apenas os 5 primeiros
        print(f"- {name}: {start} -> {end}")
    
    print("\nImagens disponíveis:")
    for image in manager.get_available_images()[:5]:  # Mostrar apenas as 5 primeiras
        print(f"- {os.path.basename(image)}")
    
    print("\nVídeos disponíveis:")
    for video in manager.get_available_videos()[:5]:  # Mostrar apenas os 5 primeiros
        print(f"- {os.path.basename(video)}")
    
    # Testar criação de fundo com cor sólida
    print("\nCriando fundo com cor sólida...")
    solid_path = manager.create_solid_color_background("#3498db", 640, 360)
    if solid_path:
        print(f"Fundo criado: {solid_path}")
    
    # Testar criação de fundo com gradiente
    print("\nCriando fundo com gradiente...")
    gradient_path = manager.create_gradient_background("#3498db", "#e74c3c", "horizontal", 640, 360)
    if gradient_path:
        print(f"Fundo criado: {gradient_path}")
    
    # Testar seleção de fundo aleatório
    print("\nSelecionando fundo aleatório...")
    random_bg = manager.get_random_background()
    print(f"Fundo selecionado: {random_bg['name']} ({random_bg['type']})")


if __name__ == "__main__":
    test_background_manager()

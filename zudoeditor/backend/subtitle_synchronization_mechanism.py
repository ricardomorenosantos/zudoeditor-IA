#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mecanismo de Sincronização de Legendas para o ZudoEditor
Este módulo implementa funcionalidades para gerar e sincronizar legendas
com o áudio narrado nos vídeos gerados automaticamente.
"""

import os
import sys
import time
import json
import tempfile
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import subprocess

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zudo_subtitles')

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
    import speech_recognition as sr
except ImportError as e:
    logger.error(f"Erro ao importar dependências: {e}")
    logger.error("Instale as dependências necessárias: pip install numpy pillow moviepy SpeechRecognition")
    sys.exit(1)

class SubtitleStyle:
    """Estilos de legenda disponíveis."""
    STANDARD = "standard"
    BOLD = "bold"
    SHADOW = "shadow"
    OUTLINE = "outline"
    MODERN = "modern"
    MINIMAL = "minimal"


class SubtitlePosition:
    """Posições de legenda disponíveis."""
    BOTTOM = "bottom"
    TOP = "top"
    MIDDLE = "middle"


class SubtitleFormat:
    """Formatos de arquivo de legenda."""
    SRT = "srt"
    VTT = "vtt"
    ASS = "ass"


class SubtitleManager:
    """Gerenciador de legendas para vídeos."""
    
    def __init__(self, resources_dir: str = None):
        """
        Inicializa o gerenciador de legendas.
        
        Args:
            resources_dir: Diretório para recursos (fontes, etc.)
        """
        # Definir diretório de recursos
        self.resources_dir = resources_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "resources", 
            "fonts"
        )
        
        # Criar diretório se não existir
        os.makedirs(self.resources_dir, exist_ok=True)
        
        # Estilos predefinidos (nome: configuração)
        self.predefined_styles = {
            SubtitleStyle.STANDARD: {
                "font": "Arial",
                "fontsize": 36,
                "color": "white",
                "bg_color": None,
                "stroke_color": None,
                "stroke_width": 0,
                "shadow": False,
                "shadow_color": "black",
                "shadow_offset": (2, 2)
            },
            SubtitleStyle.BOLD: {
                "font": "Arial-Bold",
                "fontsize": 40,
                "color": "white",
                "bg_color": None,
                "stroke_color": None,
                "stroke_width": 0,
                "shadow": False,
                "shadow_color": "black",
                "shadow_offset": (2, 2)
            },
            SubtitleStyle.SHADOW: {
                "font": "Arial",
                "fontsize": 36,
                "color": "white",
                "bg_color": None,
                "stroke_color": None,
                "stroke_width": 0,
                "shadow": True,
                "shadow_color": "black",
                "shadow_offset": (2, 2)
            },
            SubtitleStyle.OUTLINE: {
                "font": "Arial",
                "fontsize": 36,
                "color": "white",
                "bg_color": None,
                "stroke_color": "black",
                "stroke_width": 2,
                "shadow": False,
                "shadow_color": "black",
                "shadow_offset": (2, 2)
            },
            SubtitleStyle.MODERN: {
                "font": "Roboto-Medium",
                "fontsize": 38,
                "color": "white",
                "bg_color": "rgba(0,0,0,0.5)",
                "stroke_color": None,
                "stroke_width": 0,
                "shadow": True,
                "shadow_color": "black",
                "shadow_offset": (1, 1)
            },
            SubtitleStyle.MINIMAL: {
                "font": "Roboto-Light",
                "fontsize": 32,
                "color": "white",
                "bg_color": None,
                "stroke_color": "black",
                "stroke_width": 1,
                "shadow": False,
                "shadow_color": "black",
                "shadow_offset": (0, 0)
            }
        }
        
        # Carregar fontes disponíveis
        self.available_fonts = self._load_available_fonts()
        
        logger.info(f"SubtitleManager inicializado com {len(self.available_fonts)} fontes")
    
    def _load_available_fonts(self) -> List[str]:
        """
        Carrega a lista de fontes disponíveis.
        
        Returns:
            List[str]: Lista de nomes de fontes
        """
        # Fontes padrão que devem estar disponíveis em qualquer sistema
        system_fonts = ["Arial", "Arial-Bold", "Times-Roman", "Courier", "Helvetica"]
        
        # Verificar fontes no diretório de recursos
        custom_fonts = []
        if os.path.exists(self.resources_dir):
            for file in os.listdir(self.resources_dir):
                if file.lower().endswith((".ttf", ".otf")):
                    # Extrair nome da fonte do arquivo
                    font_name = os.path.splitext(file)[0]
                    custom_fonts.append(font_name)
        
        # Tentar detectar fontes instaladas no sistema
        try:
            from PIL import ImageFont
            
            # Verificar se as fontes do sistema estão disponíveis
            available_system_fonts = []
            for font in system_fonts:
                try:
                    # Tentar carregar a fonte
                    ImageFont.truetype(font, 12)
                    available_system_fonts.append(font)
                except:
                    pass
            
            return available_system_fonts + custom_fonts
        except:
            # Fallback para fontes padrão
            return system_fonts + custom_fonts
    
    def get_predefined_styles(self) -> Dict[str, Dict]:
        """
        Retorna os estilos predefinidos.
        
        Returns:
            Dict[str, Dict]: Dicionário de estilos (nome: configuração)
        """
        return self.predefined_styles
    
    def get_available_fonts(self) -> List[str]:
        """
        Retorna a lista de fontes disponíveis.
        
        Returns:
            List[str]: Lista de nomes de fontes
        """
        return self.available_fonts
    
    def add_font(self, font_path: str) -> str:
        """
        Adiciona uma fonte à biblioteca de recursos.
        
        Args:
            font_path: Caminho para o arquivo de fonte
            
        Returns:
            str: Nome da fonte adicionada
        """
        if not os.path.exists(font_path):
            logger.error(f"Fonte não encontrada: {font_path}")
            return None
        
        # Verificar se é uma fonte válida
        try:
            from PIL import ImageFont
            ImageFont.truetype(font_path, 12)
        except Exception as e:
            logger.error(f"Arquivo não é uma fonte válida: {e}")
            return None
        
        # Copiar para a biblioteca de recursos
        filename = os.path.basename(font_path)
        dest_path = os.path.join(self.resources_dir, filename)
        
        try:
            import shutil
            shutil.copy2(font_path, dest_path)
            
            # Extrair nome da fonte
            font_name = os.path.splitext(filename)[0]
            
            logger.info(f"Fonte adicionada: {font_name}")
            
            # Atualizar lista de fontes disponíveis
            self.available_fonts = self._load_available_fonts()
            
            return font_name
        except Exception as e:
            logger.error(f"Erro ao adicionar fonte: {e}")
            return None
    
    def estimate_word_duration(self, word: str, speech_rate: float = 150) -> float:
        """
        Estima a duração de uma palavra falada.
        
        Args:
            word: Palavra a ser estimada
            speech_rate: Taxa de fala em palavras por minuto
            
        Returns:
            float: Duração estimada em segundos
        """
        # Remover pontuação
        word = re.sub(r'[^\w\s]', '', word)
        
        # Contar sílabas (estimativa simples)
        vowels = "aeiouyàáâãäåèéêëìíîïòóôõöùúûüAEIOUYÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜ"
        count = 0
        prev_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel
        
        # Garantir pelo menos uma sílaba
        count = max(1, count)
        
        # Calcular duração (em segundos)
        # Fórmula: (sílabas / (palavras por minuto / 60))
        duration = count / (speech_rate / 60)
        
        # Adicionar um pequeno buffer
        duration *= 1.2
        
        return duration
    
    def generate_subtitle_timing_from_text(self, text: str, speech_rate: float = 150) -> List[Dict]:
        """
        Gera o timing das legendas a partir do texto.
        
        Args:
            text: Texto completo
            speech_rate: Taxa de fala em palavras por minuto
            
        Returns:
            List[Dict]: Lista de legendas com timing
        """
        # Dividir o texto em sentenças
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Remover sentenças vazias
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Gerar timing para cada sentença
        subtitles = []
        current_time = 0.0
        
        for sentence in sentences:
            # Estimar duração da sentença
            words = sentence.split()
            sentence_duration = sum(self.estimate_word_duration(word, speech_rate) for word in words)
            
            # Adicionar pausa entre sentenças
            sentence_duration += 0.3
            
            # Criar entrada de legenda
            subtitle = {
                "text": sentence,
                "start": current_time,
                "end": current_time + sentence_duration
            }
            
            subtitles.append(subtitle)
            
            # Atualizar tempo atual
            current_time += sentence_duration
        
        return subtitles
    
    def generate_subtitle_timing_from_audio(self, audio_path: str, text: str = None) -> List[Dict]:
        """
        Gera o timing das legendas a partir do áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            text: Texto completo (opcional)
            
        Returns:
            List[Dict]: Lista de legendas com timing
        """
        try:
            # Verificar se o Whisper está disponível
            try:
                import whisper
                use_whisper = True
            except ImportError:
                use_whisper = False
                logger.warning("Whisper não está instalado. Usando método alternativo.")
            
            if use_whisper:
                # Usar Whisper para transcrição com timestamps
                model = whisper.load_model("tiny")
                result = model.transcribe(audio_path, word_timestamps=True)
                
                # Extrair segmentos com timestamps
                segments = result["segments"]
                
                # Converter para formato de legendas
                subtitles = []
                for segment in segments:
                    subtitle = {
                        "text": segment["text"].strip(),
                        "start": segment["start"],
                        "end": segment["end"]
                    }
                    subtitles.append(subtitle)
                
                return subtitles
            
            # Método alternativo usando SpeechRecognition
            elif text:
                # Se temos o texto, usar estimativa baseada no texto
                return self.generate_subtitle_timing_from_text(text)
            
            else:
                # Tentar usar SpeechRecognition para transcrição
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                
                # Gerar timing baseado no texto
                return self.generate_subtitle_timing_from_text(text)
        
        except Exception as e:
            logger.error(f"Erro ao gerar timing das legendas: {e}")
            
            # Fallback para estimativa baseada no texto
            if text:
                return self.generate_subtitle_timing_from_text(text)
            else:
                # Sem texto, criar uma única legenda para todo o áudio
                audio_clip = AudioFileClip(audio_path)
                return [{
                    "text": "Texto não disponível",
                    "start": 0,
                    "end": audio_clip.duration
                }]
    
    def create_subtitle_clips(self, subtitles: List[Dict], style: str = SubtitleStyle.STANDARD, 
                             position: str = SubtitlePosition.BOTTOM, video_size: Tuple[int, int] = (1920, 1080)) -> List[TextClip]:
        """
        Cria clips de legenda para cada entrada de legenda.
        
        Args:
            subtitles: Lista de legendas com timing
            style: Estilo de legenda
            position: Posição da legenda
            video_size: Tamanho do vídeo (largura, altura)
            
        Returns:
            List[TextClip]: Lista de clips de legenda
        """
        try:
            # Obter configuração de estilo
            if style in self.predefined_styles:
                style_config = self.predefined_styles[style]
            else:
                logger.warning(f"Estilo não reconhecido: {style}. Usando padrão.")
                style_config = self.predefined_styles[SubtitleStyle.STANDARD]
            
            # Criar clips de legenda
            subtitle_clips = []
            
            for subtitle in subtitles:
                # Configurar parâmetros do TextClip
                text_params = {
                    "txt": subtitle["text"],
                    "fontsize": style_config["fontsize"],
                    "color": style_config["color"],
                    "font": style_config["font"],
                    "stroke_color": style_config["stroke_color"],
                    "stroke_width": style_config["stroke_width"],
                    "method": "caption",
                    "align": "center",
                    "size": (video_size[0] * 0.9, None)  # 90% da largura do vídeo
                }
                
                # Adicionar fundo se especificado
                if style_config["bg_color"]:
                    text_params["bg_color"] = style_config["bg_color"]
                
                # Criar TextClip
                txt_clip = TextClip(**text_params)
                
                # Adicionar sombra se especificado
                if style_config["shadow"]:
                    # Criar clip de sombra
                    shadow_params = text_params.copy()
                    shadow_params["color"] = style_config["shadow_color"]
                    if "bg_color" in shadow_params:
                        del shadow_params["bg_color"]
                    
                    shadow_clip = TextClip(**shadow_params)
                    shadow_clip = shadow_clip.set_position((
                        style_config["shadow_offset"][0],
                        style_config["shadow_offset"][1]
                    ))
                    
                    # Combinar sombra e texto
                    txt_clip = CompositeVideoClip([shadow_clip, txt_clip])
                
                # Definir posição
                if position == SubtitlePosition.BOTTOM:
                    txt_clip = txt_clip.set_position(("center", video_size[1] - txt_clip.h - 50))
                elif position == SubtitlePosition.TOP:
                    txt_clip = txt_clip.set_position(("center", 50))
                elif position == SubtitlePosition.MIDDLE:
                    txt_clip = txt_clip.set_position("center")
                else:
                    txt_clip = txt_clip.set_position(("center", video_size[1] - txt_clip.h - 50))
                
                # Definir duração e tempo de início
                txt_clip = txt_clip.set_start(subtitle["start"]).set_duration(subtitle["end"] - subtitle["start"])
                
                subtitle_clips.append(txt_clip)
            
            return subtitle_clips
        
        except Exception as e:
            logger.error(f"Erro ao criar clips de legenda: {e}")
            return []
    
    def export_subtitles_file(self, subtitles: List[Dict], output_path: str, format: str = SubtitleFormat.SRT) -> str:
        """
        Exporta as legendas para um arquivo.
        
        Args:
            subtitles: Lista de legendas com timing
            output_path: Caminho para o arquivo de saída
            format: Formato do arquivo de legenda
            
        Returns:
            str: Caminho para o arquivo de legenda
        """
        try:
            # Garantir que o diretório de saída existe
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Exportar no formato especificado
            if format == SubtitleFormat.SRT:
                with open(output_path, "w", encoding="utf-8") as f:
                    for i, subtitle in enumerate(subtitles, 1):
                        # Converter tempos para formato SRT (HH:MM:SS,mmm)
                        start_time = self._format_time_srt(subtitle["start"])
                        end_time = self._format_time_srt(subtitle["end"])
                        
                        # Escrever entrada de legenda
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{subtitle['text']}\n\n")
            
            elif format == SubtitleFormat.VTT:
                with open(output_path, "w", encoding="utf-8") as f:
                    # Cabeçalho WebVTT
                    f.write("WEBVTT\n\n")
                    
                    for i, subtitle in enumerate(subtitles, 1):
                        # Converter tempos para formato VTT (HH:MM:SS.mmm)
                        start_time = self._format_time_vtt(subtitle["start"])
                        end_time = self._format_time_vtt(subtitle["end"])
                        
                        # Escrever entrada de legenda
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{subtitle['text']}\n\n")
            
            elif format == SubtitleFormat.ASS:
                with open(output_path, "w", encoding="utf-8") as f:
                    # Cabeçalho ASS
                    f.write("[Script Info]\n")
                    f.write("Title: Generated by ZudoEditor\n")
                    f.write("ScriptType: v4.00+\n")
                    f.write("PlayResX: 1920\n")
                    f.write("PlayResY: 1080\n\n")
                    
                    # Estilos
                    f.write("[V4+ Styles]\n")
                    f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
                    f.write("Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
                    
                    # Eventos
                    f.write("[Events]\n")
                    f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
                    
                    for subtitle in subtitles:
                        # Converter tempos para formato ASS (H:MM:SS.mm)
                        start_time = self._format_time_ass(subtitle["start"])
                        end_time = self._format_time_ass(subtitle["end"])
                        
                        # Escrever entrada de legenda
                        f.write(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{subtitle['text']}\n")
            
            else:
                logger.warning(f"Formato não reconhecido: {format}. Usando SRT.")
                return self.export_subtitles_file(subtitles, output_path, SubtitleFormat.SRT)
            
            logger.info(f"Arquivo de legenda exportado: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Erro ao exportar arquivo de legenda: {e}")
            return None
    
    def _format_time_srt(self, seconds: float) -> str:
        """
        Formata o tempo para o formato SRT (HH:MM:SS,mmm).
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            str: Tempo formatado
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"
    
    def _format_time_vtt(self, seconds: float) -> str:
        """
        Formata o tempo para o formato VTT (HH:MM:SS.mmm).
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            str: Tempo formatado
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d}.{milliseconds:03d}"
    
    def _format_time_ass(self, seconds: float) -> str:
        """
        Formata o tempo para o formato ASS (H:MM:SS.mm).
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            str: Tempo formatado
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        centiseconds = int((seconds - int(seconds)) * 100)
        
        return f"{hours}:{minutes:02d}:{int(seconds):02d}.{centiseconds:02d}"


# Função de teste
def test_subtitle_manager():
    """Testa o gerenciador de legendas."""
    manager = SubtitleManager()
    
    print("Estilos predefinidos:")
    for name in manager.get_predefined_styles().keys():
        print(f"- {name}")
    
    print("\nFontes disponíveis:")
    for font in manager.get_available_fonts():
        print(f"- {font}")
    
    # Testar geração de timing a partir de texto
    text = "Este é um teste do sistema de legendas. Vamos ver como funciona a sincronização automática. Cada frase deve ter seu próprio timing."
    
    print(f"\nGerando timing para o texto: '{text}'")
    subtitles = manager.generate_subtitle_timing_from_text(text)
    
    print("\nLegendas geradas:")
    for i, subtitle in enumerate(subtitles, 1):
        print(f"{i}. {subtitle['start']:.2f} --> {subtitle['end']:.2f}: {subtitle['text']}")
    
    # Testar exportação de arquivo de legenda
    output_path = os.path.join(tempfile.gettempdir(), "test_subtitles.srt")
    result = manager.export_subtitles_file(subtitles, output_path)
    
    if result:
        print(f"\nArquivo de legenda exportado: {result}")
        
        # Mostrar conteúdo do arquivo
        print("\nConteúdo do arquivo:")
        with open(result, "r", encoding="utf-8") as f:
            print(f.read())


if __name__ == "__main__":
    test_subtitle_manager()

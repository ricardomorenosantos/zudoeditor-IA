#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Geração Automática de Vídeos com IA para o ZudoEditor
Este módulo integra os componentes de conversão texto-fala, seleção de fundo visual
e sincronização de legendas para gerar vídeos completos a partir de texto.
"""

import os
import sys
import time
import json
import random
import tempfile
import logging
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zudo_video_generator')

# Importar componentes
try:
    # Adicionar diretório atual ao path para importar módulos locais
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from text_to_speech_component import TTSManager
    from background_selection_system import BackgroundManager, BackgroundType
    from subtitle_synchronization_mechanism import SubtitleManager, SubtitleStyle, SubtitlePosition
    
    # Importar dependências externas
    import numpy as np
    from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
except ImportError as e:
    logger.error(f"Erro ao importar dependências: {e}")
    logger.error("Certifique-se de que todos os componentes e dependências estão instalados.")
    sys.exit(1)

class VideoGeneratorConfig:
    """Configuração para o gerador de vídeos."""
    
    def __init__(self, **kwargs):
        """
        Inicializa a configuração com valores padrão ou personalizados.
        
        Args:
            **kwargs: Parâmetros de configuração personalizados
        """
        # Configurações de vídeo
        self.video_width = kwargs.get("video_width", 1920)
        self.video_height = kwargs.get("video_height", 1080)
        self.video_fps = kwargs.get("video_fps", 30)
        self.video_codec = kwargs.get("video_codec", "libx264")
        self.audio_codec = kwargs.get("audio_codec", "aac")
        self.audio_bitrate = kwargs.get("audio_bitrate", "192k")
        
        # Configurações de TTS
        self.tts_engine = kwargs.get("tts_engine", None)  # Usar padrão do TTSManager
        self.tts_voice = kwargs.get("tts_voice", None)    # Usar padrão do motor selecionado
        self.speech_rate = kwargs.get("speech_rate", 150) # Palavras por minuto
        
        # Configurações de fundo
        self.background_type = kwargs.get("background_type", None)  # Aleatório se None
        self.background_source = kwargs.get("background_source", None)  # Depende do tipo
        
        # Configurações de legenda
        self.subtitle_style = kwargs.get("subtitle_style", SubtitleStyle.MODERN)
        self.subtitle_position = kwargs.get("subtitle_position", SubtitlePosition.BOTTOM)
        self.export_subtitle_file = kwargs.get("export_subtitle_file", True)
        
        # Configurações de saída
        self.output_dir = kwargs.get("output_dir", os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
        self.temp_dir = kwargs.get("temp_dir", os.path.join(tempfile.gettempdir(), "zudo_generator"))
        
        # Criar diretórios se não existirem
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Configurações de integração
        self.input_dir = kwargs.get("input_dir", os.path.join(os.path.dirname(os.path.abspath(__file__)), "entrada"))
        os.makedirs(self.input_dir, exist_ok=True)


class VideoGenerator:
    """Gerador de vídeos a partir de texto."""
    
    def __init__(self, config: VideoGeneratorConfig = None):
        """
        Inicializa o gerador de vídeos.
        
        Args:
            config: Configuração personalizada (opcional)
        """
        # Usar configuração padrão se não especificada
        self.config = config or VideoGeneratorConfig()
        
        # Inicializar componentes
        self.tts_manager = TTSManager(output_dir=os.path.join(self.config.temp_dir, "audio"))
        self.background_manager = BackgroundManager(resources_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources"))
        self.subtitle_manager = SubtitleManager(resources_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "fonts"))
        
        # Definir motor TTS padrão se especificado
        if self.config.tts_engine:
            self.tts_manager.set_default_engine(self.config.tts_engine)
        
        # Definir voz padrão se especificada
        if self.config.tts_voice:
            self.tts_manager.set_voice(self.config.tts_voice)
        
        logger.info("VideoGenerator inicializado")
    
    def generate_script(self, topic: str) -> str:
        """
        Gera um roteiro a partir de um tópico.
        
        Args:
            topic: Tópico para o roteiro
            
        Returns:
            str: Roteiro gerado
        """
        try:
            # Tentar usar um modelo de linguagem local
            try:
                from transformers import pipeline
                
                # Inicializar pipeline de geração de texto
                generator = pipeline('text-generation', model='gpt2')
                
                # Gerar texto
                prompt = f"Escreva um breve texto sobre {topic}. "
                result = generator(prompt, max_length=150, num_return_sequences=1)
                
                # Extrair texto gerado
                script = result[0]['generated_text']
                
                # Limpar o texto (remover o prompt e limitar tamanho)
                script = script.replace(prompt, "")
                
                # Limitar a 30 segundos (aproximadamente 75-100 palavras)
                words = script.split()
                if len(words) > 100:
                    script = " ".join(words[:100])
                
                return script
            
            except (ImportError, Exception) as e:
                logger.warning(f"Não foi possível usar modelo de linguagem: {e}")
                
                # Usar templates pré-definidos como fallback
                templates = [
                    f"{topic} é um assunto fascinante que tem atraído a atenção de muitas pessoas. Vamos explorar alguns aspectos importantes sobre este tema e entender por que ele é tão relevante nos dias de hoje.",
                    f"Você já parou para pensar sobre {topic}? Este é um tema que tem ganhado destaque recentemente. Vamos descobrir juntos o que torna este assunto tão especial e por que você deveria se interessar por ele.",
                    f"Hoje vamos falar sobre {topic}, um tópico que tem impactado a vida de muitas pessoas. Entender este assunto pode trazer benefícios significativos e abrir novas perspectivas.",
                    f"O que você sabe sobre {topic}? Este é um tema que merece nossa atenção por diversos motivos. Vamos explorar alguns pontos importantes e descobrir por que este assunto é tão relevante atualmente.",
                    f"{topic} é mais importante do que muitos imaginam. Neste vídeo, vamos apresentar informações essenciais sobre este tema e mostrar como ele pode fazer diferença em sua vida."
                ]
                
                return random.choice(templates)
        
        except Exception as e:
            logger.error(f"Erro ao gerar roteiro: {e}")
            
            # Retornar um texto genérico em caso de erro
            return f"Este é um vídeo sobre {topic}. Um tema interessante que merece nossa atenção por diversos motivos."
    
    def generate_video_from_text(self, text: str, output_filename: str = None) -> str:
        """
        Gera um vídeo a partir de um texto.
        
        Args:
            text: Texto para narração
            output_filename: Nome do arquivo de saída (opcional)
            
        Returns:
            str: Caminho para o vídeo gerado
        """
        try:
            # Gerar nome de arquivo se não especificado
            if not output_filename:
                timestamp = int(time.time())
                output_filename = f"video_{timestamp}.mp4"
            
            # Garantir que tem extensão .mp4
            if not output_filename.lower().endswith(".mp4"):
                output_filename += ".mp4"
            
            # Caminho completo para o arquivo de saída
            output_path = os.path.join(self.config.output_dir, output_filename)
            
            # 1. Gerar áudio a partir do texto
            logger.info("Gerando áudio a partir do texto...")
            audio_path = os.path.join(self.config.temp_dir, f"audio_{int(time.time())}.mp3")
            audio_path = self.tts_manager.synthesize(
                text, 
                audio_path, 
                engine_name=self.config.tts_engine, 
                voice_id=self.config.tts_voice
            )
            
            if not audio_path or not os.path.exists(audio_path):
                raise Exception("Falha ao gerar áudio")
            
            # Carregar áudio para obter duração
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # 2. Selecionar fundo visual
            logger.info("Selecionando fundo visual...")
            if self.config.background_type and self.config.background_source:
                # Usar fundo especificado
                background_info = {
                    "type": self.config.background_type,
                    "source": self.config.background_source
                }
            else:
                # Selecionar fundo aleatório
                background_info = self.background_manager.get_random_background(
                    duration=duration,
                    width=self.config.video_width,
                    height=self.config.video_height
                )
            
            logger.info(f"Fundo selecionado: {background_info['type']}")
            
            # 3. Gerar timing das legendas
            logger.info("Gerando timing das legendas...")
            subtitles = self.subtitle_manager.generate_subtitle_timing_from_audio(audio_path, text)
            
            # 4. Exportar arquivo de legenda (opcional)
            if self.config.export_subtitle_file:
                subtitle_path = os.path.splitext(output_path)[0] + ".srt"
                self.subtitle_manager.export_subtitles_file(subtitles, subtitle_path)
            
            # 5. Criar clips de legenda
            logger.info("Criando clips de legenda...")
            subtitle_clips = self.subtitle_manager.create_subtitle_clips(
                subtitles,
                style=self.config.subtitle_style,
                position=self.config.subtitle_position,
                video_size=(self.config.video_width, self.config.video_height)
            )
            
            # 6. Criar clip de fundo
            logger.info("Criando clip de fundo...")
            background_clip = self.background_manager.create_background_clip(
                background_info["type"],
                background_info["source"],
                duration,
                self.config.video_width,
                self.config.video_height,
                self.config.video_fps
            )
            
            # 7. Combinar áudio, fundo e legendas
            logger.info("Combinando elementos do vídeo...")
            video_with_audio = background_clip.set_audio(audio_clip)
            final_clip = CompositeVideoClip([video_with_audio] + subtitle_clips)
            
            # 8. Exportar vídeo final
            logger.info(f"Exportando vídeo final para {output_path}...")
            final_clip.write_videofile(
                output_path,
                codec=self.config.video_codec,
                audio_codec=self.config.audio_codec,
                audio_bitrate=self.config.audio_bitrate,
                fps=self.config.video_fps
            )
            
            # 9. Limpar arquivos temporários
            audio_clip.close()
            final_clip.close()
            
            logger.info(f"Vídeo gerado com sucesso: {output_path}")
            
            # 10. Copiar para pasta de entrada do ZudoEditor (para processamento adicional)
            input_copy_path = os.path.join(self.config.input_dir, output_filename)
            shutil.copy2(output_path, input_copy_path)
            logger.info(f"Vídeo copiado para pasta de entrada: {input_copy_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"Erro ao gerar vídeo: {e}")
            return None
    
    def generate_video_from_topic(self, topic: str, output_filename: str = None) -> str:
        """
        Gera um vídeo a partir de um tópico.
        
        Args:
            topic: Tópico para o vídeo
            output_filename: Nome do arquivo de saída (opcional)
            
        Returns:
            str: Caminho para o vídeo gerado
        """
        # Gerar roteiro a partir do tópico
        logger.info(f"Gerando roteiro para o tópico: {topic}")
        script = self.generate_script(topic)
        
        # Gerar vídeo a partir do roteiro
        return self.generate_video_from_text(script, output_filename)
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Retorna a lista de vozes disponíveis.
        
        Returns:
            List[Dict[str, str]]: Lista de vozes disponíveis
        """
        return self.tts_manager.get_available_voices()
    
    def get_available_engines(self) -> List[str]:
        """
        Retorna a lista de motores TTS disponíveis.
        
        Returns:
            List[str]: Lista de motores TTS disponíveis
        """
        return self.tts_manager.get_available_engines()
    
    def get_available_subtitle_styles(self) -> List[str]:
        """
        Retorna a lista de estilos de legenda disponíveis.
        
        Returns:
            List[str]: Lista de estilos de legenda disponíveis
        """
        return list(self.subtitle_manager.get_predefined_styles().keys())
    
    def get_available_background_types(self) -> List[str]:
        """
        Retorna a lista de tipos de fundo disponíveis.
        
        Returns:
            List[str]: Lista de tipos de fundo disponíveis
        """
        return [
            BackgroundType.SOLID_COLOR,
            BackgroundType.GRADIENT,
            BackgroundType.IMAGE,
            BackgroundType.VIDEO
        ]
    
    def get_predefined_colors(self) -> Dict[str, str]:
        """
        Retorna as cores predefinidas.
        
        Returns:
            Dict[str, str]: Dicionário de cores (nome: valor hexadecimal)
        """
        return self.background_manager.get_predefined_colors()
    
    def get_predefined_gradients(self) -> Dict[str, Tuple[str, str]]:
        """
        Retorna os gradientes predefinidos.
        
        Returns:
            Dict[str, Tuple[str, str]]: Dicionário de gradientes (nome: (cor inicial, cor final))
        """
        return self.background_manager.get_predefined_gradients()
    
    def get_available_images(self) -> List[str]:
        """
        Retorna a lista de imagens disponíveis.
        
        Returns:
            List[str]: Lista de caminhos para as imagens
        """
        return self.background_manager.get_available_images()
    
    def get_available_videos(self) -> List[str]:
        """
        Retorna a lista de vídeos disponíveis.
        
        Returns:
            List[str]: Lista de caminhos para os vídeos
        """
        return self.background_manager.get_available_videos()


class VideoGeneratorUI:
    """Interface de linha de comando para o gerador de vídeos."""
    
    def __init__(self):
        """Inicializa a interface de linha de comando."""
        self.generator = VideoGenerator()
    
    def run(self):
        """Executa a interface de linha de comando."""
        parser = argparse.ArgumentParser(description="Gerador de Vídeos com IA para o ZudoEditor")
        
        # Subcomandos
        subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
        
        # Comando: gerar
        generate_parser = subparsers.add_parser("gerar", help="Gerar um vídeo")
        generate_parser.add_argument("--texto", "-t", help="Texto para narração")
        generate_parser.add_argument("--topico", "-p", help="Tópico para gerar roteiro automaticamente")
        generate_parser.add_argument("--saida", "-o", help="Nome do arquivo de saída")
        generate_parser.add_argument("--voz", "-v", help="ID da voz a ser usada")
        generate_parser.add_argument("--motor", "-m", help="Motor TTS a ser usado")
        generate_parser.add_argument("--estilo", "-e", help="Estilo de legenda")
        generate_parser.add_argument("--fundo", "-f", help="Tipo de fundo")
        generate_parser.add_argument("--fonte-fundo", "-s", help="Fonte do fundo (depende do tipo)")
        
        # Comando: listar
        list_parser = subparsers.add_parser("listar", help="Listar recursos disponíveis")
        list_parser.add_argument("--vozes", action="store_true", help="Listar vozes disponíveis")
        list_parser.add_argument("--motores", action="store_true", help="Listar motores TTS disponíveis")
        list_parser.add_argument("--estilos", action="store_true", help="Listar estilos de legenda disponíveis")
        list_parser.add_argument("--fundos", action="store_true", help="Listar tipos de fundo disponíveis")
        list_parser.add_argument("--cores", action="store_true", help="Listar cores predefinidas")
        list_parser.add_argument("--gradientes", action="store_true", help="Listar gradientes predefinidos")
        list_parser.add_argument("--imagens", action="store_true", help="Listar imagens disponíveis")
        list_parser.add_argument("--videos", action="store_true", help="Listar vídeos disponíveis")
        
        # Analisar argumentos
        args = parser.parse_args()
        
        # Executar comando
        if args.command == "gerar":
            if args.texto:
                # Gerar vídeo a partir de texto
                result = self.generator.generate_video_from_text(args.texto, args.saida)
                if result:
                    print(f"Vídeo gerado com sucesso: {result}")
                else:
                    print("Falha ao gerar vídeo")
            
            elif args.topico:
                # Gerar vídeo a partir de tópico
                result = self.generator.generate_video_from_topic(args.topico, args.saida)
                if result:
                    print(f"Vídeo gerado com sucesso: {result}")
                else:
                    print("Falha ao gerar vídeo")
            
            else:
                print("Erro: É necessário especificar um texto ou tópico")
                generate_parser.print_help()
        
        elif args.command == "listar":
            if args.vozes:
                # Listar vozes disponíveis
                voices = self.generator.get_available_voices()
                print(f"Vozes disponíveis ({len(voices)}):")
                for voice in voices:
                    print(f"- ID: {voice['id']}")
                    print(f"  Nome: {voice['name']}")
                    print(f"  Idioma: {voice['language']}")
                    print(f"  Gênero: {voice['gender']}")
                    print()
            
            elif args.motores:
                # Listar motores TTS disponíveis
                engines = self.generator.get_available_engines()
                print(f"Motores TTS disponíveis ({len(engines)}):")
                for engine in engines:
                    print(f"- {engine}")
            
            elif args.estilos:
                # Listar estilos de legenda disponíveis
                styles = self.generator.get_available_subtitle_styles()
                print(f"Estilos de legenda disponíveis ({len(styles)}):")
                for style in styles:
                    print(f"- {style}")
            
            elif args.fundos:
                # Listar tipos de fundo disponíveis
                types = self.generator.get_available_background_types()
                print(f"Tipos de fundo disponíveis ({len(types)}):")
                for type_ in types:
                    print(f"- {type_}")
            
            elif args.cores:
                # Listar cores predefinidas
                colors = self.generator.get_predefined_colors()
                print(f"Cores predefinidas ({len(colors)}):")
                for name, color in colors.items():
                    print(f"- {name}: {color}")
            
            elif args.gradientes:
                # Listar gradientes predefinidos
                gradients = self.generator.get_predefined_gradients()
                print(f"Gradientes predefinidos ({len(gradients)}):")
                for name, (start, end) in gradients.items():
                    print(f"- {name}: {start} -> {end}")
            
            elif args.imagens:
                # Listar imagens disponíveis
                images = self.generator.get_available_images()
                print(f"Imagens disponíveis ({len(images)}):")
                for image in images:
                    print(f"- {os.path.basename(image)}")
            
            elif args.videos:
                # Listar vídeos disponíveis
                videos = self.generator.get_available_videos()
                print(f"Vídeos disponíveis ({len(videos)}):")
                for video in videos:
                    print(f"- {os.path.basename(video)}")
            
            else:
                print("Erro: É necessário especificar o que listar")
                list_parser.print_help()
        
        else:
            parser.print_help()


# Função principal
def main():
    """Função principal."""
    ui = VideoGeneratorUI()
    ui.run()


if __name__ == "__main__":
    main()

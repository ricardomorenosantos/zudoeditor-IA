#!/usr/bin/env python3
"""
Processador de Vídeo para Sistema de Automação de Vídeos

Este script processa vídeos crus, adicionando legendas automáticas,
aplicando filtros, inserindo chamadas para ação e adaptando para
diferentes plataformas de mídia social.

Uso:
    python processador_video.py --arquivo /caminho/para/video.mp4 --pasta_saida /caminho/para/pasta_saida
"""

import os
import sys
import json
import argparse
import logging
import subprocess
import tempfile
import shutil
from datetime import datetime
import numpy as np
import cv2
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import speech_recognition as sr

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("processador_video.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ProcessadorVideo")

# Configurações das plataformas
PLATAFORMAS = {
    "youtube": {
        "resolucao": (1080, 1920),  # 9:16
        "duracao_maxima": 60,  # segundos
        "texto_cta": "Confira meu eBook! Link na descrição",
        "posicao_cta": ("center", 0.85),  # (x, y) relativo
        "cor_cta": "white",
        "bg_cta": "rgba(0,0,0,0.5)"
    },
    "instagram": {
        "resolucao": (1080, 1920),  # 9:16
        "duracao_maxima": 90,  # segundos
        "texto_cta": "Confira meu eBook! Link na bio",
        "posicao_cta": ("center", 0.85),
        "cor_cta": "white",
        "bg_cta": "rgba(0,0,0,0.5)"
    },
    "tiktok": {
        "resolucao": (1080, 1920),  # 9:16
        "duracao_maxima": 60,  # segundos
        "texto_cta": "Link do eBook na bio! 📚",
        "posicao_cta": ("center", 0.85),
        "cor_cta": "white",
        "bg_cta": "rgba(0,0,0,0.5)"
    }
}


class ProcessadorVideo:
    """Classe principal para processamento de vídeos"""
    
    def __init__(self, arquivo_entrada, pasta_saida):
        self.arquivo_entrada = arquivo_entrada
        self.pasta_saida = pasta_saida
        self.pasta_temp = os.path.join(pasta_saida, "temp")
        self.metadados_path = os.path.join(pasta_saida, "metadados.json")
        
        # Criar pasta temporária
        if not os.path.exists(self.pasta_temp):
            os.makedirs(self.pasta_temp)
        
        # Carregar metadados
        self.metadados = self._carregar_metadados()
        
        # Atualizar status
        self._atualizar_status("processando")
    
    def _carregar_metadados(self):
        """Carrega os metadados do arquivo JSON"""
        try:
            with open(self.metadados_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar metadados: {str(e)}")
            return {
                "arquivo_original": self.arquivo_entrada,
                "data_deteccao": datetime.now().isoformat(),
                "status": "detectado",
                "plataformas": ["youtube", "instagram", "tiktok"]
            }
    
    def _salvar_metadados(self):
        """Salva os metadados no arquivo JSON"""
        try:
            with open(self.metadados_path, "w") as f:
                json.dump(self.metadados, f, indent=4)
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {str(e)}")
    
    def _atualizar_status(self, status, detalhes=None):
        """Atualiza o status nos metadados"""
        self.metadados["status"] = status
        self.metadados["ultima_atualizacao"] = datetime.now().isoformat()
        
        if detalhes:
            if "detalhes" not in self.metadados:
                self.metadados["detalhes"] = {}
            self.metadados["detalhes"].update(detalhes)
        
        self._salvar_metadados()
    
    def processar(self):
        """Processa o vídeo para todas as plataformas configuradas"""
        try:
            logger.info(f"Iniciando processamento de: {self.arquivo_entrada}")
            
            # Extrair informações do vídeo original
            info_video = self._extrair_info_video()
            self.metadados["info_original"] = info_video
            self._salvar_metadados()
            
            # Extrair áudio para reconhecimento de fala
            arquivo_audio = self._extrair_audio()
            
            # Gerar legendas
            legendas = self._gerar_legendas(arquivo_audio)
            self.metadados["legendas_geradas"] = len(legendas) > 0
            self._salvar_metadados()
            
            # Processar para cada plataforma
            resultados = {}
            for plataforma in self.metadados.get("plataformas", ["youtube", "instagram", "tiktok"]):
                if plataforma in PLATAFORMAS:
                    self._atualizar_status("processando", {"plataforma_atual": plataforma})
                    
                    arquivo_saida = self._processar_plataforma(
                        plataforma, 
                        info_video, 
                        legendas
                    )
                    
                    if arquivo_saida:
                        resultados[plataforma] = {
                            "arquivo": arquivo_saida,
                            "timestamp": datetime.now().isoformat()
                        }
            
            # Atualizar metadados com resultados
            self.metadados["resultados"] = resultados
            self._atualizar_status("concluido")
            
            # Limpar arquivos temporários
            self._limpar_temp()
            
            logger.info(f"Processamento concluído para: {self.arquivo_entrada}")
            return True
            
        except Exception as e:
            logger.error(f"Erro durante processamento: {str(e)}")
            self._atualizar_status("erro", {"mensagem_erro": str(e)})
            return False
    
    def _extrair_info_video(self):
        """Extrai informações básicas do vídeo usando ffprobe"""
        try:
            comando = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration,size,bit_rate:stream=width,height,codec_name,codec_type",
                "-of", "json",
                self.arquivo_entrada
            ]
            
            resultado = subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if resultado.returncode != 0:
                raise Exception(f"Erro ao extrair informações do vídeo: {resultado.stderr}")
            
            info = json.loads(resultado.stdout)
            
            # Extrair informações relevantes
            streams = info.get("streams", [])
            formato = info.get("format", {})
            
            video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
            audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
            
            return {
                "duracao": float(formato.get("duration", 0)),
                "tamanho": int(formato.get("size", 0)),
                "bitrate": int(formato.get("bit_rate", 0)),
                "largura": int(video_stream.get("width", 0)) if video_stream else 0,
                "altura": int(video_stream.get("height", 0)) if video_stream else 0,
                "codec_video": video_stream.get("codec_name") if video_stream else None,
                "codec_audio": audio_stream.get("codec_name") if audio_stream else None,
                "tem_audio": audio_stream is not None
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do vídeo: {str(e)}")
            return {
                "duracao": 0,
                "tamanho": 0,
                "bitrate": 0,
                "largura": 0,
                "altura": 0,
                "codec_video": None,
                "codec_audio": None,
                "tem_audio": False
            }
    
    def _extrair_audio(self):
        """Extrai o áudio do vídeo para um arquivo WAV temporário"""
        arquivo_saida = os.path.join(self.pasta_temp, "audio.wav")
        
        try:
            comando = [
                "ffmpeg",
                "-i", self.arquivo_entrada,
                "-vn",  # Sem vídeo
                "-acodec", "pcm_s16le",  # Formato PCM
                "-ar", "16000",  # Taxa de amostragem
                "-ac", "1",  # Mono
                "-y",  # Sobrescrever
                arquivo_saida
            ]
            
            subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            
            logger.info(f"Áudio extraído para: {arquivo_saida}")
            return arquivo_saida
            
        except Exception as e:
            logger.error(f"Erro ao extrair áudio: {str(e)}")
            return None
    
    def _gerar_legendas(self, arquivo_audio):
        """Gera legendas a partir do áudio usando reconhecimento de fala"""
        if not arquivo_audio or not os.path.exists(arquivo_audio):
            logger.warning("Arquivo de áudio não disponível para geração de legendas")
            return []
        
        try:
            logger.info("Iniciando reconhecimento de fala para legendas")
            
            # Inicializar reconhecedor
            recognizer = sr.Recognizer()
            
            # Lista para armazenar legendas com timestamps
            legendas = []
            
            # Carregar áudio
            with sr.AudioFile(arquivo_audio) as source:
                # Ajustar para ruído ambiente
                recognizer.adjust_for_ambient_noise(source)
                
                # Definir duração dos segmentos (em segundos)
                duracao_segmento = 10
                
                # Obter duração total do áudio
                audio_info = self._extrair_info_audio(arquivo_audio)
                duracao_total = audio_info.get("duracao", 0)
                
                # Processar áudio em segmentos
                for offset in range(0, int(duracao_total), duracao_segmento):
                    # Calcular duração real do segmento
                    duracao_real = min(duracao_segmento, duracao_total - offset)
                    
                    # Pular segmentos muito curtos
                    if duracao_real < 1:
                        continue
                    
                    # Capturar segmento de áudio
                    audio_data = recognizer.record(source, duration=duracao_real)
                    
                    try:
                        # Reconhecer fala (usando Google Speech Recognition)
                        texto = recognizer.recognize_google(audio_data, language="pt-BR")
                        
                        if texto:
                            # Adicionar à lista de legendas
                            legendas.append({
                                "inicio": offset,
                                "fim": offset + duracao_real,
                                "texto": texto
                            })
                            
                            logger.debug(f"Legenda reconhecida: {texto}")
                    
                    except sr.UnknownValueError:
                        logger.debug(f"Nenhuma fala reconhecida no segmento {offset}-{offset+duracao_real}")
                    except sr.RequestError as e:
                        logger.warning(f"Erro na API de reconhecimento: {str(e)}")
                    except Exception as e:
                        logger.warning(f"Erro ao processar segmento de áudio: {str(e)}")
            
            logger.info(f"Reconhecimento de fala concluído. {len(legendas)} segmentos gerados.")
            return legendas
            
        except Exception as e:
            logger.error(f"Erro ao gerar legendas: {str(e)}")
            return []
    
    def _extrair_info_audio(self, arquivo_audio):
        """Extrai informações do arquivo de áudio"""
        try:
            comando = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                arquivo_audio
            ]
            
            resultado = subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if resultado.returncode != 0:
                raise Exception(f"Erro ao extrair informações do áudio: {resultado.stderr}")
            
            info = json.loads(resultado.stdout)
            formato = info.get("format", {})
            
            return {
                "duracao": float(formato.get("duration", 0))
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do áudio: {str(e)}")
            return {"duracao": 0}
    
    def _processar_plataforma(self, plataforma, info_video, legendas):
        """Processa o vídeo para uma plataforma específica"""
        try:
            logger.info(f"Processando vídeo para plataforma: {plataforma}")
            
            config = PLATAFORMAS.get(plataforma, {})
            if not config:
                raise Exception(f"Configuração não encontrada para plataforma: {plataforma}")
            
            # Nome do arquivo de saída
            nome_base = os.path.basename(self.arquivo_entrada)
            nome_sem_ext, _ = os.path.splitext(nome_base)
            arquivo_saida = os.path.join(self.pasta_saida, f"{nome_sem_ext}_{plataforma}.mp4")
            
            # Carregar vídeo com MoviePy
            video = VideoFileClip(self.arquivo_entrada)
            
            # Verificar duração
            if video.duration > config["duracao_maxima"]:
                logger.info(f"Vídeo excede duração máxima para {plataforma}. Cortando para {config['duracao_maxima']}s")
                video = video.subclip(0, config["duracao_maxima"])
            
            # Redimensionar para a resolução da plataforma
            video = self._redimensionar_video(video, config["resolucao"])
            
            # Aplicar filtros básicos
            video = self._aplicar_filtros(video)
            
            # Adicionar legendas
            if legendas:
                video = self._adicionar_legendas(video, legendas)
            
            # Adicionar CTA (Call to Action)
            video = self._adicionar_cta(video, config["texto_cta"], config["posicao_cta"], 
                                       config["cor_cta"], config["bg_cta"])
            
            # Adicionar marca d'água
            video = self._adicionar_marca_dagua(video)
            
            # Salvar vídeo processado
            video.write_videofile(
                arquivo_saida,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile=os.path.join(self.pasta_temp, f"temp_audio_{plataforma}.m4a"),
                remove_temp=True,
                threads=4,
                preset="medium"
            )
            
            # Fechar para liberar recursos
            video.close()
            
            logger.info(f"Vídeo processado para {plataforma}: {arquivo_saida}")
            return arquivo_saida
            
        except Exception as e:
            logger.error(f"Erro ao processar vídeo para {plataforma}: {str(e)}")
            return None
    
    def _redimensionar_video(self, video, resolucao_alvo):
        """Redimensiona o vídeo para a resolução alvo mantendo a proporção"""
        largura_alvo, altura_alvo = resolucao_alvo
        
        # Obter dimensões atuais
        largura_atual, altura_atual = video.size
    
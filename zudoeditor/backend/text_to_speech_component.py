#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Componente de Conversão Texto-Fala (TTS) para o ZudoEditor
Este módulo implementa diferentes opções de conversão de texto para fala,
priorizando soluções gratuitas e funcionais.
"""

import os
import sys
import time
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zudo_tts')

class TTSEngine:
    """Classe base para todos os motores de TTS."""
    
    def __init__(self, name: str, requires_internet: bool = False):
        """
        Inicializa o motor TTS.
        
        Args:
            name: Nome do motor TTS
            requires_internet: Se o motor requer conexão com internet
        """
        self.name = name
        self.requires_internet = requires_internet
        self.available_voices = []
        self.default_voice = None
        logger.info(f"Inicializando motor TTS: {name}")
    
    def is_available(self) -> bool:
        """Verifica se o motor está disponível no sistema."""
        return True
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Retorna a lista de vozes disponíveis."""
        return self.available_voices
    
    def set_voice(self, voice_id: str) -> bool:
        """
        Define a voz a ser usada.
        
        Args:
            voice_id: Identificador da voz
            
        Returns:
            bool: True se a voz foi definida com sucesso, False caso contrário
        """
        if not voice_id:
            return False
        
        for voice in self.available_voices:
            if voice['id'] == voice_id:
                self.default_voice = voice_id
                return True
        
        return False
    
    def synthesize(self, text: str, output_file: str, voice_id: str = None) -> str:
        """
        Sintetiza o texto em fala e salva em um arquivo.
        
        Args:
            text: Texto a ser convertido em fala
            output_file: Caminho para o arquivo de saída
            voice_id: ID da voz a ser usada (opcional)
            
        Returns:
            str: Caminho para o arquivo de áudio gerado
        """
        raise NotImplementedError("Método deve ser implementado pelas subclasses")


class PyttsxEngine(TTSEngine):
    """Motor TTS usando pyttsx3 (offline, multiplataforma)."""
    
    def __init__(self):
        """Inicializa o motor pyttsx3."""
        super().__init__("pyttsx3", requires_internet=False)
        self._engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Inicializa o motor pyttsx3."""
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            
            # Obter vozes disponíveis
            voices = self._engine.getProperty('voices')
            self.available_voices = [
                {
                    'id': str(i),
                    'name': voice.name,
                    'gender': 'male' if 'male' in voice.name.lower() else 'female',
                    'language': voice.languages[0] if voice.languages else 'unknown'
                }
                for i, voice in enumerate(voices)
            ]
            
            if self.available_voices:
                self.default_voice = self.available_voices[0]['id']
            
            logger.info(f"Motor pyttsx3 inicializado com {len(self.available_voices)} vozes")
            return True
        except ImportError:
            logger.warning("pyttsx3 não está instalado. Use 'pip install pyttsx3' para instalar.")
            return False
        except Exception as e:
            logger.error(f"Erro ao inicializar pyttsx3: {e}")
            return False
    
    def is_available(self) -> bool:
        """Verifica se o pyttsx3 está disponível."""
        try:
            import pyttsx3
            return self._engine is not None
        except ImportError:
            return False
    
    def set_voice(self, voice_id: str) -> bool:
        """Define a voz a ser usada."""
        if not super().set_voice(voice_id):
            return False
        
        try:
            voice_idx = int(voice_id)
            voices = self._engine.getProperty('voices')
            if 0 <= voice_idx < len(voices):
                self._engine.setProperty('voice', voices[voice_idx].id)
                return True
        except (ValueError, IndexError) as e:
            logger.error(f"Erro ao definir voz: {e}")
        
        return False
    
    def synthesize(self, text: str, output_file: str, voice_id: str = None) -> str:
        """Sintetiza o texto em fala usando pyttsx3."""
        if not self._engine:
            if not self._init_engine():
                return None
        
        if voice_id:
            self.set_voice(voice_id)
        
        try:
            # Garantir que o diretório de saída existe
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Configurar taxa de fala (pode ser ajustada)
            self._engine.setProperty('rate', 150)  # 150 palavras por minuto
            
            # Salvar para arquivo
            self._engine.save_to_file(text, output_file)
            self._engine.runAndWait()
            
            if os.path.exists(output_file):
                logger.info(f"Áudio gerado com sucesso: {output_file}")
                return output_file
            else:
                logger.error(f"Falha ao gerar arquivo de áudio: {output_file}")
                return None
        except Exception as e:
            logger.error(f"Erro ao sintetizar fala com pyttsx3: {e}")
            return None


class EdgeTTSEngine(TTSEngine):
    """Motor TTS usando edge-tts (Microsoft Edge TTS, requer internet)."""
    
    def __init__(self):
        """Inicializa o motor edge-tts."""
        super().__init__("edge-tts", requires_internet=True)
        self._voices = []
        self._init_engine()
    
    def _init_engine(self):
        """Inicializa o motor edge-tts."""
        try:
            import edge_tts
            import asyncio
            
            # Obter vozes disponíveis (requer execução assíncrona)
            async def get_voices():
                return await edge_tts.list_voices()
            
            # Executar a função assíncrona
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._voices = loop.run_until_complete(get_voices())
            loop.close()
            
            # Formatar lista de vozes
            self.available_voices = [
                {
                    'id': voice["ShortName"],
                    'name': voice["FriendlyName"],
                    'gender': voice["Gender"],
                    'language': voice["Locale"]
                }
                for voice in self._voices
            ]
            
            # Definir vozes padrão para português e inglês
            pt_voices = [v for v in self.available_voices if v['language'].startswith('pt')]
            en_voices = [v for v in self.available_voices if v['language'].startswith('en')]
            
            if pt_voices:
                self.default_voice = pt_voices[0]['id']
            elif en_voices:
                self.default_voice = en_voices[0]['id']
            elif self.available_voices:
                self.default_voice = self.available_voices[0]['id']
            
            logger.info(f"Motor edge-tts inicializado com {len(self.available_voices)} vozes")
            return True
        except ImportError:
            logger.warning("edge-tts não está instalado. Use 'pip install edge-tts' para instalar.")
            return False
        except Exception as e:
            logger.error(f"Erro ao inicializar edge-tts: {e}")
            return False
    
    def is_available(self) -> bool:
        """Verifica se o edge-tts está disponível."""
        try:
            import edge_tts
            return len(self._voices) > 0
        except ImportError:
            return False
    
    def synthesize(self, text: str, output_file: str, voice_id: str = None) -> str:
        """Sintetiza o texto em fala usando edge-tts."""
        try:
            import edge_tts
            import asyncio
            
            # Usar voz especificada ou padrão
            voice = voice_id if voice_id else self.default_voice
            
            # Se nenhuma voz estiver disponível, usar uma voz em inglês
            if not voice:
                voice = "en-US-ChristopherNeural"
            
            # Função assíncrona para sintetizar fala
            async def synthesize_speech():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file)
            
            # Executar a função assíncrona
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(synthesize_speech())
            loop.close()
            
            if os.path.exists(output_file):
                logger.info(f"Áudio gerado com sucesso: {output_file}")
                return output_file
            else:
                logger.error(f"Falha ao gerar arquivo de áudio: {output_file}")
                return None
        except ImportError:
            logger.error("edge-tts não está instalado. Use 'pip install edge-tts' para instalar.")
            return None
        except Exception as e:
            logger.error(f"Erro ao sintetizar fala com edge-tts: {e}")
            return None


class GTTSEngine(TTSEngine):
    """Motor TTS usando gTTS (Google Text-to-Speech, requer internet)."""
    
    def __init__(self):
        """Inicializa o motor gTTS."""
        super().__init__("gTTS", requires_internet=True)
        self._init_engine()
    
    def _init_engine(self):
        """Inicializa o motor gTTS."""
        try:
            from gtts import gTTS
            from gtts.lang import tts_langs
            
            # Obter idiomas disponíveis
            langs = tts_langs()
            
            # Criar vozes "virtuais" (gTTS não tem vozes, apenas idiomas)
            self.available_voices = [
                {
                    'id': lang_code,
                    'name': f"{lang_name} (Google)",
                    'gender': 'neutral',
                    'language': lang_code
                }
                for lang_code, lang_name in langs.items()
            ]
            
            # Definir voz padrão para português ou inglês
            pt_voices = [v for v in self.available_voices if v['language'].startswith('pt')]
            en_voices = [v for v in self.available_voices if v['language'].startswith('en')]
            
            if pt_voices:
                self.default_voice = pt_voices[0]['id']
            elif en_voices:
                self.default_voice = en_voices[0]['id']
            elif self.available_voices:
                self.default_voice = self.available_voices[0]['id']
            
            logger.info(f"Motor gTTS inicializado com {len(self.available_voices)} idiomas")
            return True
        except ImportError:
            logger.warning("gTTS não está instalado. Use 'pip install gtts' para instalar.")
            return False
        except Exception as e:
            logger.error(f"Erro ao inicializar gTTS: {e}")
            return False
    
    def is_available(self) -> bool:
        """Verifica se o gTTS está disponível."""
        try:
            from gtts import gTTS
            return True
        except ImportError:
            return False
    
    def synthesize(self, text: str, output_file: str, voice_id: str = None) -> str:
        """Sintetiza o texto em fala usando gTTS."""
        try:
            from gtts import gTTS
            
            # Usar idioma especificado ou padrão
            lang = voice_id if voice_id else self.default_voice
            
            # Se nenhum idioma estiver disponível, usar inglês
            if not lang:
                lang = "en"
            
            # Criar objeto gTTS
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Garantir que o diretório de saída existe
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Salvar para arquivo
            tts.save(output_file)
            
            if os.path.exists(output_file):
                logger.info(f"Áudio gerado com sucesso: {output_file}")
                return output_file
            else:
                logger.error(f"Falha ao gerar arquivo de áudio: {output_file}")
                return None
        except ImportError:
            logger.error("gTTS não está instalado. Use 'pip install gtts' para instalar.")
            return None
        except Exception as e:
            logger.error(f"Erro ao sintetizar fala com gTTS: {e}")
            return None


class TTSManager:
    """Gerenciador de motores TTS."""
    
    def __init__(self, output_dir: str = None):
        """
        Inicializa o gerenciador TTS.
        
        Args:
            output_dir: Diretório para salvar os arquivos de áudio
        """
        self.engines = {}
        self.default_engine = None
        self.output_dir = output_dir or os.path.join(tempfile.gettempdir(), "zudo_tts")
        
        # Criar diretório de saída se não existir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Inicializar motores disponíveis
        self._init_engines()
    
    def _init_engines(self):
        """Inicializa todos os motores TTS disponíveis."""
        # Tentar inicializar edge-tts (melhor qualidade)
        edge_engine = EdgeTTSEngine()
        if edge_engine.is_available():
            self.engines[edge_engine.name] = edge_engine
            self.default_engine = edge_engine.name
        
        # Tentar inicializar pyttsx3 (offline)
        pyttsx_engine = PyttsxEngine()
        if pyttsx_engine.is_available():
            self.engines[pyttsx_engine.name] = pyttsx_engine
            if not self.default_engine:
                self.default_engine = pyttsx_engine.name
        
        # Tentar inicializar gTTS (requer internet)
        gtts_engine = GTTSEngine()
        if gtts_engine.is_available():
            self.engines[gtts_engine.name] = gtts_engine
            if not self.default_engine:
                self.default_engine = gtts_engine.name
        
        logger.info(f"Motores TTS disponíveis: {', '.join(self.engines.keys())}")
        if self.default_engine:
            logger.info(f"Motor TTS padrão: {self.default_engine}")
        else:
            logger.warning("Nenhum motor TTS disponível!")
    
    def get_available_engines(self) -> List[str]:
        """Retorna a lista de motores TTS disponíveis."""
        return list(self.engines.keys())
    
    def get_available_voices(self, engine_name: str = None) -> List[Dict[str, str]]:
        """
        Retorna a lista de vozes disponíveis para um motor específico ou para o motor padrão.
        
        Args:
            engine_name: Nome do motor TTS (opcional)
            
        Returns:
            List[Dict[str, str]]: Lista de vozes disponíveis
        """
        engine = self.engines.get(engine_name or self.default_engine)
        if engine:
            return engine.get_available_voices()
        return []
    
    def set_default_engine(self, engine_name: str) -> bool:
        """
        Define o motor TTS padrão.
        
        Args:
            engine_name: Nome do motor TTS
            
        Returns:
            bool: True se o motor foi definido com sucesso, False caso contrário
        """
        if engine_name in self.engines:
            self.default_engine = engine_name
            logger.info(f"Motor TTS padrão definido: {engine_name}")
            return True
        
        logger.warning(f"Motor TTS não disponível: {engine_name}")
        return False
    
    def set_voice(self, voice_id: str, engine_name: str = None) -> bool:
        """
        Define a voz a ser usada para um motor específico ou para o motor padrão.
        
        Args:
            voice_id: Identificador da voz
            engine_name: Nome do motor TTS (opcional)
            
        Returns:
            bool: True se a voz foi definida com sucesso, False caso contrário
        """
        engine = self.engines.get(engine_name or self.default_engine)
        if engine:
            return engine.set_voice(voice_id)
        return False
    
    def synthesize(self, text: str, output_file: str = None, engine_name: str = None, voice_id: str = None) -> str:
        """
        Sintetiza o texto em fala usando o motor especificado ou o motor padrão.
        
        Args:
            text: Texto a ser convertido em fala
            output_file: Caminho para o arquivo de saída (opcional)
            engine_name: Nome do motor TTS (opcional)
            voice_id: ID da voz a ser usada (opcional)
            
        Returns:
            str: Caminho para o arquivo de áudio gerado
        """
        # Verificar se há algum motor disponível
        if not self.default_engine:
            logger.error("Nenhum motor TTS disponível!")
            return None
        
        # Usar motor especificado ou padrão
        engine = self.engines.get(engine_name or self.default_engine)
        if not engine:
            logger.error(f"Motor TTS não disponível: {engine_name}")
            return None
        
        # Gerar nome de arquivo se não especificado
        if not output_file:
            timestamp = int(time.time())
            output_file = os.path.join(self.output_dir, f"tts_{timestamp}.mp3")
        
        # Sintetizar texto em fala
        return engine.synthesize(text, output_file, voice_id)


# Função de teste
def test_tts_manager():
    """Testa o gerenciador TTS."""
    manager = TTSManager()
    
    print("Motores TTS disponíveis:")
    for engine_name in manager.get_available_engines():
        print(f"- {engine_name}")
    
    if not manager.default_engine:
        print("Nenhum motor TTS disponível!")
        return
    
    print(f"\nMotor TTS padrão: {manager.default_engine}")
    
    print("\nVozes disponíveis:")
    voices = manager.get_available_voices()
    for i, voice in enumerate(voices[:5]):  # Mostrar apenas as 5 primeiras vozes
        print(f"- {voice['id']}: {voice['name']} ({voice['language']})")
    
    if voices:
        print(f"\nTotal de vozes: {len(voices)}")
        
        # Testar síntese com a primeira voz
        test_text = "Este é um teste do sistema de conversão de texto para fala do ZudoEditor."
        output_file = os.path.join(tempfile.gettempdir(), "zudo_tts_test.mp3")
        
        print(f"\nSintetizando texto: '{test_text}'")
        result = manager.synthesize(test_text, output_file, voice_id=voices[0]['id'])
        
        if result:
            print(f"Áudio gerado com sucesso: {result}")
        else:
            print("Falha ao gerar áudio!")


if __name__ == "__main__":
    test_tts_manager()

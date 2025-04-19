#!/usr/bin/env python3
"""
Automação de Upload para Sistema de Automação de Vídeos

Este script gerencia o upload automático de vídeos processados para
múltiplas plataformas sociais (YouTube, Instagram e TikTok).

Uso:
    python automacao_upload.py --pasta_videos /caminho/para/videos --config /caminho/para/config.json
"""

import os
import sys
import json
import time
import random
import argparse
import logging
from datetime import datetime

# Módulos externos
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')  # modo invisível
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automacao_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutomacaoUpload")

# Configurações padrão
CONFIG_PADRAO = {
    "contas": {
        "youtube": [],
        "instagram": [],
        "tiktok": []
    },
    "proxies": [],
    "horarios_otimos": {
        "youtube": [
            {"dia": "todos", "hora": 15, "minuto": 0},
            {"dia": "todos", "hora": 18, "minuto": 0},
            {"dia": "fim_de_semana", "hora": 10, "minuto": 0}
        ],
        "instagram": [
            {"dia": "todos", "hora": 12, "minuto": 0},
            {"dia": "todos", "hora": 18, "minuto": 0},
            {"dia": "todos", "hora": 21, "minuto": 0}
        ],
        "tiktok": [
            {"dia": "todos", "hora": 9, "minuto": 0},
            {"dia": "todos", "hora": 15, "minuto": 0},
            {"dia": "todos", "hora": 19, "minuto": 0}
        ]
    },
    "limites_diarios": {
        "youtube": 5,
        "instagram": 3,
        "tiktok": 5
    },
    "intervalo_entre_uploads": {
        "youtube": 3600,
        "instagram": 7200,
        "tiktok": 3600
    },
    "tempo_espera_entre_acoes": {
        "min": 1,
        "max": 3
    },
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
}

class GerenciadorUpload:
    def __init__(self, pasta_videos, config_path):
        self.pasta_videos = pasta_videos
        self.config_path = config_path
        self.config = self._carregar_config()
        self.status_path = os.path.join(os.path.dirname(config_path), "status_upload.json")
        self.status = self._carregar_status()

    def _carregar_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                config_completa = CONFIG_PADRAO.copy()
                for chave, valor in config.items():
                    if isinstance(valor, dict) and chave in config_completa and isinstance(config_completa[chave], dict):
                        config_completa[chave].update(valor)
                    else:
                        config_completa[chave] = valor
                return config_completa
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {self.config_path}")
                return CONFIG_PADRAO
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            return CONFIG_PADRAO

    def _carregar_status(self):
        try:
            if os.path.exists(self.status_path):
                with open(self.status_path, "r") as f:
                    return json.load(f)
            else:
                status_inicial = {
                    "uploads": {},
                    "contas": {"youtube": {}, "instagram": {}, "tiktok": {}},
                    "ultima_atualizacao": datetime.now().isoformat()
                }
                self._salvar_status(status_inicial)
                return status_inicial
        except Exception as e:
            logger.error(f"Erro ao carregar status: {str(e)}")
            return {"uploads": {}, "contas": {"youtube": {}, "instagram": {}, "tiktok": {}}, "ultima_atualizacao": datetime.now().isoformat()}

    def _salvar_status(self, status=None):
        try:
            if status is None:
                status = self.status
            status["ultima_atualizacao"] = datetime.now().isoformat()
            with open(self.status_path, "w") as f:
                json.dump(status, f, indent=4)
        except Exception as e:
            logger.error(f"Erro ao salvar status: {str(e)}")

    def _verificar_limites_diarios(self, plataforma, usuario):
        try:
            limite = self.config["limites_diarios"].get(plataforma, 5)
            data_atual = datetime.now().strftime("%Y-%m-%d")
            contador = 0
            for video_id, plataformas in self.status["uploads"].items():
                if plataforma in plataformas and usuario in plataformas[plataforma]:
                    upload_info = plataformas[plataforma][usuario]
                    if upload_info.get("status") == "concluido" and upload_info.get("data_upload", "").startswith(data_atual):
                        contador += 1
            return contador < limite
        except Exception as e:
            logger.error(f"Erro ao verificar limites diários: {str(e)}")
            return True

    def _verificar_intervalo_entre_uploads(self, plataforma, usuario):
        try:
            intervalo = self.config["intervalo_entre_uploads"].get(plataforma, 3600)
            agora = datetime.now()
            ultimo_upload = None
            for video_id, plataformas in self.status["uploads"].items():
                if plataforma in plataformas and usuario in plataformas[plataforma]:
                    upload_info = plataformas[plataforma][usuario]
                    if upload_info.get("status") == "concluido" and "data_upload" in upload_info:
                        data_upload = datetime.fromisoformat(upload_info["data_upload"])
                        if ultimo_upload is None or data_upload > ultimo_upload:
                            ultimo_upload = data_upload
            if ultimo_upload is None:
                return True
            return (agora - ultimo_upload).total_seconds() >= intervalo
        except Exception as e:
            logger.error(f"Erro ao verificar intervalo: {str(e)}")
            return True

    def processar_uploads(self):
        try:
            logger.info("Iniciando processamento de uploads...")
            videos_pendentes = self._obter_videos_pendentes()
            if not videos_pendentes:
                logger.info("Nenhum vídeo pendente para upload.")
                return
            for video in videos_pendentes:
                plataforma = video["plataforma"]
                conta = video["conta"]
                usuario = conta["usuario"]

                if not self._verificar_limites_diarios(plataforma, usuario):
                    logger.warning(f"Limite diário atingido para {usuario} em {plataforma}.")
                    continue

                if not self._verificar_intervalo_entre_uploads(plataforma, usuario):
                    logger.warning(f"Intervalo mínimo não respeitado para {usuario} em {plataforma}.")
                    continue

                self._atualizar_status_upload(
                    video["id"], plataforma, usuario,
                    {"status": "pendente", "arquivo": video["arquivo"], "tentativas": 0}
                )

                proxy = self._selecionar_proxy()
                logger.info(f"Iniciando upload para {plataforma} com conexão segura")

        except Exception as e:
            logger.error(f"Erro durante o processamento dos uploads: {str(e)}")

AutomacaoUpload = GerenciadorUpload

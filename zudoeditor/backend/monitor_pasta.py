#!/usr/bin/env python3
"""
Monitor de Pasta para Sistema de Automação de Vídeos

Este script monitora uma pasta específica para novos arquivos de vídeo,
verifica se são formatos válidos e os envia para processamento.

Uso:
    python monitor_pasta.py --pasta_entrada /caminho/para/pasta_entrada --pasta_saida /caminho/para/pasta_saida
"""

import os
import time
import argparse
import logging
import json
import shutil
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor_pasta.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MonitorPasta")

# Formatos de vídeo suportados
FORMATOS_SUPORTADOS = ['.mp4', '.mov', '.avi', '.wmv', '.mkv']

class ProcessadorFila:
    """Gerencia a fila de processamento de vídeos"""
    
    def __init__(self, pasta_saida):
        self.pasta_saida = pasta_saida
        self.fila = []
        self.processando = False
        
        # Criar pasta de saída se não existir
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
            logger.info(f"Pasta de saída criada: {pasta_saida}")
    
    def adicionar(self, arquivo):
        """Adiciona um arquivo à fila de processamento"""
        self.fila.append(arquivo)
        logger.info(f"Arquivo adicionado à fila: {arquivo}")
        
        # Iniciar processamento se não estiver em andamento
        if not self.processando:
            self.processar_proximo()
    
    def processar_proximo(self):
        """Processa o próximo arquivo na fila"""
        if not self.fila:
            self.processando = False
            return
        
        self.processando = True
        arquivo = self.fila.pop(0)
        
        try:
            logger.info(f"Iniciando processamento de: {arquivo}")
            
            # Criar pasta para este vídeo específico
            nome_base = os.path.basename(arquivo)
            nome_sem_ext, _ = os.path.splitext(nome_base)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta_video = os.path.join(self.pasta_saida, f"{nome_sem_ext}_{timestamp}")
            os.makedirs(pasta_video)
            
            # Copiar arquivo original para pasta de processamento
            arquivo_destino = os.path.join(pasta_video, nome_base)
            shutil.copy2(arquivo, arquivo_destino)
            
            # Criar arquivo de metadados
            metadados = {
                "arquivo_original": arquivo,
                "data_deteccao": datetime.now().isoformat(),
                "status": "detectado",
                "plataformas": ["youtube", "instagram", "tiktok"]
            }
            
            with open(os.path.join(pasta_video, "metadados.json"), "w") as f:
                json.dump(metadados, f, indent=4)
            
            # Iniciar processamento em segundo plano
            self._iniciar_processamento(arquivo_destino, pasta_video)
            
            logger.info(f"Arquivo preparado para processamento: {arquivo}")
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {arquivo}: {str(e)}")
        
        # Continuar com o próximo arquivo
        self.processar_proximo()
    
    def _iniciar_processamento(self, arquivo, pasta_saida):
        """Inicia o script de processamento em segundo plano"""
        try:
            # Aqui chamaríamos o script de processamento real
            # Para este exemplo, apenas simulamos chamando um script externo
            comando = [
                "python3", 
                "processador_video.py", 
                "--arquivo", arquivo, 
                "--pasta_saida", pasta_saida
            ]
            
            # Executar em segundo plano
            subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            logger.info(f"Processamento iniciado para: {arquivo}")
            
            # Atualizar metadados
            metadados_path = os.path.join(pasta_saida, "metadados.json")
            with open(metadados_path, "r") as f:
                metadados = json.load(f)
            
            metadados["status"] = "processando"
            metadados["inicio_processamento"] = datetime.now().isoformat()
            
            with open(metadados_path, "w") as f:
                json.dump(metadados, f, indent=4)
                
        except Exception as e:
            logger.error(f"Erro ao iniciar processamento: {str(e)}")


class ManipuladorArquivos(FileSystemEventHandler):
    """Manipula eventos de criação de arquivos na pasta monitorada"""
    
    def __init__(self, processador):
        self.processador = processador
        super().__init__()
    
    def on_created(self, event):
        """Chamado quando um arquivo é criado na pasta monitorada"""
        if event.is_directory:
            return
        
        caminho_arquivo = event.src_path
        
        # Verificar se é um formato de vídeo suportado
        _, extensao = os.path.splitext(caminho_arquivo)
        if extensao.lower() not in FORMATOS_SUPORTADOS:
            logger.info(f"Arquivo ignorado (formato não suportado): {caminho_arquivo}")
            return
        
        # Verificar se o arquivo está completo (não está sendo copiado)
        self._esperar_arquivo_completo(caminho_arquivo)
        
        # Verificar se o arquivo é um vídeo válido
        if self._validar_video(caminho_arquivo):
            # Adicionar à fila de processamento
            self.processador.adicionar(caminho_arquivo)
        else:
            logger.warning(f"Arquivo inválido ou corrompido: {caminho_arquivo}")
    
    def _esperar_arquivo_completo(self, caminho_arquivo):
        """Espera até que o arquivo esteja completamente copiado"""
        tamanho_anterior = -1
        tamanho_atual = os.path.getsize(caminho_arquivo)
        
        # Enquanto o tamanho estiver mudando, o arquivo ainda está sendo copiado
        while tamanho_atual != tamanho_anterior:
            tamanho_anterior = tamanho_atual
            time.sleep(1)  # Esperar 1 segundo
            try:
                tamanho_atual = os.path.getsize(caminho_arquivo)
            except FileNotFoundError:
                # Arquivo pode ter sido removido
                logger.warning(f"Arquivo removido durante cópia: {caminho_arquivo}")
                return False
        
        # Esperar mais um pouco para garantir que o sistema de arquivos esteja estável
        time.sleep(2)
        return True
    
    def _validar_video(self, caminho_arquivo):
        """Verifica se o arquivo é um vídeo válido usando ffprobe"""
        try:
            resultado = subprocess.run(
                ["ffprobe", "-v", "error", caminho_arquivo],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Se o código de saída for 0, o arquivo é um vídeo válido
            return resultado.returncode == 0
            
        except Exception as e:
            logger.error(f"Erro ao validar vídeo {caminho_arquivo}: {str(e)}")
            return False


def iniciar_monitoramento(pasta_entrada, pasta_saida):
    """Inicia o monitoramento da pasta de entrada"""
    
    # Verificar se a pasta de entrada existe
    if not os.path.exists(pasta_entrada):
        os.makedirs(pasta_entrada)
        logger.info(f"Pasta de entrada criada: {pasta_entrada}")
    
    # Criar processador de fila
    processador = ProcessadorFila(pasta_saida)
    
    # Configurar manipulador de eventos
    manipulador = ManipuladorArquivos(processador)
    
    # Configurar observador
    observador = Observer()
    observador.schedule(manipulador, pasta_entrada, recursive=False)
    observador.start()
    
    logger.info(f"Monitoramento iniciado na pasta: {pasta_entrada}")
    logger.info(f"Arquivos processados serão salvos em: {pasta_saida}")
    
    try:
        # Processar arquivos existentes na pasta
        for arquivo in os.listdir(pasta_entrada):
            caminho_completo = os.path.join(pasta_entrada, arquivo)
            if os.path.isfile(caminho_completo):
                _, extensao = os.path.splitext(caminho_completo)
                if extensao.lower() in FORMATOS_SUPORTADOS:
                    if manipulador._validar_video(caminho_completo):
                        processador.adicionar(caminho_completo)
        
        # Manter o script em execução
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Monitoramento interrompido pelo usuário")
        observador.stop()
    
    observador.join()


if __name__ == "__main__":
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Monitor de pasta para sistema de automação de vídeos")
    parser.add_argument("--pasta_entrada", required=True, help="Caminho para a pasta de entrada")
    parser.add_argument("--pasta_saida", required=True, help="Caminho para a pasta de saída")
    
    args = parser.parse_args()
    
    # Iniciar monitoramento
    iniciar_monitoramento(args.pasta_entrada, args.pasta_saida)

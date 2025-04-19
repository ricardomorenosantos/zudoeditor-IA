#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZudoEditor - Painel de Controle Integrado
Este módulo implementa a interface gráfica do ZudoEditor com integração completa
aos componentes de backend para geração, edição e publicação de vídeos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import queue
import time
import json
import subprocess

# Adicionar diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Tentar importar módulos do backend
try:
    from backend.video_generator_module import VideoGenerator, VideoGeneratorConfig
    from backend.processador_video import ProcessadorVideo
    from backend.automacao_upload import AutomacaoUpload
    BACKEND_IMPORTS_OK = True
except ImportError as e:
    print(f"Aviso: Não foi possível importar módulos do backend: {e}")
    print("O painel funcionará em modo limitado.")
    BACKEND_IMPORTS_OK = False

class ZudoEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZudoEditor - Painel de Comando")
        self.root.geometry("900x700")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TFrame", background="#ffffff")
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criar abas
        self.tab_gerar = ttk.Frame(self.notebook)
        self.tab_editar = ttk.Frame(self.notebook)
        self.tab_publicar = ttk.Frame(self.notebook)
        self.tab_automatico = ttk.Frame(self.notebook)
        self.tab_config = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_gerar, text="Gerar Vídeo")
        self.notebook.add(self.tab_editar, text="Editar Vídeo")
        self.notebook.add(self.tab_publicar, text="Publicar")
        self.notebook.add(self.tab_automatico, text="Fluxo Automático")
        self.notebook.add(self.tab_config, text="Configurações")
        
        # Inicializar variáveis de controle
        self.fila_processamento = queue.Queue()
        self.processando = False
        self.tempo_inicio = 0
        
        # Obter diretório raiz do projeto
        self.dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Inicializar componentes
        self.inicializar_aba_gerar()
        self.inicializar_aba_editar()
        self.inicializar_aba_publicar()
        self.inicializar_aba_automatico()
        self.inicializar_aba_config()
        
        # Barra de status
        self.frame_status = ttk.Frame(root)
        self.frame_status.pack(fill=tk.X, padx=10, pady=5)
        
        self.label_status = ttk.Label(self.frame_status, text="Pronto")
        self.label_status.pack(side=tk.LEFT)
        
        # Carregar configurações
        self.carregar_configuracoes()
        
        # Inicializar componentes do backend
        if BACKEND_IMPORTS_OK:
            self.inicializar_backend()
        else:
            self.atualizar_status("Backend não disponível. Funcionalidade limitada.", erro=True)
    
    def inicializar_backend(self):
        """Inicializa os componentes do backend"""
        try:
            # Configuração para o gerador de vídeos
            config = VideoGeneratorConfig(
                output_dir=os.path.join(self.dir_raiz, "saida"),
                input_dir=os.path.join(self.dir_raiz, "entrada")
            )
            
            # Inicializar gerador de vídeos
            self.video_generator = VideoGenerator(config)
            
            # Carregar opções disponíveis
            self.carregar_opcoes_tts()
            self.carregar_opcoes_fundo()
            self.carregar_opcoes_legenda()
            
            self.atualizar_status("Backend inicializado com sucesso")
        except Exception as e:
            self.atualizar_status(f"Erro ao inicializar backend: {str(e)}", erro=True)
    
    def inicializar_aba_gerar(self):
        """Inicializa a aba de geração de vídeo"""
        frame = ttk.Frame(self.tab_gerar, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Geração de Vídeo com IA", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Área de texto para roteiro
        ttk.Label(frame, text="Digite o roteiro para o vídeo:").pack(anchor=tk.W)
        self.campo_texto = tk.Text(frame, height=10, width=80, wrap=tk.WORD)
        self.campo_texto.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame para opções de TTS
        frame_tts = ttk.LabelFrame(frame, text="Opções de Voz", padding=10)
        frame_tts.pack(fill=tk.X, pady=5)
        
        # Motor TTS
        ttk.Label(frame_tts, text="Motor TTS:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.motor_tts = tk.StringVar()
        self.combo_motor_tts = ttk.Combobox(frame_tts, textvariable=self.motor_tts, state="readonly")
        self.combo_motor_tts.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.combo_motor_tts.bind("<<ComboboxSelected>>", self.atualizar_vozes)
        
        # Voz
        ttk.Label(frame_tts, text="Voz:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.voz_tts = tk.StringVar()
        self.combo_voz_tts = ttk.Combobox(frame_tts, textvariable=self.voz_tts, state="readonly", width=40)
        self.combo_voz_tts.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame para opções de fundo
        frame_fundo = ttk.LabelFrame(frame, text="Opções de Fundo", padding=10)
        frame_fundo.pack(fill=tk.X, pady=5)
        
        # Tipo de fundo
        ttk.Label(frame_fundo, text="Tipo de Fundo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tipo_fundo = tk.StringVar()
        self.combo_tipo_fundo = ttk.Combobox(frame_fundo, textvariable=self.tipo_fundo, state="readonly")
        self.combo_tipo_fundo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.combo_tipo_fundo.bind("<<ComboboxSelected>>", self.atualizar_opcoes_fundo)
        
        # Fonte do fundo
        ttk.Label(frame_fundo, text="Fonte do Fundo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.fonte_fundo = tk.StringVar()
        self.combo_fonte_fundo = ttk.Combobox(frame_fundo, textvariable=self.fonte_fundo, state="readonly", width=40)
        self.combo_fonte_fundo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame para opções de legenda
        frame_legenda = ttk.LabelFrame(frame, text="Opções de Legenda", padding=10)
        frame_legenda.pack(fill=tk.X, pady=5)
        
        # Estilo de legenda
        ttk.Label(frame_legenda, text="Estilo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.estilo_legenda = tk.StringVar()
        self.combo_estilo_legenda = ttk.Combobox(frame_legenda, textvariable=self.estilo_legenda, state="readonly")
        self.combo_estilo_legenda.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Posição de legenda
        ttk.Label(frame_legenda, text="Posição:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.posicao_legenda = tk.StringVar()
        self.combo_posicao_legenda = ttk.Combobox(frame_legenda, textvariable=self.posicao_legenda, state="readonly")
        self.combo_posicao_legenda.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Botão de geração
        self.botao_gerar = ttk.Button(frame, text="🎥 Gerar Vídeo com IA", command=self.gerar_video)
        self.botao_gerar.pack(pady=10)
        
        # Barra de progresso
        self.progresso_gerar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progresso_gerar.pack(fill=tk.X, pady=5)
        
        # Tempo estimado
        self.label_tempo_gerar = ttk.Label(frame, text="Tempo estimado: 3-8 minutos")
        self.label_tempo_gerar.pack(pady=5)
        
        # Informações de tempo de processamento
        frame_info = ttk.LabelFrame(frame, text="Informações de Tempo de Processamento", padding=10)
        frame_info.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_info, text="• Conversão de texto para fala: 1-2 minutos para 500 palavras").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Seleção e preparação de fundo: 30-60 segundos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Sincronização de legendas: 1-2 minutos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Renderização final: 1-3 minutos para vídeo de 1-2 minutos").pack(anchor=tk.W)
        
        # Preencher com valores padrão
        if not BACKEND_IMPORTS_OK:
            # Valores fictícios para demonstração
            self.combo_motor_tts['values'] = ["pyttsx3", "edge-tts", "gtts"]
            self.motor_tts.set("pyttsx3")
            
            self.combo_voz_tts['values'] = ["pt_BR_1 - Português Brasil (Masculino)", "pt_BR_2 - Português Brasil (Feminino)"]
            self.voz_tts.set("pt_BR_1 - Português Brasil (Masculino)")
            
            self.combo_tipo_fundo['values'] = ["solid_color", "gradient", "image", "video"]
            self.tipo_fundo.set("solid_color")
            
            self.combo_fonte_fundo['values'] = ["azul", "verde", "cinza", "gradiente_azul"]
            self.fonte_fundo.set("azul")
            
            self.combo_estilo_legenda['values'] = ["modern", "classic", "subtitle", "caption"]
            self.estilo_legenda.set("modern")
            
            self.combo_posicao_legenda['values'] = ["bottom", "top", "middle"]
            self.posicao_legenda.set("bottom")
    
    def inicializar_aba_editar(self):
        """Inicializa a aba de edição de vídeo"""
        frame = ttk.Frame(self.tab_editar, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Edição Automática de Vídeo", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Lista de vídeos disponíveis
        ttk.Label(frame, text="Vídeos disponíveis para edição:").pack(anchor=tk.W)
        
        # Frame para lista e botões
        frame_lista = ttk.Frame(frame)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Lista de vídeos
        self.lista_videos = tk.Listbox(frame_lista, height=10, width=80)
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.lista_videos.yview)
        self.lista_videos.configure(yscrollcommand=scrollbar.set)
        
        self.lista_videos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para atualizar lista
        ttk.Button(frame, text="🔄 Atualizar Lista", command=self.atualizar_lista_videos).pack(pady=5)
        
        # Frame para opções de edição
        frame_opcoes = ttk.LabelFrame(frame, text="Opções de Edição", padding=10)
        frame_opcoes.pack(fill=tk.X, pady=5)
        
        # Plataformas
        ttk.Label(frame_opcoes, text="Plataformas:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Checkboxes para plataformas
        self.plataforma_youtube = tk.BooleanVar(value=True)
        self.plataforma_instagram = tk.BooleanVar(value=True)
        self.plataforma_tiktok = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(frame_opcoes, text="YouTube", variable=self.plataforma_youtube).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="Instagram", variable=self.plataforma_instagram).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="TikTok", variable=self.plataforma_tiktok).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Botão de edição
        self.botao_editar = ttk.Button(frame, text="✂️ Editar Vídeo Automaticamente", command=self.editar_video)
        self.botao_editar.pack(pady=10)
        
        # Barra de progresso
        self.progresso_editar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progresso_editar.pack(fill=tk.X, pady=5)
        
        # Tempo estimado
        self.label_tempo_editar = ttk.Label(frame, text="Tempo estimado: 2-5 minutos por plataforma")
        self.label_tempo_editar.pack(pady=5)
        
        # Informações de tempo de processamento
        frame_info = ttk.LabelFrame(frame, text="Informações de Tempo de Processamento", padding=10)
        frame_info.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_info, text="• Análise do vídeo: 30-60 segundos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Processamento de legendas: 1-2 minutos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Aplicação de filtros: 30-60 segundos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Adaptação para plataformas: 1-2 minutos por plataforma").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Renderização final: 1-3 minutos por plataforma").pack(anchor=tk.W)
    
    def inicializar_aba_publicar(self):
        """Inicializa a aba de publicação de vídeo"""
        frame = ttk.Frame(self.tab_publicar, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Publicação Automática nas Redes Sociais", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Lista de vídeos editados
        ttk.Label(frame, text="Vídeos editados disponíveis para publicação:").pack(anchor=tk.W)
        
        # Frame para lista e botões
        frame_lista = ttk.Frame(frame)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Lista de vídeos
        self.lista_videos_editados = tk.Listbox(frame_lista, height=10, width=80)
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.lista_videos_editados.yview)
        self.lista_videos_editados.configure(yscrollcommand=scrollbar.set)
        
        self.lista_videos_editados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para atualizar lista
        ttk.Button(frame, text="🔄 Atualizar Lista", command=self.atualizar_lista_videos_editados).pack(pady=5)
        
        # Frame para opções de publicação
        frame_opcoes = ttk.LabelFrame(frame, text="Opções de Publicação", padding=10)
        frame_opcoes.pack(fill=tk.X, pady=5)
        
        # Plataformas para publicação
        ttk.Label(frame_opcoes, text="Publicar em:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Checkboxes para plataformas
        self.publicar_youtube = tk.BooleanVar(value=True)
        self.publicar_instagram = tk.BooleanVar(value=True)
        self.publicar_tiktok = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(frame_opcoes, text="YouTube", variable=self.publicar_youtube).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="Instagram", variable=self.publicar_instagram).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="TikTok", variable=self.publicar_tiktok).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Título e descrição
        ttk.Label(frame_opcoes, text="Título:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.titulo_video = tk.StringVar()
        ttk.Entry(frame_opcoes, textvariable=self.titulo_video, width=50).grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(frame_opcoes, text="Descrição:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.descricao_video = tk.Text(frame_opcoes, height=4, width=50)
        self.descricao_video.grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Botão de publicação
        self.botao_publicar = ttk.Button(frame, text="🚀 Publicar nas Redes Sociais", command=self.publicar_video)
        self.botao_publicar.pack(pady=10)
        
        # Barra de progresso
        self.progresso_publicar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progresso_publicar.pack(fill=tk.X, pady=5)
        
        # Tempo estimado
        self.label_tempo_publicar = ttk.Label(frame, text="Tempo estimado: 2-5 minutos para todas as plataformas")
        self.label_tempo_publicar.pack(pady=5)
        
        # Informações de tempo de processamento
        frame_info = ttk.LabelFrame(frame, text="Informações de Tempo de Processamento", padding=10)
        frame_info.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_info, text="• Preparação de metadados: 20-30 segundos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Upload para plataformas: 1-3 minutos por plataforma").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Verificação de políticas: 30-60 segundos").pack(anchor=tk.W)
    
    def inicializar_aba_automatico(self):
        """Inicializa a aba de fluxo automático"""
        frame = ttk.Frame(self.tab_automatico, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Fluxo de Trabalho Automático", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Descrição
        ttk.Label(frame, text="Configure e execute o fluxo de trabalho completo: Geração > Edição > Publicação").pack(pady=5)
        
        # Frame para entrada de texto
        frame_texto = ttk.LabelFrame(frame, text="Roteiro do Vídeo", padding=10)
        frame_texto.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_automatico = tk.Text(frame_texto, height=8, width=80, wrap=tk.WORD)
        self.texto_automatico.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame para opções
        frame_opcoes = ttk.LabelFrame(frame, text="Opções do Fluxo", padding=10)
        frame_opcoes.pack(fill=tk.X, pady=5)
        
        # Checkboxes para etapas
        self.auto_gerar = tk.BooleanVar(value=True)
        self.auto_editar = tk.BooleanVar(value=True)
        self.auto_publicar = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(frame_opcoes, text="Gerar Vídeo", variable=self.auto_gerar).grid(row=0, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Checkbutton(frame_opcoes, text="Editar Vídeo", variable=self.auto_editar).grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
        ttk.Checkbutton(frame_opcoes, text="Publicar Vídeo", variable=self.auto_publicar).grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)
        
        # Plataformas
        ttk.Label(frame_opcoes, text="Plataformas:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Checkboxes para plataformas
        self.auto_youtube = tk.BooleanVar(value=True)
        self.auto_instagram = tk.BooleanVar(value=True)
        self.auto_tiktok = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(frame_opcoes, text="YouTube", variable=self.auto_youtube).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="Instagram", variable=self.auto_instagram).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Checkbutton(frame_opcoes, text="TikTok", variable=self.auto_tiktok).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Botão de execução
        self.botao_executar = ttk.Button(frame, text="▶️ Executar Fluxo Completo", command=self.executar_fluxo_automatico)
        self.botao_executar.pack(pady=10)
        
        # Barra de progresso geral
        ttk.Label(frame, text="Progresso Geral:").pack(anchor=tk.W, pady=(10, 0))
        self.progresso_geral = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progresso_geral.pack(fill=tk.X, pady=5)
        
        # Barras de progresso para cada etapa
        frame_progresso = ttk.Frame(frame)
        frame_progresso.pack(fill=tk.X, pady=5)
        
        # Geração
        ttk.Label(frame_progresso, text="Geração:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.progresso_auto_gerar = ttk.Progressbar(frame_progresso, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progresso_auto_gerar.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        
        # Edição
        ttk.Label(frame_progresso, text="Edição:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.progresso_auto_editar = ttk.Progressbar(frame_progresso, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progresso_auto_editar.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        
        # Publicação
        ttk.Label(frame_progresso, text="Publicação:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.progresso_auto_publicar = ttk.Progressbar(frame_progresso, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progresso_auto_publicar.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        
        # Configurar grid
        frame_progresso.columnconfigure(1, weight=1)
        
        # Status e tempo
        self.label_status_auto = ttk.Label(frame, text="Status: Pronto")
        self.label_status_auto.pack(anchor=tk.W, pady=5)
        
        self.label_tempo_auto = ttk.Label(frame, text="Tempo estimado total: 10-20 minutos")
        self.label_tempo_auto.pack(anchor=tk.W, pady=5)
        
        # Informações de tempo de processamento
        frame_info = ttk.LabelFrame(frame, text="Informações de Tempo de Processamento", padding=10)
        frame_info.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_info, text="• Tempo total estimado para o fluxo completo: 10-20 minutos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Geração de vídeo: 3-8 minutos").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Edição de vídeo: 2-5 minutos por plataforma").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Publicação: 2-5 minutos para todas as plataformas").pack(anchor=tk.W)
        ttk.Label(frame_info, text="• Os tempos variam de acordo com o tamanho do vídeo e as opções selecionadas").pack(anchor=tk.W)
    
    def inicializar_aba_config(self):
        """Inicializa a aba de configurações"""
        frame = ttk.Frame(self.tab_config, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Configurações do Sistema", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para configurações gerais
        frame_geral = ttk.LabelFrame(frame, text="Configurações Gerais", padding=10)
        frame_geral.pack(fill=tk.X, pady=5)
        
        # Diretórios
        ttk.Label(frame_geral, text="Diretório de Entrada:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dir_entrada = tk.StringVar()
        ttk.Entry(frame_geral, textvariable=self.dir_entrada, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(frame_geral, text="...", command=lambda: self.selecionar_diretorio(self.dir_entrada)).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame_geral, text="Diretório de Saída:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.dir_saida = tk.StringVar()
        ttk.Entry(frame_geral, textvariable=self.dir_saida, width=50).grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(frame_geral, text="...", command=lambda: self.selecionar_diretorio(self.dir_saida)).grid(row=1, column=2, padx=5, pady=5)
        
        # Configurar grid
        frame_geral.columnconfigure(1, weight=1)
        
        # Frame para configurações de API
        frame_api = ttk.LabelFrame(frame, text="Configurações de API", padding=10)
        frame_api.pack(fill=tk.X, pady=5)
        
        # YouTube API
        ttk.Label(frame_api, text="YouTube API Key:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.youtube_api = tk.StringVar()
        ttk.Entry(frame_api, textvariable=self.youtube_api, width=50).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Instagram API
        ttk.Label(frame_api, text="Instagram Token:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.instagram_api = tk.StringVar()
        ttk.Entry(frame_api, textvariable=self.instagram_api, width=50).grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # TikTok API
        ttk.Label(frame_api, text="TikTok API Key:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.tiktok_api = tk.StringVar()
        ttk.Entry(frame_api, textvariable=self.tiktok_api, width=50).grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Configurar grid
        frame_api.columnconfigure(1, weight=1)
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame_botoes, text="Salvar Configurações", command=self.salvar_configuracoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Restaurar Padrões", command=self.restaurar_configuracoes).pack(side=tk.LEFT, padx=5)
        
        # Informações de sistema
        frame_info = ttk.LabelFrame(frame, text="Informações do Sistema", padding=10)
        frame_info.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_info, text="Versão do ZudoEditor: 1.0.0").pack(anchor=tk.W)
        ttk.Label(frame_info, text=f"Diretório de Instalação: {self.dir_raiz}").pack(anchor=tk.W)
        
        # Botão para verificar dependências
        ttk.Button(frame, text="Verificar Dependências", command=self.verificar_dependencias).pack(pady=10)
    
    # Métodos de carregamento de opções
    
    def carregar_opcoes_tts(self):
        """Carrega as opções de TTS disponíveis"""
        try:
            # Obter motores disponíveis
            motores = self.video_generator.get_available_engines()
            self.combo_motor_tts['values'] = motores
            
            if motores:
                self.motor_tts.set(motores[0])
                self.atualizar_vozes()
        except Exception as e:
            self.atualizar_status(f"Erro ao carregar opções de TTS: {str(e)}", erro=True)
    
    def atualizar_vozes(self, event=None):
        """Atualiza a lista de vozes com base no motor selecionado"""
        try:
            # Obter vozes disponíveis
            vozes = self.video_generator.get_available_voices()
            
            # Filtrar por motor selecionado (se necessário)
            # Aqui você pode implementar a lógica para filtrar vozes por motor
            
            # Formatar para exibição
            opcoes_vozes = [f"{v['id']} - {v['name']} ({v['language']})" for v in vozes[:20]]  # Limitar a 20 para não sobrecarregar
            
            self.combo_voz_tts['values'] = opcoes_vozes
            
            if opcoes_vozes:
                self.voz_tts.set(opcoes_vozes[0])
        except Exception as e:
            self.atualizar_status(f"Erro ao atualizar vozes: {str(e)}", erro=True)
    
    def carregar_opcoes_fundo(self):
        """Carrega as opções de fundo disponíveis"""
        try:
            # Obter tipos de fundo disponíveis
            tipos = self.video_generator.get_available_background_types()
            self.combo_tipo_fundo['values'] = tipos
            
            if tipos:
                self.tipo_fundo.set(tipos[0])
                self.atualizar_opcoes_fundo()
        except Exception as e:
            self.atualizar_status(f"Erro ao carregar opções de fundo: {str(e)}", erro=True)
    
    def atualizar_opcoes_fundo(self, event=None):
        """Atualiza as opções de fonte de fundo com base no tipo selecionado"""
        try:
            tipo = self.tipo_fundo.get()
            opcoes = []
            
            if tipo == "solid_color":
                # Obter cores predefinidas
                cores = self.video_generator.get_predefined_colors()
                opcoes = list(cores.keys())
            elif tipo == "gradient":
                # Obter gradientes predefinidos
                gradientes = self.video_generator.get_predefined_gradients()
                opcoes = list(gradientes.keys())
            elif tipo == "image":
                # Obter imagens disponíveis
                imagens = self.video_generator.get_available_images()
                opcoes = [os.path.basename(img) for img in imagens]
            elif tipo == "video":
                # Obter vídeos disponíveis
                videos = self.video_generator.get_available_videos()
                opcoes = [os.path.basename(vid) for vid in videos]
            
            self.combo_fonte_fundo['values'] = opcoes
            
            if opcoes:
                self.fonte_fundo.set(opcoes[0])
        except Exception as e:
            self.atualizar_status(f"Erro ao atualizar opções de fundo: {str(e)}", erro=True)
    
    def carregar_opcoes_legenda(self):
        """Carrega as opções de legenda disponíveis"""
        try:
            # Obter estilos de legenda disponíveis
            estilos = self.video_generator.get_available_subtitle_styles()
            self.combo_estilo_legenda['values'] = estilos
            
            if estilos:
                self.estilo_legenda.set(estilos[0])
            
            # Definir posições de legenda
            posicoes = ["bottom", "top", "middle"]
            self.combo_posicao_legenda['values'] = posicoes
            
            if posicoes:
                self.posicao_legenda.set(posicoes[0])
        except Exception as e:
            self.atualizar_status(f"Erro ao carregar opções de legenda: {str(e)}", erro=True)
    
    # Métodos de funcionalidade
    
    def gerar_video(self):
        """Gera um vídeo a partir do texto inserido"""
        texto = self.campo_texto.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite um roteiro antes de gerar o vídeo.")
            return
        
        # Desabilitar botão durante o processamento
        self.botao_gerar.configure(state=tk.DISABLED)
        self.progresso_gerar.start()
        self.tempo_inicio = time.time()
        
        # Atualizar estimativa de tempo
        self.atualizar_estimativa_tempo("gerar", len(texto.split()))
        
        # Iniciar thread para não bloquear a interface
        threading.Thread(target=self._gerar_video_thread, args=(texto,), daemon=True).start()
    
    def _gerar_video_thread(self, texto):
        """Thread para geração de vídeo"""
        try:
            if not BACKEND_IMPORTS_OK:
                # Simulação para demonstração
                time.sleep(3)  # Simular processamento
                self.root.after(0, lambda: self._finalizar_geracao("/caminho/simulado/video_gerado.mp4"))
                return
                
            # Obter configurações
            motor = self.motor_tts.get() if hasattr(self, 'motor_tts') else None
            voz = self.voz_tts.get().split(" - ")[0] if hasattr(self, 'voz_tts') else None
            tipo_fundo = self.tipo_fundo.get() if hasattr(self, 'tipo_fundo') else None
            fonte_fundo = self.fonte_fundo.get() if hasattr(self, 'fonte_fundo') else None
            estilo_legenda = self.estilo_legenda.get() if hasattr(self, 'estilo_legenda') else None
            posicao_legenda = self.posicao_legenda.get() if hasattr(self, 'posicao_legenda') else None
            
            # Criar configuração personalizada
            config = VideoGeneratorConfig(
                tts_engine=motor,
                tts_voice=voz,
                background_type=tipo_fundo,
                background_source=fonte_fundo,
                subtitle_style=estilo_legenda,
                subtitle_position=posicao_legenda,
                output_dir=os.path.join(self.dir_raiz, "saida"),
                input_dir=os.path.join(self.dir_raiz, "entrada")
            )
            
            # Inicializar gerador com a configuração
            generator = VideoGenerator(config)
            
            # Gerar vídeo
            resultado = generator.generate_video_from_text(texto)
            
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_geracao(resultado))
            
        except Exception as e:
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_geracao(None, str(e)))
    
    def _finalizar_geracao(self, resultado, erro=None):
        """Finaliza o processo de geração de vídeo"""
        self.progresso_gerar.stop()
        self.botao_gerar.configure(state=tk.NORMAL)
        
        tempo_total = time.time() - self.tempo_inicio
        
        if resultado:
            self.atualizar_status(f"Vídeo gerado com sucesso em {tempo_total:.1f} segundos: {resultado}")
            messagebox.showinfo("Sucesso", f"Vídeo gerado com sucesso em {tempo_total:.1f} segundos!\nSalvo em: {resultado}")
            
            # Atualizar lista de vídeos na aba de edição
            self.atualizar_lista_videos()
        else:
            self.atualizar_status(f"Erro ao gerar vídeo: {erro}", erro=True)
            messagebox.showerror("Erro", f"Erro ao gerar vídeo: {erro}")
    
    def editar_video(self):
        """Edita o vídeo selecionado"""
        # Verificar se há vídeo selecionado
        selecao = self.lista_videos.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um vídeo para editar.")
            return
        
        # Obter caminho do vídeo selecionado
        video_path = self.lista_videos.get(selecao[0])
        
        # Desabilitar botão durante o processamento
        self.botao_editar.configure(state=tk.DISABLED)
        self.progresso_editar.start()
        self.tempo_inicio = time.time()
        
        # Obter plataformas selecionadas
        plataformas = []
        if self.plataforma_youtube.get():
            plataformas.append("youtube")
        if self.plataforma_instagram.get():
            plataformas.append("instagram")
        if self.plataforma_tiktok.get():
            plataformas.append("tiktok")
        
        # Atualizar estimativa de tempo
        self.atualizar_estimativa_tempo("editar", len(plataformas))
        
        # Iniciar thread para não bloquear a interface
        threading.Thread(target=self._editar_video_thread, args=(video_path, plataformas), daemon=True).start()
    
    def _editar_video_thread(self, video_path, plataformas):
        """Thread para edição de vídeo"""
        try:
            if not BACKEND_IMPORTS_OK:
                # Simulação para demonstração
                time.sleep(3)  # Simular processamento
                self.root.after(0, lambda: self._finalizar_edicao(True, os.path.join(self.dir_raiz, "saida")))
                return
                
            # Diretório de saída
            dir_saida = os.path.join(self.dir_raiz, "saida")
            os.makedirs(dir_saida, exist_ok=True)
            
            # Inicializar processador
            processador = ProcessadorVideo(video_path, dir_saida)
            
            # Atualizar metadados com plataformas selecionadas
            processador.metadados["plataformas"] = plataformas
            processador._salvar_metadados()
            
            # Processar vídeo
            resultado = processador.processar()
            
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_edicao(resultado, dir_saida))
            
        except Exception as e:
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_edicao(False, None, str(e)))
    
    def _finalizar_edicao(self, resultado, dir_saida, erro=None):
        """Finaliza o processo de edição de vídeo"""
        self.progresso_editar.stop()
        self.botao_editar.configure(state=tk.NORMAL)
        
        tempo_total = time.time() - self.tempo_inicio
        
        if resultado:
            self.atualizar_status(f"Vídeo editado com sucesso em {tempo_total:.1f} segundos")
            messagebox.showinfo("Sucesso", f"Vídeo editado com sucesso em {tempo_total:.1f} segundos!\nSalvo em: {dir_saida}")
            
            # Atualizar lista de vídeos na aba de publicação
            self.atualizar_lista_videos_editados()
        else:
            self.atualizar_status(f"Erro ao editar vídeo: {erro}", erro=True)
            messagebox.showerror("Erro", f"Erro ao editar vídeo: {erro}")
    
    def publicar_video(self):
        """Publica o vídeo selecionado nas redes sociais"""
        # Verificar se há vídeo selecionado
        selecao = self.lista_videos_editados.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um vídeo para publicar.")
            return
        
        # Obter caminho do vídeo selecionado
        video_path = self.lista_videos_editados.get(selecao[0])
        
        # Obter título e descrição
        titulo = self.titulo_video.get()
        descricao = self.descricao_video.get("1.0", tk.END).strip()
        
        if not titulo:
            messagebox.showwarning("Aviso", "Digite um título para o vídeo.")
            return
        
        # Desabilitar botão durante o processamento
        self.botao_publicar.configure(state=tk.DISABLED)
        self.progresso_publicar.start()
        self.tempo_inicio = time.time()
        
        # Obter plataformas selecionadas
        plataformas = []
        if self.publicar_youtube.get():
            plataformas.append("youtube")
        if self.publicar_instagram.get():
            plataformas.append("instagram")
        if self.publicar_tiktok.get():
            plataformas.append("tiktok")
        
        # Atualizar estimativa de tempo
        self.atualizar_estimativa_tempo("publicar", len(plataformas))
        
        # Iniciar thread para não bloquear a interface
        threading.Thread(target=self._publicar_video_thread, args=(video_path, titulo, descricao, plataformas), daemon=True).start()
    
    def _publicar_video_thread(self, video_path, titulo, descricao, plataformas):
        """Thread para publicação de vídeo"""
        try:
            if not BACKEND_IMPORTS_OK:
                # Simulação para demonstração
                time.sleep(3)  # Simular processamento
                self.root.after(0, lambda: self._finalizar_publicacao(True))
                return
                
            # Caminho para o arquivo de configuração
            config_path = os.path.join(self.dir_raiz, "config", "config.json")
            
            # Verificar se o diretório de configuração existe
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Criar configuração se não existir
            if not os.path.exists(config_path):
                config = {
                    "youtube": {
                        "api_key": self.youtube_api.get() if hasattr(self, 'youtube_api') else "",
                        "channel_id": ""
                    },
                    "instagram": {
                        "token": self.instagram_api.get() if hasattr(self, 'instagram_api') else "",
                        "user_id": ""
                    },
                    "tiktok": {
                        "api_key": self.tiktok_api.get() if hasattr(self, 'tiktok_api') else "",
                        "user_id": ""
                    }
                }
                
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=4)
            
            # Inicializar automação de upload
            automacao = AutomacaoUpload(config_path)
            
            # Publicar vídeo
            resultado = automacao.publicar_video(video_path, titulo, descricao, plataformas)
            
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_publicacao(resultado))
            
        except Exception as e:
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_publicacao(None, str(e)))
    
    def _finalizar_publicacao(self, resultado, erro=None):
        """Finaliza o processo de publicação de vídeo"""
        self.progresso_publicar.stop()
        self.botao_publicar.configure(state=tk.NORMAL)
        
        tempo_total = time.time() - self.tempo_inicio
        
        if resultado:
            self.atualizar_status(f"Vídeo publicado com sucesso em {tempo_total:.1f} segundos")
            messagebox.showinfo("Sucesso", f"Vídeo publicado com sucesso em {tempo_total:.1f} segundos!")
        else:
            self.atualizar_status(f"Erro ao publicar vídeo: {erro}", erro=True)
            messagebox.showerror("Erro", f"Erro ao publicar vídeo: {erro}")
    
    def executar_fluxo_automatico(self):
        """Executa o fluxo de trabalho automático completo"""
        texto = self.texto_automatico.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite um roteiro antes de executar o fluxo.")
            return
        
        # Verificar quais etapas estão selecionadas
        if not (self.auto_gerar.get() or self.auto_editar.get() or self.auto_publicar.get()):
            messagebox.showwarning("Aviso", "Selecione pelo menos uma etapa para executar.")
            return
        
        # Desabilitar botão durante o processamento
        self.botao_executar.configure(state=tk.DISABLED)
        
        # Resetar barras de progresso
        self.progresso_geral['value'] = 0
        self.progresso_auto_gerar['value'] = 0
        self.progresso_auto_editar['value'] = 0
        self.progresso_auto_publicar['value'] = 0
        
        # Obter plataformas selecionadas
        plataformas = []
        if self.auto_youtube.get():
            plataformas.append("youtube")
        if self.auto_instagram.get():
            plataformas.append("instagram")
        if self.auto_tiktok.get():
            plataformas.append("tiktok")
        
        # Atualizar estimativa de tempo
        etapas = 0
        if self.auto_gerar.get():
            etapas += 1
        if self.auto_editar.get():
            etapas += 1
        if self.auto_publicar.get():
            etapas += 1
        
        self.atualizar_estimativa_tempo("automatico", etapas, len(plataformas))
        
        # Iniciar thread para não bloquear a interface
        threading.Thread(target=self._executar_fluxo_thread, args=(texto, plataformas), daemon=True).start()
    
    def _executar_fluxo_thread(self, texto, plataformas):
        """Thread para execução do fluxo automático"""
        try:
            resultado_video = None
            resultado_edicao = None
            resultado_publicacao = None
            
            if not BACKEND_IMPORTS_OK:
                # Simulação para demonstração
                if self.auto_gerar.get():
                    self.root.after(0, lambda: self.atualizar_status_auto("Gerando vídeo..."))
                    time.sleep(3)  # Simular processamento
                    resultado_video = "/caminho/simulado/video_gerado.mp4"
                    self.root.after(0, lambda: self._atualizar_progresso_auto("gerar", 100))
                    
                if self.auto_editar.get():
                    self.root.after(0, lambda: self.atualizar_status_auto("Editando vídeo..."))
                    time.sleep(3)  # Simular processamento
                    resultado_edicao = True
                    self.root.after(0, lambda: self._atualizar_progresso_auto("editar", 100))
                    
                if self.auto_publicar.get():
                    self.root.after(0, lambda: self.atualizar_status_auto("Publicando vídeo..."))
                    time.sleep(3)  # Simular processamento
                    resultado_publicacao = True
                    self.root.after(0, lambda: self._atualizar_progresso_auto("publicar", 100))
                
                # Atualizar progresso geral
                self.root.after(0, lambda: self._atualizar_progresso_geral(100))
                
                # Finalizar fluxo
                self.root.after(0, lambda: self._finalizar_fluxo_automatico(
                    resultado_video if self.auto_gerar.get() else None, 
                    resultado_edicao if self.auto_editar.get() else None, 
                    resultado_publicacao if self.auto_publicar.get() else None
                ))
                return
            
            # Etapa 1: Geração de vídeo
            if self.auto_gerar.get():
                self.root.after(0, lambda: self.atualizar_status_auto("Gerando vídeo..."))
                
                # Obter configurações
                motor = self.motor_tts.get() if hasattr(self, 'motor_tts') else None
                voz = self.voz_tts.get().split(" - ")[0] if hasattr(self, 'voz_tts') else None
                tipo_fundo = self.tipo_fundo.get() if hasattr(self, 'tipo_fundo') else None
                fonte_fundo = self.fonte_fundo.get() if hasattr(self, 'fonte_fundo') else None
                estilo_legenda = self.estilo_legenda.get() if hasattr(self, 'estilo_legenda') else None
                posicao_legenda = self.posicao_legenda.get() if hasattr(self, 'posicao_legenda') else None
                
                # Criar configuração personalizada
                config = VideoGeneratorConfig(
                    tts_engine=motor,
                    tts_voice=voz,
                    background_type=tipo_fundo,
                    background_source=fonte_fundo,
                    subtitle_style=estilo_legenda,
                    subtitle_position=posicao_legenda,
                    output_dir=os.path.join(self.dir_raiz, "saida"),
                    input_dir=os.path.join(self.dir_raiz, "entrada")
                )
                
                # Inicializar gerador com a configuração
                generator = VideoGenerator(config)
                
                # Gerar vídeo
                resultado_video = generator.generate_video_from_text(texto)
                
                if not resultado_video:
                    raise Exception("Falha ao gerar vídeo")
                
                # Atualizar progresso
                self.root.after(0, lambda: self._atualizar_progresso_auto("gerar", 100))
                
                # Atualizar progresso geral
                if self.auto_gerar.get() and self.auto_editar.get() and self.auto_publicar.get():
                    self.root.after(0, lambda: self._atualizar_progresso_geral(33))
                elif (self.auto_gerar.get() and self.auto_editar.get()) or (self.auto_gerar.get() and self.auto_publicar.get()):
                    self.root.after(0, lambda: self._atualizar_progresso_geral(50))
                else:
                    self.root.after(0, lambda: self._atualizar_progresso_geral(100))
            
            # Etapa 2: Edição de vídeo
            if self.auto_editar.get() and (resultado_video or not self.auto_gerar.get()):
                self.root.after(0, lambda: self.atualizar_status_auto("Editando vídeo..."))
                
                # Se não geramos vídeo, usar o primeiro da lista
                if not resultado_video:
                    # Verificar se há vídeos na pasta de entrada
                    dir_entrada = os.path.join(self.dir_raiz, "entrada")
                    videos = [os.path.join(dir_entrada, f) for f in os.listdir(dir_entrada) 
                             if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]
                    
                    if not videos:
                        raise Exception("Nenhum vídeo disponível para edição")
                    
                    resultado_video = videos[0]
                
                # Diretório de saída
                dir_saida = os.path.join(self.dir_raiz, "saida")
                os.makedirs(dir_saida, exist_ok=True)
                
                # Inicializar processador
                processador = ProcessadorVideo(resultado_video, dir_saida)
                
                # Atualizar metadados com plataformas selecionadas
                processador.metadados["plataformas"] = plataformas
                processador._salvar_metadados()
                
                # Processar vídeo
                resultado_edicao = processador.processar()
                
                if not resultado_edicao:
                    raise Exception("Falha ao editar vídeo")
                
                # Obter caminhos dos vídeos editados
                videos_editados = []
                for plataforma in plataformas:
                    nome_base = os.path.basename(resultado_video)
                    nome_sem_ext, _ = os.path.splitext(nome_base)
                    video_editado = os.path.join(dir_saida, f"{nome_sem_ext}_{plataforma}.mp4")
                    if os.path.exists(video_editado):
                        videos_editados.append(video_editado)
                
                # Atualizar progresso
                self.root.after(0, lambda: self._atualizar_progresso_auto("editar", 100))
                
                # Atualizar progresso geral
                if self.auto_gerar.get() and self.auto_editar.get() and self.auto_publicar.get():
                    self.root.after(0, lambda: self._atualizar_progresso_geral(66))
                elif (self.auto_gerar.get() and self.auto_editar.get()) or (self.auto_editar.get() and self.auto_publicar.get()):
                    self.root.after(0, lambda: self._atualizar_progresso_geral(75))
                else:
                    self.root.after(0, lambda: self._atualizar_progresso_geral(100))
            
            # Etapa 3: Publicação de vídeo
            if self.auto_publicar.get() and ((resultado_edicao and videos_editados) or not self.auto_editar.get()):
                self.root.after(0, lambda: self.atualizar_status_auto("Publicando vídeo..."))
                
                # Se não editamos vídeo, usar o primeiro da lista de editados
                if not resultado_edicao or not videos_editados:
                    # Verificar se há vídeos na pasta de saída
                    dir_saida = os.path.join(self.dir_raiz, "saida")
                    videos_editados = [os.path.join(dir_saida, f) for f in os.listdir(dir_saida) 
                                      if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]
                    
                    if not videos_editados:
                        raise Exception("Nenhum vídeo disponível para publicação")
                
                # Caminho para o arquivo de configuração
                config_path = os.path.join(self.dir_raiz, "config", "config.json")
                
                # Verificar se o diretório de configuração existe
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                
                # Criar configuração se não existir
                if not os.path.exists(config_path):
                    config = {
                        "youtube": {
                            "api_key": self.youtube_api.get() if hasattr(self, 'youtube_api') else "",
                            "channel_id": ""
                        },
                        "instagram": {
                            "token": self.instagram_api.get() if hasattr(self, 'instagram_api') else "",
                            "user_id": ""
                        },
                        "tiktok": {
                            "api_key": self.tiktok_api.get() if hasattr(self, 'tiktok_api') else "",
                            "user_id": ""
                        }
                    }
                    
                    with open(config_path, "w") as f:
                        json.dump(config, f, indent=4)
                
                # Inicializar automação de upload
                automacao = AutomacaoUpload(config_path)
                
                # Gerar título e descrição automáticos se não fornecidos
                titulo = f"Vídeo sobre {' '.join(texto.split()[:5])}" if len(texto) > 20 else texto
                descricao = texto[:500] + "...\n\nGerado automaticamente pelo ZudoEditor."
                
                # Publicar cada vídeo editado
                for video_path in videos_editados:
                    plataforma = os.path.basename(video_path).split("_")[-1].split(".")[0]
                    if plataforma in plataformas:
                        automacao.publicar_video(video_path, titulo, descricao, [plataforma])
                
                resultado_publicacao = True
                
                # Atualizar progresso
                self.root.after(0, lambda: self._atualizar_progresso_auto("publicar", 100))
                
                # Atualizar progresso geral
                self.root.after(0, lambda: self._atualizar_progresso_geral(100))
            
            # Finalizar fluxo
            self.root.after(0, lambda: self._finalizar_fluxo_automatico(
                resultado_video if self.auto_gerar.get() else None, 
                resultado_edicao if self.auto_editar.get() else None, 
                resultado_publicacao if self.auto_publicar.get() else None
            ))
            
        except Exception as e:
            # Atualizar interface na thread principal
            self.root.after(0, lambda: self._finalizar_fluxo_automatico(
                resultado_video if self.auto_gerar.get() else None, 
                resultado_edicao if self.auto_editar.get() else None, 
                resultado_publicacao if self.auto_publicar.get() else None, 
                str(e)
            ))
    
    def _finalizar_fluxo_automatico(self, resultado_video, resultado_edicao, resultado_publicacao, erro=None):
        """Finaliza o processo de fluxo automático"""
        self.botao_executar.configure(state=tk.NORMAL)
        
        if erro:
            self.atualizar_status_auto(f"Erro no fluxo automático: {erro}")
            messagebox.showerror("Erro", f"Erro no fluxo automático: {erro}")
            return
        
        # Construir mensagem de sucesso
        mensagem = "Fluxo automático concluído com sucesso!\n\n"
        
        if self.auto_gerar.get() and resultado_video:
            mensagem += f"- Vídeo gerado: {resultado_video}\n"
        
        if self.auto_editar.get() and resultado_edicao:
            mensagem += "- Vídeo editado com sucesso\n"
        
        if self.auto_publicar.get() and resultado_publicacao:
            mensagem += "- Vídeo publicado nas plataformas selecionadas\n"
        
        self.atualizar_status_auto("Fluxo automático concluído com sucesso!")
        messagebox.showinfo("Sucesso", mensagem)
        
        # Atualizar listas
        self.atualizar_lista_videos()
        self.atualizar_lista_videos_editados()
    
    # Métodos auxiliares
    
    def atualizar_lista_videos(self):
        """Atualiza a lista de vídeos disponíveis para edição"""
        try:
            # Limpar lista atual
            self.lista_videos.delete(0, tk.END)
            
            # Diretório de entrada
            dir_entrada = os.path.join(self.dir_raiz, "entrada")
            
            # Verificar se o diretório existe
            if not os.path.exists(dir_entrada):
                os.makedirs(dir_entrada, exist_ok=True)
                return
            
            # Listar arquivos de vídeo
            for arquivo in os.listdir(dir_entrada):
                if arquivo.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
                    self.lista_videos.insert(tk.END, os.path.join(dir_entrada, arquivo))
        except Exception as e:
            self.atualizar_status(f"Erro ao atualizar lista de vídeos: {str(e)}", erro=True)
    
    def atualizar_lista_videos_editados(self):
        """Atualiza a lista de vídeos editados disponíveis para publicação"""
        try:
            # Limpar lista atual
            self.lista_videos_editados.delete(0, tk.END)
            
            # Diretório de saída
            dir_saida = os.path.join(self.dir_raiz, "saida")
            
            # Verificar se o diretório existe
            if not os.path.exists(dir_saida):
                os.makedirs(dir_saida, exist_ok=True)
                return
            
            # Listar arquivos de vídeo
            for arquivo in os.listdir(dir_saida):
                if arquivo.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
                    self.lista_videos_editados.insert(tk.END, os.path.join(dir_saida, arquivo))
        except Exception as e:
            self.atualizar_status(f"Erro ao atualizar lista de vídeos editados: {str(e)}", erro=True)
    
    def atualizar_status(self, mensagem, erro=False):
        """Atualiza a barra de status"""
        self.label_status.configure(text=mensagem, foreground="red" if erro else "black")
        print(f"Status: {mensagem}")
    
    def atualizar_status_auto(self, mensagem):
        """Atualiza o status na aba de fluxo automático"""
        self.label_status_auto.configure(text=f"Status: {mensagem}")
    
    def atualizar_estimativa_tempo(self, etapa, quantidade, plataformas=1):
        """Atualiza a estimativa de tempo para a operação"""
        tempo_estimado = 0
        
        if etapa == "gerar":
            # Estimar com base no número de palavras
            palavras = quantidade
            tempo_estimado = 3 + (palavras / 100) * 2  # Base + tempo por palavra
        elif etapa == "editar":
            # Estimar com base no número de plataformas
            tempo_estimado = 2 + quantidade * 3  # Base + tempo por plataforma
        elif etapa == "publicar":
            # Estimar com base no número de plataformas
            tempo_estimado = 1 + quantidade * 2  # Base + tempo por plataforma
        elif etapa == "automatico":
            # Estimar com base no número de etapas e plataformas
            tempo_estimado = quantidade * 5 + plataformas * 2  # Tempo por etapa + tempo por plataforma
        
        # Formatar tempo
        minutos = int(tempo_estimado)
        segundos = int((tempo_estimado - minutos) * 60)
        tempo_formatado = f"{minutos:02d}:{segundos:02d}"
        
        # Atualizar label correspondente
        if etapa == "gerar":
            self.label_tempo_gerar.configure(text=f"Tempo estimado: {tempo_formatado}")
        elif etapa == "editar":
            self.label_tempo_editar.configure(text=f"Tempo estimado: {tempo_formatado}")
        elif etapa == "publicar":
            self.label_tempo_publicar.configure(text=f"Tempo estimado: {tempo_formatado}")
        elif etapa == "automatico":
            self.label_tempo_auto.configure(text=f"Tempo estimado total: {tempo_formatado}")
    
    def _atualizar_progresso_auto(self, etapa, valor):
        """Atualiza o progresso na aba de fluxo automático"""
        if etapa == "gerar":
            self.progresso_auto_gerar['value'] = valor
        elif etapa == "editar":
            self.progresso_auto_editar['value'] = valor
        elif etapa == "publicar":
            self.progresso_auto_publicar['value'] = valor
    
    def _atualizar_progresso_geral(self, valor):
        """Atualiza o progresso geral na aba de fluxo automático"""
        self.progresso_geral['value'] = valor
    
    def selecionar_diretorio(self, var):
        """Abre um diálogo para selecionar diretório"""
        diretorio = filedialog.askdirectory()
        if diretorio:
            var.set(diretorio)
    
    def carregar_configuracoes(self):
        """Carrega as configurações do arquivo"""
        try:
            config_path = os.path.join(self.dir_raiz, "config", "config.json")
            
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                
                # Carregar configurações de API
                if "youtube" in config and "api_key" in config["youtube"]:
                    self.youtube_api.set(config["youtube"]["api_key"])
                
                if "instagram" in config and "token" in config["instagram"]:
                    self.instagram_api.set(config["instagram"]["token"])
                
                if "tiktok" in config and "api_key" in config["tiktok"]:
                    self.tiktok_api.set(config["tiktok"]["api_key"])
            
            # Carregar diretórios
            self.dir_entrada.set(os.path.join(self.dir_raiz, "entrada"))
            self.dir_saida.set(os.path.join(self.dir_raiz, "saida"))
            
            # Atualizar listas
            self.atualizar_lista_videos()
            self.atualizar_lista_videos_editados()
            
        except Exception as e:
            self.atualizar_status(f"Erro ao carregar configurações: {str(e)}", erro=True)
    
    def salvar_configuracoes(self):
        """Salva as configurações no arquivo"""
        try:
            config_path = os.path.join(self.dir_raiz, "config", "config.json")
            
            # Verificar se o diretório de configuração existe
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Criar configuração
            config = {
                "youtube": {
                    "api_key": self.youtube_api.get(),
                    "channel_id": ""
                },
                "instagram": {
                    "token": self.instagram_api.get(),
                    "user_id": ""
                },
                "tiktok": {
                    "api_key": self.tiktok_api.get(),
                    "user_id": ""
                }
            }
            
            # Salvar configuração
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)
            
            # Criar diretórios se não existirem
            os.makedirs(self.dir_entrada.get(), exist_ok=True)
            os.makedirs(self.dir_saida.get(), exist_ok=True)
            
            self.atualizar_status("Configurações salvas com sucesso")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            self.atualizar_status(f"Erro ao salvar configurações: {str(e)}", erro=True)
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def restaurar_configuracoes(self):
        """Restaura as configurações para os valores padrão"""
        try:
            # Restaurar diretórios
            self.dir_entrada.set(os.path.join(self.dir_raiz, "entrada"))
            self.dir_saida.set(os.path.join(self.dir_raiz, "saida"))
            
            # Restaurar APIs
            self.youtube_api.set("")
            self.instagram_api.set("")
            self.tiktok_api.set("")
            
            self.atualizar_status("Configurações restauradas para valores padrão")
            messagebox.showinfo("Sucesso", "Configurações restauradas para valores padrão!")
            
        except Exception as e:
            self.atualizar_status(f"Erro ao restaurar configurações: {str(e)}", erro=True)
            messagebox.showerror("Erro", f"Erro ao restaurar configurações: {str(e)}")
    
    def verificar_dependencias(self):
        """Verifica se todas as dependências estão instaladas"""
        try:
            # Lista de dependências
            dependencias = [
                "moviepy", "numpy", "pillow", "pyttsx3", "edge-tts", "gtts", 
                "SpeechRecognition", "transformers", "whisper"
            ]
            
            # Verificar cada dependência
            faltando = []
            for dep in dependencias:
                try:
                    __import__(dep.replace("-", "_"))
                except ImportError:
                    faltando.append(dep)
            
            if faltando:
                mensagem = "As seguintes dependências estão faltando:\n\n"
                mensagem += "\n".join(faltando)
                mensagem += "\n\nDeseja instalar automaticamente?"
                
                if messagebox.askyesno("Dependências Faltando", mensagem):
                    # Instalar dependências
                    for dep in faltando:
                        subprocess.run([sys.executable, "-m", "pip", "install", dep])
                    
                    messagebox.showinfo("Sucesso", "Dependências instaladas com sucesso!")
            else:
                messagebox.showinfo("Dependências", "Todas as dependências estão instaladas!")
            
        except Exception as e:
            self.atualizar_status(f"Erro ao verificar dependências: {str(e)}", erro=True)
            messagebox.showerror("Erro", f"Erro ao verificar dependências: {str(e)}")


# Função principal
def main():
    root = tk.Tk()
    app = ZudoEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

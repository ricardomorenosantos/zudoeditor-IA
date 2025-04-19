#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZudoEditor - Script de Inicialização
Este script inicia o ZudoEditor e verifica as dependências necessárias.
"""

import sys
import os

# Adiciona o caminho do projeto no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from moviepy.editor import VideoFileClip  # ou qualquer outro objeto que você precise
    print("✅ moviepy foi importado com sucesso!")
except ImportError as e:
    print("❌ ERRO ao importar moviepy:", e)


from moviepy.editor import VideoFileClip
print("✅ moviepy.editor acessado com sucesso!")
  # <- testa se está visível
print("moviepy funciona!")


sys.path.append(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python310", "site-packages"))

import subprocess
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "zudoeditor"))

import importlib.util

def verificar_dependencias():
    print("Verificando dependências...")

    # Mapeamento: nome da dependência → nome do módulo real a ser testado
    dependencias = {
        "moviepy": "moviepy.editor",
        "numpy": "numpy",
        "pillow": "PIL",
        "pyttsx3": "pyttsx3",
        "edge-tts": "edge_tts",
        "gtts": "gtts",
        "SpeechRecognition": "speech_recognition",
        "transformers": "transformers",
        "whisper": "whisper"
    }

    faltando = []
    for pacote, modulo in dependencias.items():
        if importlib.util.find_spec(modulo) is None:
            faltando.append(pacote)

    return faltando




def instalar_dependencias(deps):
    """Instala as dependências faltantes"""
    for dep in deps:
        print(f"Instalando {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)

def criar_diretorios():
    """Cria os diretórios necessários se não existirem"""
    # Obter diretório raiz do projeto
    dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Diretórios necessários
    diretorios = [
        os.path.join(dir_raiz, "entrada"),
        os.path.join(dir_raiz, "saida"),
        os.path.join(dir_raiz, "config"),
        os.path.join(dir_raiz, "temp")
    ]
    
    # Criar diretórios
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)

def iniciar_painel():
    """Inicia o painel do ZudoEditor"""
    try:
        # Importar o módulo do painel
        from zudoeditor.painel.painel import ZudoEditorApp

        # Iniciar a aplicação
        root = tk.Tk()
        app = ZudoEditorApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar o painel: {str(e)}")
        sys.exit(1)

def main():
    """Função principal"""
    print("Iniciando ZudoEditor...")
    
    # Verificar dependências
    print("Verificando dependências...")
    deps_faltando = verificar_dependencias()
    
    if deps_faltando:
        print(f"Dependências faltando: {', '.join(deps_faltando)}")
        
        # Perguntar se deseja instalar
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        
        mensagem = "As seguintes dependências estão faltando:\n\n"
        mensagem += "\n".join(deps_faltando)
        mensagem += "\n\nDeseja instalar automaticamente?"
        
        if messagebox.askyesno("Dependências Faltando", mensagem):
            try:
                instalar_dependencias(deps_faltando)
                print("Dependências instaladas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao instalar dependências: {str(e)}")
                sys.exit(1)
        else:
            messagebox.showwarning("Aviso", "O ZudoEditor pode não funcionar corretamente sem as dependências necessárias.")
        
        root.destroy()
    
    # Criar diretórios necessários
    print("Verificando diretórios...")
    criar_diretorios()
    
    # Iniciar o painel
    print("Iniciando painel...")
    iniciar_painel()

if __name__ == "__main__":
    main()

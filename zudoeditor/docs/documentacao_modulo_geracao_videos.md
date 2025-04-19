# Documentação do Módulo de Geração Automática de Vídeos com IA

## Introdução

O Módulo de Geração Automática de Vídeos com IA é uma nova funcionalidade do ZudoEditor que permite criar vídeos completos a partir de texto ou tópicos. Este módulo utiliza tecnologias de Inteligência Artificial para gerar narração com voz sintética, sincronizar legendas automaticamente e aplicar fundos visuais personalizáveis.

Esta documentação fornece instruções detalhadas sobre como instalar, configurar e utilizar o módulo de geração de vídeos, bem como exemplos práticos de uso.

## Índice

1. [Instalação e Requisitos](#1-instalação-e-requisitos)
2. [Visão Geral do Módulo](#2-visão-geral-do-módulo)
3. [Guia de Uso](#3-guia-de-uso)
4. [Interface de Linha de Comando](#4-interface-de-linha-de-comando)
5. [Personalização](#5-personalização)
6. [Integração com o ZudoEditor](#6-integração-com-o-zudoeditor)
7. [Solução de Problemas](#7-solução-de-problemas)
8. [Perguntas Frequentes](#8-perguntas-frequentes)

## 1. Instalação e Requisitos

### 1.1 Requisitos de Sistema

- **Sistema Operacional**: Windows 10/11, macOS 10.15+, ou Ubuntu 20.04+
- **CPU**: Processador quad-core moderno
- **RAM**: Mínimo de 8GB, recomendado 16GB
- **Armazenamento**: 2GB para bibliotecas e recursos + espaço para vídeos
- **Python**: Versão 3.8 ou superior

### 1.2 Dependências

O módulo de geração de vídeos depende das seguintes bibliotecas Python:

```
moviepy>=1.0.3
numpy>=1.20.0
pillow>=8.0.0
pyttsx3>=2.90
edge-tts>=6.1.3
gtts>=2.3.0
SpeechRecognition>=3.8.1
transformers>=4.20.0 (opcional, para geração de roteiro)
whisper>=1.1.10 (opcional, para transcrição avançada)
```

### 1.3 Instalação

1. Certifique-se de que o ZudoEditor já está instalado e funcionando corretamente.

2. Instale as dependências necessárias:

```bash
pip install moviepy numpy pillow pyttsx3 edge-tts gtts SpeechRecognition
```

3. Para funcionalidades avançadas (opcional):

```bash
pip install transformers whisper
```

4. Copie os arquivos do módulo para o diretório do ZudoEditor:

```bash
cp text_to_speech_component.py background_selection_system.py subtitle_synchronization_mechanism.py video_generator_module.py /caminho/para/zudoeditor/
```

5. Crie os diretórios necessários:

```bash
mkdir -p /caminho/para/zudoeditor/resources/backgrounds/images
mkdir -p /caminho/para/zudoeditor/resources/backgrounds/videos
mkdir -p /caminho/para/zudoeditor/resources/fonts
mkdir -p /caminho/para/zudoeditor/entrada
mkdir -p /caminho/para/zudoeditor/output
```

## 2. Visão Geral do Módulo

O Módulo de Geração Automática de Vídeos com IA é composto por quatro componentes principais:

1. **Gerador de Roteiro**: Cria um roteiro a partir de um tópico fornecido pelo usuário.
2. **Conversor Texto-Fala (TTS)**: Transforma o texto do roteiro em narração de áudio.
3. **Seletor de Fundo Visual**: Gerencia o fundo visual do vídeo (cor sólida, gradiente, imagem ou vídeo).
4. **Gerador de Legendas**: Cria e sincroniza legendas com a narração.

Estes componentes trabalham juntos para produzir um vídeo completo que é automaticamente enviado para a pasta de entrada do ZudoEditor, onde pode ser processado pelo sistema de edição inteligente existente.

### 2.1 Fluxo de Trabalho

O fluxo de trabalho típico do módulo é o seguinte:

1. O usuário fornece um texto ou tópico para o vídeo.
2. Se um tópico for fornecido, o sistema gera automaticamente um roteiro.
3. O texto é convertido em áudio usando o motor TTS selecionado.
4. Um fundo visual é selecionado (aleatoriamente ou conforme especificado pelo usuário).
5. As legendas são geradas e sincronizadas com o áudio.
6. Todos os elementos são combinados em um vídeo final.
7. O vídeo é exportado para a pasta de entrada do ZudoEditor para processamento adicional.

## 3. Guia de Uso

### 3.1 Usando o Módulo via Python

Para usar o módulo em seu próprio código Python:

```python
from video_generator_module import VideoGenerator, VideoGeneratorConfig

# Criar configuração personalizada (opcional)
config = VideoGeneratorConfig(
    video_width=1920,
    video_height=1080,
    tts_engine="edge-tts",  # ou "pyttsx3", "gTTS"
    subtitle_style="modern"  # ou "standard", "bold", "shadow", "outline", "minimal"
)

# Inicializar o gerador de vídeos
generator = VideoGenerator(config)

# Gerar vídeo a partir de texto
video_path = generator.generate_video_from_text(
    "Este é um exemplo de texto que será convertido em um vídeo com narração, legendas e fundo visual.",
    "meu_video.mp4"
)

# Ou gerar vídeo a partir de um tópico
video_path = generator.generate_video_from_topic(
    "inteligência artificial",
    "video_ia.mp4"
)

print(f"Vídeo gerado: {video_path}")
```

### 3.2 Usando a Interface de Linha de Comando

O módulo inclui uma interface de linha de comando para facilitar o uso:

```bash
# Gerar vídeo a partir de texto
python video_generator_module.py gerar --texto "Este é um exemplo de texto para o vídeo." --saida "meu_video.mp4"

# Gerar vídeo a partir de tópico
python video_generator_module.py gerar --topico "inteligência artificial" --saida "video_ia.mp4"

# Listar vozes disponíveis
python video_generator_module.py listar --vozes

# Listar motores TTS disponíveis
python video_generator_module.py listar --motores

# Listar estilos de legenda disponíveis
python video_generator_module.py listar --estilos
```

## 4. Interface de Linha de Comando

A interface de linha de comando oferece duas funcionalidades principais: geração de vídeos e listagem de recursos disponíveis.

### 4.1 Comando "gerar"

O comando `gerar` cria um vídeo a partir de texto ou tópico:

```bash
python video_generator_module.py gerar [opções]
```

Opções disponíveis:

- `--texto`, `-t`: Texto para narração
- `--topico`, `-p`: Tópico para gerar roteiro automaticamente
- `--saida`, `-o`: Nome do arquivo de saída
- `--voz`, `-v`: ID da voz a ser usada
- `--motor`, `-m`: Motor TTS a ser usado
- `--estilo`, `-e`: Estilo de legenda
- `--fundo`, `-f`: Tipo de fundo
- `--fonte-fundo`, `-s`: Fonte do fundo (depende do tipo)

Exemplos:

```bash
# Gerar vídeo com texto e voz específica
python video_generator_module.py gerar --texto "Este é um exemplo." --voz "pt-BR-AntonioNeural" --motor "edge-tts"

# Gerar vídeo com tópico e estilo de legenda específico
python video_generator_module.py gerar --topico "energia renovável" --estilo "bold" --saida "energia.mp4"

# Gerar vídeo com fundo de cor sólida
python video_generator_module.py gerar --texto "Exemplo com fundo azul." --fundo "solid_color" --fonte-fundo "#0000FF"
```

### 4.2 Comando "listar"

O comando `listar` exibe os recursos disponíveis:

```bash
python video_generator_module.py listar [opções]
```

Opções disponíveis:

- `--vozes`: Listar vozes disponíveis
- `--motores`: Listar motores TTS disponíveis
- `--estilos`: Listar estilos de legenda disponíveis
- `--fundos`: Listar tipos de fundo disponíveis
- `--cores`: Listar cores predefinidas
- `--gradientes`: Listar gradientes predefinidos
- `--imagens`: Listar imagens disponíveis
- `--videos`: Listar vídeos disponíveis

Exemplos:

```bash
# Listar todas as vozes disponíveis
python video_generator_module.py listar --vozes

# Listar cores predefinidas
python video_generator_module.py listar --cores
```

## 5. Personalização

### 5.1 Personalização de Voz

O módulo suporta diferentes motores TTS, cada um com suas próprias vozes:

- **edge-tts**: Oferece vozes de alta qualidade da Microsoft em vários idiomas
- **pyttsx3**: Funciona offline, usando as vozes instaladas no sistema
- **gTTS**: Usa o Google Text-to-Speech (requer internet)

Para listar as vozes disponíveis:

```bash
python video_generator_module.py listar --vozes
```

Para usar uma voz específica:

```python
generator = VideoGenerator(VideoGeneratorConfig(
    tts_engine="edge-tts",
    tts_voice="pt-BR-FranciscaNeural"  # ID da voz
))
```

### 5.2 Personalização de Fundo

O módulo suporta quatro tipos de fundo:

- **Cor sólida**: Uma cor única para todo o vídeo
- **Gradiente**: Transição suave entre duas cores
- **Imagem**: Uma imagem estática como fundo
- **Vídeo**: Um vídeo como fundo (com loop se necessário)

Para adicionar imagens ou vídeos personalizados:

```python
# Adicionar imagem
background_manager = BackgroundManager()
background_manager.add_image("/caminho/para/minha_imagem.jpg")

# Adicionar vídeo
background_manager.add_video("/caminho/para/meu_video.mp4")
```

### 5.3 Personalização de Legendas

O módulo oferece vários estilos de legenda predefinidos:

- **standard**: Estilo padrão, texto branco simples
- **bold**: Texto branco em negrito, maior
- **shadow**: Texto branco com sombra
- **outline**: Texto branco com contorno preto
- **modern**: Texto branco com fundo semi-transparente e sombra suave
- **minimal**: Texto branco com contorno fino, fonte leve

Para usar um estilo específico:

```python
generator = VideoGenerator(VideoGeneratorConfig(
    subtitle_style="modern"
))
```

Para adicionar fontes personalizadas:

```python
subtitle_manager = SubtitleManager()
subtitle_manager.add_font("/caminho/para/minha_fonte.ttf")
```

## 6. Integração com o ZudoEditor

O módulo de geração de vídeos foi projetado para integrar-se perfeitamente com o ZudoEditor existente.

### 6.1 Fluxo de Integração

1. O módulo gera um vídeo completo com narração, legendas e fundo visual.
2. O vídeo é salvo na pasta de saída (`output/`) e também copiado para a pasta de entrada do ZudoEditor (`entrada/`).
3. O sistema de monitoramento de pasta do ZudoEditor detecta o novo vídeo.
4. O sistema de edição inteligente do ZudoEditor processa o vídeo conforme suas configurações.
5. O vídeo final é exportado para as plataformas configuradas.

### 6.2 Configuração da Integração

Por padrão, o módulo usa os seguintes diretórios:

- **Pasta de saída**: `output/` (dentro do diretório do ZudoEditor)
- **Pasta de entrada**: `entrada/` (dentro do diretório do ZudoEditor)

Você pode personalizar estes diretórios na configuração:

```python
generator = VideoGenerator(VideoGeneratorConfig(
    output_dir="/caminho/personalizado/para/saida",
    input_dir="/caminho/personalizado/para/entrada"
))
```

## 7. Solução de Problemas

### 7.1 Problemas Comuns e Soluções

#### Erro: "Falha ao gerar áudio"

**Possíveis causas e soluções:**

- **Motor TTS não disponível**: Tente usar um motor TTS diferente.
  ```bash
  python video_generator_module.py gerar --texto "Teste" --motor "pyttsx3"
  ```

- **Dependências ausentes**: Verifique se todas as dependências estão instaladas.
  ```bash
  pip install pyttsx3 edge-tts gtts
  ```

- **Sem conexão com a internet**: Se estiver usando edge-tts ou gTTS, verifique sua conexão com a internet.

#### Erro: "Falha ao gerar vídeo"

**Possíveis causas e soluções:**

- **Dependências ausentes**: Verifique se moviepy e suas dependências estão instaladas.
  ```bash
  pip install moviepy
  ```

- **FFmpeg ausente**: MoviePy requer FFmpeg. Instale-o no seu sistema.
  ```bash
  # Ubuntu
  sudo apt-get install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Windows
  # Baixe de https://ffmpeg.org/download.html e adicione ao PATH
  ```

- **Permissões de arquivo**: Verifique se o usuário tem permissões para escrever nos diretórios de saída.

#### Aviso: "Não foi possível usar modelo de linguagem"

**Possíveis causas e soluções:**

- **Transformers não instalado**: Instale a biblioteca transformers para geração de roteiro.
  ```bash
  pip install transformers
  ```

- **Modelo não baixado**: O primeiro uso pode demorar mais, pois o modelo precisa ser baixado.

### 7.2 Logs e Depuração

O módulo usa o sistema de logging do Python para registrar informações, avisos e erros. Por padrão, os logs são exibidos no console.

Para salvar os logs em um arquivo:

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='zudo_generator.log'
)

# Usar o gerador normalmente
generator = VideoGenerator()
generator.generate_video_from_text("Texto de teste")
```

## 8. Perguntas Frequentes

### 8.1 Geral

**P: O módulo funciona offline?**
R: Parcialmente. O componente pyttsx3 funciona completamente offline, mas edge-tts e gTTS requerem conexão com a internet. A geração de roteiro com transformers funciona offline após o download inicial do modelo.

**P: Quais idiomas são suportados?**
R: O suporte a idiomas depende do motor TTS escolhido. O edge-tts suporta mais de 40 idiomas, incluindo português brasileiro. O pyttsx3 suporta os idiomas instalados no seu sistema. O gTTS suporta os idiomas do Google Text-to-Speech.

**P: Posso usar o módulo sem o ZudoEditor?**
R: Sim, o módulo pode ser usado de forma independente. Basta não configurar a pasta de entrada ou ignorar a cópia do vídeo para essa pasta.

### 8.2 Personalização

**P: Como adicionar mais vozes?**
R: As vozes disponíveis dependem do motor TTS. Para pyttsx3, você pode instalar vozes adicionais no seu sistema operacional. Para edge-tts e gTTS, as vozes são fornecidas pelos serviços respectivos.

**P: Como adicionar mais imagens de fundo?**
R: Coloque as imagens no diretório `resources/backgrounds/images/` ou use o método `add_image()` do `BackgroundManager`.

**P: Posso personalizar o estilo das legendas além dos predefinidos?**
R: Sim, você pode criar um estilo personalizado modificando o dicionário `predefined_styles` no arquivo `subtitle_synchronization_mechanism.py`.

### 8.3 Desempenho

**P: Quanto tempo leva para gerar um vídeo?**
R: O tempo de geração depende de vários fatores, incluindo o comprimento do texto, o motor TTS escolhido, o tipo de fundo e o hardware do seu sistema. Em média, um vídeo de 30 segundos leva de 1 a 3 minutos para ser gerado.

**P: O módulo usa GPU para acelerar o processamento?**
R: O módulo não usa GPU diretamente, mas algumas bibliotecas subjacentes (como transformers para geração de roteiro) podem usar GPU se disponível.

**P: Como otimizar o desempenho?**
R: Use pyttsx3 para geração de voz offline mais rápida, prefira fundos de cor sólida ou gradiente em vez de vídeos, e use um estilo de legenda simples como "standard" ou "minimal".

---

## Exemplos de Código

### Exemplo 1: Geração Básica de Vídeo

```python
from video_generator_module import VideoGenerator

# Inicializar o gerador com configurações padrão
generator = VideoGenerator()

# Gerar vídeo a partir de texto
video_path = generator.generate_video_from_text(
    "Este é um exemplo de vídeo gerado automaticamente pelo ZudoEditor. "
    "O sistema converte texto em narração, adiciona legendas sincronizadas "
    "e aplica um fundo visual para criar um vídeo completo."
)

print(f"Vídeo gerado: {video_path}")
```

### Exemplo 2: Personalização Completa

```python
from video_generator_module import VideoGenerator, VideoGeneratorConfig
from subtitle_synchronization_mechanism import SubtitleStyle, SubtitlePosition
from background_selection_system import BackgroundType

# Criar configuração personalizada
config = VideoGeneratorConfig(
    # Configurações de vídeo
    video_width=1920,
    video_height=1080,
    video_fps=30,
    
    # Configurações de TTS
    tts_engine="edge-tts",
    tts_voice="pt-BR-AntonioNeural",
    speech_rate=150,
    
    # Configurações de fundo
    background_type=BackgroundType.GRADIENT,
    background_source="Azul para Roxo",
    
    # Configurações de legenda
    subtitle_style=SubtitleStyle.MODERN,
    subtitle_position=SubtitlePosition.BOTTOM,
    export_subtitle_file=True,
    
    # Configurações de saída
    output_dir="/caminho/para/videos/gerados",
    input_dir="/caminho/para/zudoeditor/entrada"
)

# Inicializar o gerador com a configuração personalizada
generator = VideoGenerator(config)

# Gerar vídeo a partir de um tópico
video_path = generator.generate_video_from_topic(
    "inteligência artificial na educação",
    "ia_educacao.mp4"
)

print(f"Vídeo gerado: {video_path}")
```

### Exemplo 3: Script para Processamento em Lote

```python
import os
from video_generator_module import VideoGenerator

def process_topics_file(file_path, output_dir):
    """
    Processa um arquivo de tópicos e gera um vídeo para cada linha.
    
    Args:
        file_path: Caminho para o arquivo de tópicos (um tópico por linha)
        output_dir: Diretório para salvar os vídeos gerados
    """
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Inicializar o gerador
    generator = VideoGenerator()
    
    # Ler tópicos do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        topics = [line.strip() for line in f if line.strip()]
    
    # Gerar vídeo para cada tópico
    for i, topic in enumerate(topics, 1):
        print(f"Processando tópico {i}/{len(topics)}: {topic}")
        
        # Gerar nome de arquivo baseado no tópico
        filename = f"{i:02d}_{topic.replace(' ', '_')[:30]}.mp4"
        output_path = os.path.join(output_dir, filename)
        
        # Gerar vídeo
        result = generator.generate_video_from_topic(topic, output_path)
        
        if result:
            print(f"Vídeo gerado: {result}")
        else:
            print(f"Falha ao gerar vídeo para o tópico: {topic}")

# Exemplo de uso
if __name__ == "__main__":
    process_topics_file("topicos.txt", "videos_gerados")
```

---

Esta documentação fornece uma visão geral completa do Módulo de Geração Automática de Vídeos com IA para o ZudoEditor. Para mais informações ou suporte, consulte a documentação do ZudoEditor ou entre em contato com a equipe de suporte.

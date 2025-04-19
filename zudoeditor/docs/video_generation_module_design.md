# Design do Módulo de Geração Automática de Vídeos com IA

## Visão Geral

Este documento descreve o design do novo módulo de geração automática de vídeos com IA para o ZudoEditor. O módulo permitirá que os usuários criem vídeos completos a partir de um texto ou roteiro, com narração por voz sintética, legendas sincronizadas e fundos visuais personalizáveis.

## Arquitetura do Módulo

O módulo de geração automática de vídeos será integrado ao ZudoEditor como um componente independente, mantendo todas as funcionalidades existentes intactas. A arquitetura seguirá um design modular para facilitar a manutenção e futuras expansões.

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                       ZudoEditor (Existente)                     │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐  │
│  │                 │    │                 │    │              │  │
│  │ Monitoramento   │    │ Edição          │    │ Sistema de   │  │
│  │ de Pasta        │    │ Inteligente     │    │ Aprendizado  │  │
│  │                 │    │                 │    │              │  │
│  └─────────────────┘    └─────────────────┘    └──────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                                                             │  │
│  │              Módulo de Geração de Vídeos (Novo)             │  │
│  │                                                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │
│  │  │             │  │             │  │                     │  │  │
│  │  │ Gerador de  │  │ Conversor   │  │ Seletor de Fundo    │  │  │
│  │  │ Roteiro     │  │ Texto-Fala  │  │ Visual              │  │  │
│  │  │             │  │             │  │                     │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │  │
│  │                                                             │  │
│  │  ┌─────────────────────┐  ┌─────────────────────────────┐  │  │
│  │  │                     │  │                             │  │  │
│  │  │ Gerador de Legendas │  │ Compositor de Vídeo Final   │  │  │
│  │  │                     │  │                             │  │  │
│  │  └─────────────────────┘  └─────────────────────────────┘  │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Interface do Usuário

A interface do usuário será expandida para incluir uma nova seção "Criar Vídeo com IA" com os seguintes elementos:

- Campo de texto para inserção direta do roteiro
- Botão "Gerar Roteiro com IA" para criação automática de roteiro
- Campo para inserir o assunto do vídeo (usado quando o roteiro é gerado automaticamente)
- Seletor de voz para a narração (com opções de vozes disponíveis)
- Seletor de fundo visual (cor sólida, imagem ou vídeo)
- Controles de personalização (duração, estilo de legenda, etc.)
- Botão "Gerar Vídeo" para iniciar o processo de criação

### 2. Gerador de Roteiro

Este componente será responsável por criar um roteiro a partir de um assunto fornecido pelo usuário:

- Utilizará um modelo de IA local para gerar o texto
- Limitará o roteiro a uma duração adequada para vídeos curtos (15-60 segundos)
- Formatará o texto para otimizar a narração e legibilidade
- Opções para ajustar o tom, estilo e comprimento do roteiro

### 3. Conversor Texto-Fala (TTS)

Este componente transformará o texto do roteiro em narração de áudio:

- Suportará múltiplas bibliotecas TTS (pyttsx3, gTTS, edge-tts, etc.)
- Permitirá a seleção de diferentes vozes e ajustes de velocidade
- Otimizará a qualidade do áudio para uso em vídeos
- Salvará o áudio em formato compatível com o compositor de vídeo

### 4. Seletor de Fundo Visual

Este componente gerenciará o fundo visual do vídeo:

- Permitirá a seleção de cores sólidas, imagens estáticas ou vídeos de fundo
- Incluirá uma biblioteca de recursos visuais pré-selecionados
- Suportará o upload de imagens ou vídeos personalizados
- Aplicará filtros e ajustes visuais para melhorar a aparência

### 5. Gerador de Legendas

Este componente criará e sincronizará legendas com a narração:

- Utilizará o texto do roteiro para gerar as legendas
- Sincronizará as legendas com o áudio gerado
- Aplicará estilos visuais às legendas (fonte, tamanho, cor, etc.)
- Otimizará a legibilidade e posicionamento no vídeo

### 6. Compositor de Vídeo Final

Este componente combinará todos os elementos em um vídeo final:

- Integrará o áudio de narração com o fundo visual
- Sobreporá as legendas sincronizadas
- Aplicará transições e efeitos conforme necessário
- Exportará o vídeo no formato adequado para o sistema principal
- Moverá automaticamente o vídeo para a pasta de entrada do ZudoEditor

## Fluxo de Trabalho

1. O usuário acessa a nova seção "Criar Vídeo com IA" no painel do ZudoEditor
2. O usuário insere um roteiro ou solicita a geração automática de um roteiro
3. O usuário seleciona as opções de voz, fundo visual e estilo de legenda
4. O usuário clica em "Gerar Vídeo" para iniciar o processo
5. O sistema gera o áudio de narração a partir do texto
6. O sistema prepara o fundo visual selecionado
7. O sistema cria e sincroniza as legendas com o áudio
8. O sistema compõe o vídeo final combinando todos os elementos
9. O vídeo final é exportado para a pasta de entrada do ZudoEditor
10. O sistema principal do ZudoEditor detecta o novo vídeo e inicia o processamento normal

## Tecnologias Recomendadas

### Geração de Roteiro
- Modelo de linguagem local leve (GPT2, BERT, etc.)
- Alternativa: Templates pré-definidos com preenchimento de variáveis

### Conversão Texto-Fala
- Primeira opção: edge-tts (Microsoft Edge TTS) - boa qualidade e gratuito
- Alternativas: pyttsx3 (offline, mais leve), gTTS (Google TTS, requer internet)
- Opção premium: ElevenLabs API (limitada na versão gratuita)

### Processamento de Vídeo
- MoviePy para composição e edição de vídeo
- OpenCV para processamento de imagem (se necessário)
- FFmpeg para codificação e otimização final

### Geração de Legendas
- Método direto: Sincronização baseada no tempo estimado por palavra/caractere
- Alternativa: Whisper para transcrição e sincronização do áudio gerado

## Requisitos Técnicos

### Dependências de Software
- Python 3.8+
- MoviePy
- Biblioteca TTS selecionada (edge-tts, pyttsx3, etc.)
- FFmpeg
- Pillow para processamento de imagem
- Modelo de linguagem leve (opcional)

### Requisitos de Sistema
- CPU: Processador quad-core moderno
- RAM: Mínimo de 4GB, recomendado 8GB
- Armazenamento: 1GB para bibliotecas e recursos + espaço para vídeos
- GPU: Não obrigatório, mas recomendado para processamento mais rápido

## Considerações de Implementação

### Integração com o Sistema Existente
- O novo módulo será implementado como um componente independente
- Nenhuma modificação será feita nos componentes existentes
- A comunicação entre o novo módulo e o sistema existente será feita através do sistema de arquivos (pasta de entrada)

### Extensibilidade
- O design modular permitirá a adição de novos recursos no futuro
- Interfaces bem definidas facilitarão a substituição de componentes individuais
- Configurações serão armazenadas em arquivos externos para fácil personalização

### Desempenho
- Operações intensivas serão executadas em threads separadas para manter a interface responsiva
- Caching de recursos frequentemente utilizados para melhorar o desempenho
- Opções de qualidade ajustáveis para equilibrar velocidade e qualidade do resultado

## Próximos Passos

1. Implementar o componente de conversão texto-fala
2. Desenvolver o sistema de seleção de fundo visual
3. Criar o mecanismo de sincronização de legendas
4. Implementar o compositor de vídeo final
5. Integrar todos os componentes em um módulo coeso
6. Testar a integração com o sistema existente
7. Documentar o uso e configuração do novo módulo
8. Atualizar o site com informações sobre a nova funcionalidade

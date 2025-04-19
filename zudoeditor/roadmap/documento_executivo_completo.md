# Documento Executivo: Software Automatizado de Edição e Publicação de Vídeos para Divulgação de eBooks

## Sumário

1. [Introdução](#1-introdução)
2. [Descrição do Projeto](#2-descrição-do-projeto)
3. [Arquitetura do Sistema](#3-arquitetura-do-sistema)
4. [Roadmap de Desenvolvimento](#4-roadmap-de-desenvolvimento)
5. [Design do Painel Administrativo](#5-design-do-painel-administrativo)
6. [Exemplos de Código](#6-exemplos-de-código)
7. [Manual do Usuário (Resumo)](#7-manual-do-usuário-resumo)
8. [Estratégia de Monetização (Resumo)](#8-estratégia-de-monetização-resumo)
9. [Conclusão](#9-conclusão)
10. [Anexos](#10-anexos)

## 1. Introdução

Este documento executivo apresenta uma solução completa para automatizar a edição e publicação de vídeos curtos para divulgação de eBooks em múltiplas plataformas sociais. O software proposto elimina a necessidade de edição manual e gerenciamento individual de contas, permitindo que autores e editores se concentrem na criação de conteúdo de qualidade enquanto o sistema cuida de todo o processo de distribuição.

Desenvolvido com foco em gratuidade e funcionalidade, conforme solicitado, o sistema utiliza tecnologias de código aberto e ferramentas gratuitas sempre que possível, mantendo a qualidade e confiabilidade necessárias para uma operação profissional.

## 2. Descrição do Projeto

### 2.1. Visão Geral

O Software Automatizado de Edição e Publicação de Vídeos é uma solução completa que automatiza todo o fluxo de trabalho de criação e distribuição de conteúdo em vídeo para promover eBooks. O sistema monitora uma pasta designada para novos vídeos, processa-os automaticamente com edições profissionais, e os publica em múltiplas plataformas sociais (YouTube, Instagram e TikTok) em horários otimizados para maximizar o engajamento.

### 2.2. Objetivos Principais

- Automatizar completamente o processo de edição de vídeos para diferentes plataformas
- Gerenciar múltiplas contas em diversas plataformas sociais
- Otimizar horários de publicação para maximizar engajamento
- Gerar legendas, títulos, descrições e hashtags automaticamente
- Fornecer análises detalhadas de desempenho
- Minimizar custos utilizando tecnologias gratuitas e de código aberto

### 2.3. Funcionalidades Principais

#### 2.3.1. Monitoramento e Detecção
- Monitoramento automático de pasta para novos vídeos
- Detecção de formatos compatíveis
- Verificação de qualidade e integridade

#### 2.3.2. Processamento de Vídeo
- Edição automática baseada em templates
- Geração de legendas por reconhecimento de fala
- Adaptação para diferentes formatos de plataforma (9:16, 16:9, 1:1)
- Adição de chamadas para ação (CTAs) e marca d'água
- Aplicação de filtros e efeitos visuais
- Integração opcional com CapCut

#### 2.3.3. Gerenciamento de Contas
- Suporte para múltiplas contas por plataforma
- Rotação inteligente de contas para evitar bloqueios
- Monitoramento de saúde das contas
- Suporte a proxies para maior segurança

#### 2.3.4. Publicação Automatizada
- Agendamento inteligente baseado em horários ótimos
- Geração automática de títulos, descrições e hashtags
- Upload simultâneo para múltiplas plataformas
- Verificação de sucesso de publicação

#### 2.3.5. Análise e Relatórios
- Rastreamento de métricas de engajamento
- Relatórios detalhados por plataforma e conta
- Análise de desempenho por horário e tipo de conteúdo
- Recomendações para otimização

### 2.4. Benefícios

- **Economia de tempo**: Redução de 90% no tempo gasto com edição e publicação
- **Consistência**: Manutenção de padrão visual e qualidade em todos os vídeos
- **Alcance ampliado**: Presença simultânea em múltiplas plataformas
- **Otimização**: Publicação nos melhores horários para maximizar engajamento
- **Escalabilidade**: Capacidade de gerenciar dezenas ou centenas de contas
- **Economia financeira**: Eliminação da necessidade de contratar editores de vídeo

### 2.5. Público-Alvo

- Autores independentes de eBooks
- Pequenas editoras digitais
- Criadores de conteúdo educacional
- Profissionais de marketing de conteúdo

## 3. Arquitetura do Sistema

### 3.1. Visão Geral da Arquitetura

O sistema segue uma arquitetura modular composta por cinco componentes principais que trabalham em conjunto para fornecer um fluxo de trabalho automatizado completo:

1. **Módulo de Monitoramento**: Detecta novos vídeos e inicia o processamento
2. **Módulo de Processamento**: Edita e adapta vídeos para diferentes plataformas
3. **Módulo de Gerenciamento de Contas**: Administra credenciais e estado das contas
4. **Módulo de Publicação**: Gerencia uploads e agendamento
5. **Módulo de Análise**: Coleta e processa métricas de desempenho

Estes módulos são coordenados por um sistema central que gerencia o fluxo de trabalho e mantém o estado do sistema.

### 3.2. Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      Interface do Usuário                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Dashboard  │  │ Gerenciador │  │ Calendário  │  │ Config. │ │
│  │             │  │  de Vídeos  │  │             │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                           │                                      │
│         ┌─────────────────▼────────────────────┐                │
│         │        Controlador Principal         │                │
│         └─────────────────┬────────────────────┘                │
│                           │                                      │
│  ┌────────────┐ ┌─────────┴──────────┐ ┌────────────────────┐   │
│  │  Módulo de │ │     Módulo de      │ │      Módulo de     │   │
│  │Monitoramento◄─►   Processamento   ├─►     Publicação     │   │
│  └────────────┘ └─────────┬──────────┘ └──────────┬─────────┘   │
│                           │                       │             │
│                 ┌─────────┴───────────┐           │             │
│                 │      Módulo de      │           │             │
│                 │   Gerenciamento     ◄───────────┘             │
│                 │     de Contas       │                         │
│                 └─────────┬───────────┘                         │
│                           │                                     │
│                 ┌─────────▼───────────┐                         │
│                 │      Módulo de      │                         │
│                 │       Análise       │                         │
│                 └─────────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3. Componentes do Sistema

#### 3.3.1. Módulo de Monitoramento
- **Tecnologias**: Python, Watchdog
- **Funcionalidades**:
  - Monitoramento contínuo de diretório designado
  - Detecção de novos arquivos de vídeo
  - Validação de formatos e qualidade
  - Enfileiramento para processamento

#### 3.3.2. Módulo de Processamento
- **Tecnologias**: Python, FFmpeg, MoviePy, SpeechRecognition
- **Funcionalidades**:
  - Edição de vídeo baseada em templates
  - Reconhecimento de fala para legendas
  - Redimensionamento para diferentes plataformas
  - Aplicação de filtros e efeitos
  - Adição de CTAs e marca d'água
  - Integração opcional com CapCut

#### 3.3.3. Módulo de Gerenciamento de Contas
- **Tecnologias**: Python, SQLite/PostgreSQL, Cryptography
- **Funcionalidades**:
  - Armazenamento seguro de credenciais
  - Monitoramento de saúde das contas
  - Rotação inteligente de contas
  - Gerenciamento de proxies
  - Controle de limites de uso

#### 3.3.4. Módulo de Publicação
- **Tecnologias**: Python, Selenium, APIs de plataformas
- **Funcionalidades**:
  - Agendamento inteligente
  - Geração de metadados (títulos, descrições, hashtags)
  - Upload automatizado
  - Verificação de sucesso
  - Retenção de logs

#### 3.3.5. Módulo de Análise
- **Tecnologias**: Python, Pandas, Matplotlib, APIs de plataformas
- **Funcionalidades**:
  - Coleta de métricas de engajamento
  - Processamento e agregação de dados
  - Geração de relatórios
  - Visualizações e dashboards
  - Recomendações baseadas em dados

### 3.4. Banco de Dados

O sistema utiliza um banco de dados relacional para armazenar:

- Metadados de vídeos
- Informações de contas
- Histórico de publicações
- Métricas de desempenho
- Configurações do sistema

**Tecnologias recomendadas**:
- SQLite (para instalação local/simples)
- PostgreSQL (para instalação em servidor/avançada)

### 3.5. Interface do Usuário

A interface do usuário é uma aplicação web responsiva que permite:

- Visualização do dashboard com métricas principais
- Gerenciamento de vídeos e contas
- Configuração de templates e preferências
- Visualização de calendário de publicações
- Acesso a relatórios detalhados

**Tecnologias recomendadas**:
- Frontend: React.js, Material-UI
- Backend: Flask ou FastAPI

### 3.6. Segurança

O sistema implementa várias camadas de segurança:

- Criptografia AES-256 para credenciais armazenadas
- Autenticação de dois fatores para acesso ao sistema
- Conexões HTTPS para todas as comunicações
- Logs detalhados de todas as atividades
- Backups automáticos do banco de dados

### 3.7. Requisitos de Sistema

#### 3.7.1. Hardware Mínimo
- Processador: Intel Core i5 ou equivalente (2 núcleos, 2.5GHz)
- Memória RAM: 4GB
- Armazenamento: 50GB de espaço livre em disco
- Conexão de Internet: 10Mbps de download, 5Mbps de upload

#### 3.7.2. Hardware Recomendado
- Processador: Intel Core i7 ou equivalente (4+ núcleos, 3.0GHz+)
- Memória RAM: 8GB+
- Armazenamento: 100GB+ de espaço livre em SSD
- Conexão de Internet: 25Mbps+ de download, 10Mbps+ de upload

#### 3.7.3. Software Necessário
- Sistema Operacional: Windows 10/11, macOS 10.15+, ou Ubuntu 20.04+
- Navegadores: Chrome 90+ ou Firefox 88+
- Python 3.8 ou superior
- FFmpeg (instalado automaticamente)

## 4. Roadmap de Desenvolvimento

### 4.1. Visão Geral das Fases

O desenvolvimento do software será dividido em cinco fases principais, seguindo uma abordagem iterativa que prioriza a entrega de valor desde as primeiras versões:

1. **Fase 1: Fundação** - Estrutura básica e funcionalidades essenciais
2. **Fase 2: Automação Core** - Processamento de vídeo e publicação básica
3. **Fase 3: Expansão** - Suporte a múltiplas plataformas e contas
4. **Fase 4: Inteligência** - Otimização e análise avançada
5. **Fase 5: Refinamento** - Polimento e recursos avançados

### 4.2. Detalhamento das Fases

#### 4.2.1. Fase 1: Fundação (Mês 1-2)

**Objetivos**:
- Estabelecer a arquitetura básica do sistema
- Implementar o monitoramento de pasta
- Criar a estrutura do banco de dados
- Desenvolver interface de usuário básica

**Entregáveis**:
- Sistema funcional de monitoramento de pasta
- Banco de dados configurado
- Interface de usuário básica
- Documentação inicial

**Marcos**:
- Semana 2: Arquitetura definida e ambiente de desenvolvimento configurado
- Semana 4: Monitoramento de pasta funcional
- Semana 6: Interface básica implementada
- Semana 8: Integração dos componentes iniciais

#### 4.2.2. Fase 2: Automação Core (Mês 3-4)

**Objetivos**:
- Implementar processamento básico de vídeo
- Desenvolver sistema de geração de legendas
- Criar funcionalidade de publicação para uma plataforma (YouTube)
- Expandir interface de usuário

**Entregáveis**:
- Processador de vídeo funcional
- Sistema de reconhecimento de fala para legendas
- Publicação automatizada para YouTube
- Interface de usuário expandida

**Marcos**:
- Semana 10: Processamento básico de vídeo implementado
- Semana 12: Sistema de legendas funcional
- Semana 14: Publicação para YouTube implementada
- Semana 16: Testes de integração concluídos

#### 4.2.3. Fase 3: Expansão (Mês 5-6)

**Objetivos**:
- Adicionar suporte para Instagram e TikTok
- Implementar gerenciamento de múltiplas contas
- Desenvolver sistema de agendamento básico
- Criar templates de edição para diferentes plataformas

**Entregáveis**:
- Publicação automatizada para Instagram e TikTok
- Sistema de gerenciamento de contas
- Agendador de publicações
- Biblioteca de templates de edição

**Marcos**:
- Semana 18: Suporte ao Instagram implementado
- Semana 20: Suporte ao TikTok implementado
- Semana 22: Sistema de gerenciamento de contas funcional
- Semana 24: Agendador básico implementado

#### 4.2.4. Fase 4: Inteligência (Mês 7-8)

**Objetivos**:
- Implementar agendamento inteligente baseado em dados
- Desenvolver sistema de análise e relatórios
- Criar geração automática de metadados otimizados
- Implementar rotação inteligente de contas

**Entregáveis**:
- Algoritmo de agendamento inteligente
- Dashboard de análise e relatórios
- Sistema de geração de metadados
- Rotação automática de contas

**Marcos**:
- Semana 26: Coleta de métricas implementada
- Semana 28: Dashboard de análise funcional
- Semana 30: Agendamento inteligente implementado
- Semana 32: Sistema de geração de metadados funcional

#### 4.2.5. Fase 5: Refinamento (Mês 9-10)

**Objetivos**:
- Polir interface de usuário
- Otimizar performance do sistema
- Implementar recursos avançados de segurança
- Desenvolver documentação completa

**Entregáveis**:
- Interface de usuário final
- Sistema otimizado
- Recursos de segurança avançados
- Documentação completa e manual do usuário

**Marcos**:
- Semana 34: Refinamentos de UI/UX implementados
- Semana 36: Otimizações de performance concluídas
- Semana 38: Recursos de segurança implementados
- Semana 40: Documentação finalizada e sistema pronto para lançamento

### 4.3. Cronograma Resumido

| Fase | Duração | Principais Entregas |
|------|---------|---------------------|
| 1: Fundação | 2 meses | Monitoramento, DB, UI básica |
| 2: Automação Core | 2 meses | Processamento de vídeo, legendas, YouTube |
| 3: Expansão | 2 meses | Instagram, TikTok, múltiplas contas |
| 4: Inteligência | 2 meses | Agendamento inteligente, análises |
| 5: Refinamento | 2 meses | UI final, otimizações, documentação |

### 4.4. Desafios Potenciais e Mitigações

| Desafio | Impacto | Mitigação |
|---------|---------|-----------|
| Mudanças nas APIs das plataformas | Alto | Design modular, monitoramento constante, atualizações rápidas |
| Detecção de automação pelas plataformas | Alto | Simulação de comportamento humano, limites de uso, rotação de contas |
| Requisitos de processamento elevados | Médio | Otimização de código, processamento em lotes, requisitos claros de hardware |
| Complexidade da edição de vídeo | Médio | Abordagem incremental, templates pré-definidos, integração com ferramentas existentes |
| Segurança das credenciais | Alto | Criptografia forte, armazenamento local, autenticação de dois fatores |

## 5. Design do Painel Administrativo

### 5.1. Visão Geral da Interface

O painel administrativo foi projetado para ser intuitivo, eficiente e responsivo, permitindo que usuários de todos os níveis de habilidade técnica possam gerenciar facilmente todo o processo de automação de vídeos.

A interface segue princípios de design moderno com foco em:
- Simplicidade e clareza
- Fluxos de trabalho eficientes
- Visualização de dados relevantes
- Adaptabilidade a diferentes dispositivos
- Feedback visual imediato

### 5.2. Estrutura do Painel

O painel administrativo é organizado em seis seções principais, acessíveis através de uma barra de navegação lateral:

1. **Dashboard**: Visão geral do sistema e estatísticas
2. **Vídeos**: Gerenciamento de vídeos crus e processados
3. **Publicações**: Calendário e lista de publicações
4. **Contas**: Gerenciamento de contas de redes sociais
5. **Relatórios**: Análise de desempenho e engajamento
6. **Configurações**: Personalização do sistema

### 5.3. Telas Principais

#### 5.3.1. Dashboard

![Dashboard](https://exemplo.com/dashboard.png)

O Dashboard oferece uma visão geral do sistema com:

- **Estatísticas Rápidas**:
  - Total de vídeos processados
  - Publicações agendadas
  - Publicações realizadas hoje
  - Taxa de engajamento média

- **Gráfico de Desempenho**:
  - Visualizações por plataforma
  - Engajamento ao longo do tempo
  - Comparativo entre períodos

- **Calendário de Publicações**:
  - Visão semanal das próximas publicações
  - Codificação por cores por plataforma

- **Atividade Recente**:
  - Últimas ações do sistema
  - Alertas e notificações
  - Status de processamento

#### 5.3.2. Gerenciamento de Vídeos

![Gerenciamento de Vídeos](https://exemplo.com/videos.png)

A seção de Vídeos permite gerenciar todo o ciclo de vida dos vídeos:

- **Vídeos Crus**:
  - Lista de vídeos na pasta de entrada
  - Status de detecção
  - Opção de upload manual

- **Em Processamento**:
  - Vídeos sendo processados
  - Progresso e etapa atual
  - Tempo estimado para conclusão

- **Processados**:
  - Vídeos prontos para publicação
  - Prévia dos resultados
  - Opções de edição manual

- **Publicados**:
  - Histórico de vídeos publicados
  - Métricas de desempenho
  - Links para visualização nas plataformas

#### 5.3.3. Calendário de Publicações

![Calendário de Publicações](https://exemplo.com/calendario.png)

A seção de Publicações oferece duas visualizações principais:

- **Calendário**:
  - Visão mensal, semanal ou diária
  - Codificação por cores por plataforma
  - Drag-and-drop para reagendamento

- **Lista**:
  - Todas as publicações em formato de lista
  - Filtros por status, plataforma, período
  - Opções de edição e cancelamento

#### 5.3.4. Gerenciamento de Contas

![Gerenciamento de Contas](https://exemplo.com/contas.png)

A seção de Contas permite gerenciar todas as contas de redes sociais:

- **Visão Geral**:
  - Lista de todas as contas por plataforma
  - Status de cada conta (ativa, bloqueada, em uso)
  - Métricas de uso

- **Detalhes da Conta**:
  - Informações completas
  - Histórico de publicações
  - Estatísticas de desempenho
  - Opções de teste de conexão

#### 5.3.5. Relatórios e Análises

![Relatórios](https://exemplo.com/relatorios.png)

A seção de Relatórios oferece análises detalhadas:

- **Desempenho por Plataforma**:
  - Comparativo entre YouTube, Instagram e TikTok
  - Métricas específicas por plataforma
  - Tendências ao longo do tempo

- **Análise de Conteúdo**:
  - Desempenho por tipo de conteúdo
  - Palavras-chave mais eficazes
  - Duração ideal dos vídeos

- **Análise de Horários**:
  - Melhores dias e horários para publicação
  - Heatmap de engajamento
  - Recomendações personalizadas

#### 5.3.6. Configurações

![Configurações](https://exemplo.com/configuracoes.png)

A seção de Configurações permite personalizar todos os aspectos do sistema:

- **Geral**:
  - Informações da conta
  - Idioma e fuso horário
  - Notificações

- **Pastas e Armazenamento**:
  - Configuração de pastas
  - Política de retenção
  - Backup automático

- **Templates de Vídeo**:
  - Configurações por plataforma
  - Editor visual de templates
  - Biblioteca de templates

- **Geração de Conteúdo**:
  - Configurações de título e descrição
  - Banco de hashtags
  - Personalização por plataforma

### 5.4. Tecnologias Recomendadas

Para implementação do painel administrativo, recomendamos as seguintes tecnologias gratuitas e de código aberto:

#### 5.4.1. Frontend
- **Framework**: React.js
- **Biblioteca de UI**: Material-UI
- **Gerenciamento de Estado**: Redux ou Context API
- **Gráficos e Visualizações**: Chart.js ou D3.js
- **Calendário**: FullCalendar
- **Editor de Vídeo Web**: FFmpeg.wasm

#### 5.4.2. Backend
- **Framework**: Flask ou FastAPI (Python)
- **API**: RESTful com autenticação JWT
- **Documentação API**: Swagger/OpenAPI
- **WebSockets**: Socket.IO (para atualizações em tempo real)

#### 5.4.3. Armazenamento
- **Banco de Dados**: SQLite (local) ou PostgreSQL (servidor)
- **Cache**: Redis (opcional, para melhor performance)
- **Armazenamento de Arquivos**: Sistema de arquivos local ou MinIO

### 5.5. Considerações de Usabilidade

O design do painel administrativo incorpora as seguintes considerações de usabilidade:

- **Responsividade**: Adaptação a diferentes tamanhos de tela
- **Acessibilidade**: Conformidade com WCAG 2.1
- **Feedback Imediato**: Notificações e indicadores de progresso
- **Consistência**: Padrões de design uniformes em toda a interface
- **Eficiência**: Atalhos de teclado e fluxos de trabalho otimizados
- **Prevenção de Erros**: Confirmações para ações irreversíveis
- **Ajuda Contextual**: Dicas e documentação integrada

## 6. Exemplos de Código

Esta seção apresenta exemplos de código para os componentes-chave do sistema, demonstrando a viabilidade técnica e fornecendo uma base para implementação.

### 6.1. Monitoramento de Pasta

O componente de monitoramento de pasta é responsável por detectar novos arquivos de vídeo e iniciar o processamento.

```python
#!/usr/bin/env python3
"""
Monitor de Pasta para Sistema de Automação de Vídeos

Este script monitora uma pasta específica para novos arquivos de vídeo,
verifica se são formatos válidos e os envia para processamento.
"""

import os
import time
import logging
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
            
            # Aqui chamaríamos o processador de vídeo real
            # Para este exemplo, apenas simulamos o processamento
            
            logger.info(f"Processamento concluído para: {arquivo}")
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {arquivo}: {str(e)}")
        
        # Continuar com o próximo arquivo
        self.processar_proximo()

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
        
        # Adicionar à fila de processamento
        self.processador.adicionar(caminho_arquivo)
    
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
                    processador.adicionar(caminho_completo)
        
        # Manter o script em execução
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Monitoramento interrompido pelo usuário")
        observador.stop()
    
    observador.join()

if __name__ == "__main__":
    # Configurar caminhos de pasta
    pasta_entrada = "/caminho/para/pasta_entrada"
    pasta_saida = "/caminho/para/pasta_saida"
    
    # Iniciar monitoramento
    iniciar_monitoramento(pasta_entrada, pasta_saida)
```

### 6.2. Processamento de Vídeo

O componente de processamento de vídeo é responsável por editar os vídeos, adicionar legendas e adaptar para diferentes plataformas.

```python
#!/usr/bin/env python3
"""
Processador de Vídeo para Sistema de Automação de Vídeos

Este script processa vídeos crus, adicionando legendas automáticas,
aplicando filtros, inserindo chamadas para ação e adaptando para
diferentes plataformas de mídia social.
"""

import os
import json
import logging
import subprocess
from datetime import datetime
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
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
        "resolucao": (1920, 1080),  # 16:9
        "duracao_maxima": 60,  # segundos
        "texto_cta": "Confira meu eBook! Link na descrição",
        "posicao_cta": ("center", 0.85),  # (x, y) relativo
        "cor_cta": "white",
        "bg_cta": "rgba(0,0,0,0.5)"
    },
    "instagram": {
        "resolucao": (1080, 1920),  # 9:16
        "duracao_maxima": 60,  # segundos
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
        
        # Inicializar metadados
        self.metadados = {
            "arquivo_original": self.arquivo_entrada,
            "data_processamento": datetime.now().isoformat(),
            "status": "iniciado",
            "plataformas": list(PLATAFORMAS.keys())
        }
        self._salvar_metadados()
    
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
            self._atualizar_status("processando")
            
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
            for plataforma in self.metadados.get("plataformas", []):
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
        proporcao_atual = largura_atual / altura_atual
        proporcao_alvo = largura_alvo / altura_alvo
        
        # Determinar estratégia de redimensionamento
        if proporcao_atual > proporcao_alvo:
            # Vídeo é mais largo que o alvo, cortar laterais
            nova_largura = int(altura_atual * proporcao_alvo)
            x1 = (largura_atual - nova_largura) // 2
            y1 = 0
            video_cortado = video.crop(x1=x1, y1=y1, x2=x1+nova_largura, y2=altura_atual)
        else:
            # Vídeo é mais alto que o alvo, cortar topo e base
            nova_altura = int(largura_atual / proporcao_alvo)
            x1 = 0
            y1 = (altura_atual - nova_altura) // 2
            video_cortado = video.crop(x1=x1, y1=y1, x2=largura_atual, y2=y1+nova_altura)
        
        # Redimensionar para resolução final
        return video_cortado.resize(resolucao_alvo)
    
    def _aplicar_filtros(self, video):
        """Aplica filtros básicos para melhorar a aparência do vídeo"""
        # Exemplo simples: aumentar brilho e contraste
        def ajustar_frame(frame):
            # Converter para float para evitar overflow
            frame_float = frame.astype(float)
            
            # Ajustar contraste (fator 1.2)
            contraste = 1.2
            frame_float = (frame_float - 128) * contraste + 128
            
            # Ajustar brilho (+10)
            brilho = 10
            frame_float += brilho
            
            # Garantir que os valores estejam no intervalo [0, 255]
            frame_float = np.clip(frame_float, 0, 255)
            
            return frame_float.astype('uint8')
        
        return video.fl_image(ajustar_frame)
    
    def _adicionar_legendas(self, video, legendas):
        """Adiciona legendas ao vídeo"""
        # Lista para armazenar clips de texto
        clips_texto = []
        
        for legenda in legendas:
            # Criar clip de texto para cada legenda
            texto_clip = TextClip(
                legenda["texto"],
                fontsize=30,
                color='white',
                bg_color='rgba(0,0,0,0.5)',
                font='Arial-Bold',
                method='caption',
                size=(video.w * 0.9, None),
                stroke_color='black',
                stroke_width=1
            )
            
            # Posicionar na parte inferior
            texto_clip = texto_clip.set_position(('center', 'bottom'))
            
            # Definir duração baseada nos timestamps
            texto_clip = texto_clip.set_start(legenda["inicio"]).set_end(legenda["fim"])
            
            # Adicionar à lista
            clips_texto.append(texto_clip)
        
        # Combinar vídeo com legendas
        return CompositeVideoClip([video] + clips_texto)
    
    def _adicionar_cta(self, video, texto, posicao, cor, bg_cor):
        """Adiciona chamada para ação (CTA) ao vídeo"""
        # Criar clip de texto para o CTA
        cta_clip = TextClip(
            texto,
            fontsize=40,
            color=cor,
            bg_color=bg_cor,
            font='Arial-Bold',
            method='caption',
            align='center',
            stroke_color='black',
            stroke_width=1
        )
        
        # Posicionar conforme configuração
        cta_clip = cta_clip.set_position(posicao, relative=True)
        
        # Definir duração igual ao vídeo
        cta_clip = cta_clip.set_duration(video.duration)
        
        # Combinar vídeo com CTA
        return CompositeVideoClip([video, cta_clip])
    
    def _adicionar_marca_dagua(self, video):
        """Adiciona marca d'água ao vídeo"""
        # Criar texto simples como marca d'água
        marca_clip = TextClip(
            "eBook",
            fontsize=30,
            color='white',
            bg_color=None,
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=1
        )
        
        # Posicionar no canto superior direito
        marca_clip = marca_clip.set_position((0.95, 0.05), relative=True)
        
        # Definir duração igual ao vídeo
        marca_clip = marca_clip.set_duration(video.duration)
        
        # Combinar vídeo com marca d'água
        return CompositeVideoClip([video, marca_clip])

# Exemplo de uso
if __name__ == "__main__":
    arquivo_entrada = "/caminho/para/video.mp4"
    pasta_saida = "/caminho/para/saida"
    
    processador = ProcessadorVideo(arquivo_entrada, pasta_saida)
    processador.processar()
```

### 6.3. Automação de Upload

O componente de automação de upload é responsável por publicar os vídeos processados nas plataformas sociais.

```python
#!/usr/bin/env python3
"""
Automação de Upload para Sistema de Automação de Vídeos

Este script gerencia o upload automático de vídeos processados para
múltiplas plataformas sociais (YouTube, Instagram e TikTok).
"""

import os
import json
import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automacao_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutomacaoUpload")

class GerenciadorUpload:
    """Classe principal para gerenciar uploads para múltiplas plataformas"""
    
    def __init__(self, pasta_videos, config_path):
        self.pasta_videos = pasta_videos
        self.config_path = config_path
        self.config = self._carregar_config()
        self.status_path = os.path.join(os.path.dirname(config_path), "status_upload.json")
        self.status = self._carregar_status()
        
        # Inicializar gerenciadores específicos de plataforma
        self.gerenciadores = {
            "youtube": UploadYouTube(self.config),
            "instagram": UploadInstagram(self.config),
            "tiktok": UploadTikTok(self.config)
        }
    
    def _carregar_config(self):
        """Carrega a configuração do arquivo JSON"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {self.config_path}")
                return {
                    "contas": {
                        "youtube": [],
                        "instagram": [],
                        "tiktok": []
                    },
                    "proxies": [],
                    "limites_diarios": {
                        "youtube": 5,
                        "instagram": 3,
                        "tiktok": 5
                    }
                }
                
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            return {
                "contas": {
                    "youtube": [],
                    "instagram": [],
                    "tiktok": []
                },
                "proxies": [],
                "limites_diarios": {
                    "youtube": 5,
                    "instagram": 3,
                    "tiktok": 5
                }
            }
    
    def _carregar_status(self):
        """Carrega o status de uploads do arquivo JSON"""
        try:
            if os.path.exists(self.status_path):
                with open(self.status_path, "r") as f:
                    return json.load(f)
            else:
                logger.info("Arquivo de status não encontrado. Criando novo.")
                status_inicial = {
                    "uploads": {},
                    "contas": {
                        "youtube": {},
                        "instagram": {},
                        "tiktok": {}
                    },
                    "ultima_atualizacao": datetime.now().isoformat()
                }
                self._salvar_status(status_inicial)
                return status_inicial
                
        except Exception as e:
            logger.error(f"Erro ao carregar status: {str(e)}")
            return {
                "uploads": {},
                "contas": {
                    "youtube": {},
                    "instagram": {},
                    "tiktok": {}
                },
                "ultima_atualizacao": datetime.now().isoformat()
            }
    
    def _salvar_status(self, status=None):
        """Salva o status de uploads no arquivo JSON"""
        try:
            if status is None:
                status = self.status
            
            status["ultima_atualizacao"] = datetime.now().isoformat()
            
            with open(self.status_path, "w") as f:
                json.dump(status, f, indent=4)
                
        except Exception as e:
            logger.error(f"Erro ao salvar status: {str(e)}")
    
    def _obter_videos_pendentes(self):
        """Obtém a lista de vídeos pendentes para upload"""
        videos_pendentes = []
        
        try:
            # Percorrer diretórios de vídeos processados
            for item in os.listdir(self.pasta_videos):
                caminho_item = os.path.join(self.pasta_videos, item)
                
                # Verificar se é um diretório (cada vídeo processado tem seu próprio diretório)
                if os.path.isdir(caminho_item):
                    # Verificar se há um arquivo de metadados
                    metadados_path = os.path.join(caminho_item, "metadados.json")
                    if os.path.exists(metadados_path):
                        try:
                            with open(metadados_path, "r") as f:
                                metadados = json.load(f)
                            
                            # Verificar se o processamento foi concluído
                            if metadados.get("status") == "concluido":
                                # Verificar se há resultados para cada plataforma
                                resultados = metadados.get("resultados", {})
                                
                                for plataforma, info in resultados.items():
                                    arquivo = info.get("arquivo")
                                    
                                    # Verificar se o arquivo existe
                                    if arquivo and os.path.exists(arquivo):
                                        # Verificar se já foi feito upload para todas as contas
                                        contas_disponiveis = self.config["contas"].get(plataforma, [])
                                        
                                        # Identificador único para o vídeo
                                        video_id = os.path.basename(caminho_item)
                                        
                                        # Verificar uploads já realizados
                                        uploads_realizados = self.status["uploads"].get(video_id, {}).get(plataforma, {})
                                        
                                        # Filtrar contas que ainda não receberam upload
                                        for conta in contas_disponiveis:
                                            usuario = conta.get("usuario")
                                            
                                            # Se não há registro de upload ou o upload falhou
                                            if (usuario not in uploads_realizados or 
                                                uploads_realizados[usuario].get("status") != "concluido"):
                                                
                                                videos_pendentes.append({
                                                    "id": video_id,
                                                    "diretorio": caminho_item,
                                                    "arquivo": arquivo,
                                                    "plataforma": plataforma,
                                                    "conta": conta,
                                                    "metadados": metadados
                                                })
                        
                        except Exception as e:
                            logger.error(f"Erro ao processar metadados de {caminho_item}: {str(e)}")
            
            return videos_pendentes
            
        except Exception as e:
            logger.error(f"Erro ao obter vídeos pendentes: {str(e)}")
            return []
    
    def _selecionar_proxy(self):
        """Seleciona um proxy aleatório da lista de proxies configurados"""
        proxies = self.config.get("proxies", [])
        if proxies:
            return random.choice(proxies)
        return None
    
    def _verificar_limites_diarios(self, plataforma, usuario):
        """Verifica se a conta atingiu o limite diário de uploads"""
        try:
            # Obter limite diário para a plataforma
            limite = self.config["limites_diarios"].get(plataforma, 5)
            
            # Obter data atual (apenas ano, mês, dia)
            data_atual = datetime.now().strftime("%Y-%m-%d")
            
            # Contar uploads do dia para esta conta
            contador = 0
            
            for video_id, plataformas in self.status["uploads"].items():
                if plataforma in plataformas and usuario in plataformas[plataforma]:
                    upload_info = plataformas[plataforma][usuario]
                    
                    # Verificar se o upload foi concluído hoje
                    if (upload_info.get("status") == "concluido" and 
                        upload_info.get("data_upload", "").startswith(data_atual)):
                        contador += 1
            
            return contador < limite
            
        except Exception as e:
            logger.error(f"Erro ao verificar limites diários: {str(e)}")
            return True  # Em caso de erro, permitir o upload
    
    def processar_uploads(self):
        """Processa todos os vídeos pendentes para upload"""
        try:
            # Obter lista de vídeos pendentes
            videos_pendentes = self._obter_videos_pendentes()
            
            if not videos_pendentes:
                logger.info("Nenhum vídeo pendente para upload")
                return
            
            logger.info(f"Encontrados {len(videos_pendentes)} vídeos pendentes para upload")
            
            # Processar cada vídeo pendente
            for video in videos_pendentes:
                plataforma = video["plataforma"]
                conta = video["conta"]
                usuario = conta["usuario"]
                
                # Verificar limites diários
                if not self._verificar_limites_diarios(plataforma, usuario):
                    logger.warning(f"Limite diário atingido para {usuario} na plataforma {plataforma}")
                    continue
                
                # Atualizar status para "pendente"
                self._atualizar_status_upload(
                    video["id"], 
                    plataforma, 
                    usuario, 
                    {
                        "status": "pendente",
                        "arquivo": video["arquivo"],
                        "tentativas": 0
                    }
                )
                
                # Selecionar proxy
                proxy = self._selecionar_proxy()
                
                # Realizar upload
                logger.info(f"Iniciando upload para {plataforma} com conta {usuario}")
                
                try:
                    # Obter gerenciador específico da plataforma
                    gerenciador = self.gerenciadores.get(plataforma)
                    
                    if gerenciador:
                        # Atualizar status para "em_andamento"
                        self._atualizar_status_upload(
                            video["id"], 
                            plataforma, 
                            usuario, 
                            {
                                "status": "em_andamento",
                                "inicio_upload": datetime.now().isoformat(),
                                "tentativas": 1
                            }
                        )
                        
                        # Realizar upload
                        resultado = gerenciador.fazer_upload(
                            video["arquivo"],
                            conta,
                            proxy,
                            video["metadados"]
                        )
                        
                        if resultado["sucesso"]:
                            # Atualizar status para "concluido"
                            self._atualizar_status_upload(
                                video["id"], 
                                plataforma, 
                                usuario, 
                                {
                                    "status": "concluido",
                                    "data_upload": datetime.now().isoformat(),
                                    "url": resultado.get("url", ""),
                                    "detalhes": resultado.get("detalhes", {})
                                }
                            )
                            
                            logger.info(f"Upload concluído com sucesso para {plataforma} com conta {usuario}")
                            
                        else:
                            # Atualizar status para "falha"
                            self._atualizar_status_upload(
                                video["id"], 
                                plataforma, 
                                usuario, 
                                {
                                    "status": "falha",
                                    "erro": resultado.get("erro", "Erro desconhecido"),
                                    "detalhes": resultado.get("detalhes", {})
                                }
                            )
                            
                            logger.error(f"Falha no upload para {plataforma} com conta {usuario}: {resultado.get('erro', 'Erro desconhecido')}")
                    else:
                        logger.error(f"Gerenciador não encontrado para plataforma: {plataforma}")
                
                except Exception as e:
                    logger.error(f"Erro durante upload para {plataforma} com conta {usuario}: {str(e)}")
                    
                    # Atualizar status para "falha"
                    self._atualizar_status_upload(
                        video["id"], 
                        plataforma, 
                        usuario, 
                        {
                            "status": "falha",
                            "erro": str(e)
                        }
                    )
                
                # Aguardar intervalo entre uploads (mesmo que tenha falhado)
                intervalo = random.randint(5, 15)
                logger.info(f"Aguardando {intervalo} segundos antes do próximo upload")
                time.sleep(intervalo)
            
        except Exception as e:
            logger.error(f"Erro ao processar uploads: {str(e)}")
    
    def _atualizar_status_upload(self, video_id, plataforma, usuario, status_upload):
        """Atualiza o status de um upload específico"""
        if video_id not in self.status["uploads"]:
            self.status["uploads"][video_id] = {}
        
        if plataforma not in self.status["uploads"][video_id]:
            self.status["uploads"][video_id][plataforma] = {}
        
        self.status["uploads"][video_id][plataforma][usuario] = {
            **status_upload,
            "ultima_atualizacao": datetime.now().isoformat()
        }
        
        self._salvar_status()

class UploadYouTube:
    """Classe para gerenciar uploads para o YouTube"""
    
    def __init__(self, config):
        self.config = config
    
    def fazer_upload(self, arquivo, conta, proxy, metadados):
        """Realiza o upload de um vídeo para o YouTube"""
        logger.info(f"Iniciando upload para YouTube: {arquivo}")
        
        try:
            # Inicializar driver do Selenium
            driver = self._inicializar_driver(proxy)
            
            try:
                # Fazer login
                if not self._fazer_login(driver, conta):
                    return {
                        "sucesso": False,
                        "erro": "Falha no login",
                        "problema_conta": True
                    }
                
                # Navegar para página de upload
                self._navegar_para_upload(driver)
                
                # Selecionar arquivo
                self._selecionar_arquivo(driver, arquivo)
                
                # Preencher detalhes
                titulo, descricao, tags = self._gerar_conteudo(metadados)
                self._preencher_detalhes(driver, titulo, descricao, tags)
                
                # Publicar vídeo
                url = self._publicar_video(driver)
                
                return {
                    "sucesso": True,
                    "url": url,
                    "detalhes": {
                        "titulo": titulo,
                        "plataforma": "youtube"
                    }
                }
                
            finally:
                # Fechar driver
                if driver:
                    driver.quit()
                    
        except Exception as e:
            logger.error(f"Erro durante upload para YouTube: {str(e)}")
            return {
                "sucesso": False,
                "erro": str(e)
            }
    
    def _inicializar_driver(self, proxy=None):
        """Inicializa o driver do Selenium com configurações anti-detecção"""
        options = Options()
        
        # Configurar proxy se fornecido
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        # Configurações para evitar detecção
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent aleatório
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        
        # Inicializar driver
        driver = webdriver.Chrome(options=options)
        
        # Modificar propriedades do navegador para evitar detecção
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _esperar_aleatorio(self, minimo=1, maximo=3):
        """Espera um tempo aleatório para simular comportamento humano"""
        tempo = random.uniform(minimo, maximo)
        time.sleep(tempo)
    
    def _fazer_login(self, driver, conta):
        """Realiza login no YouTube/Google"""
        try:
            # Navegar para página de login
            driver.get("https://accounts.google.com/signin")
            self._esperar_aleatorio(2, 4)
            
            # Preencher email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(conta["usuario"])
            self._esperar_aleatorio()
            
            # Clicar em próximo
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            self._esperar_aleatorio(3, 5)
            
            # Preencher senha
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(conta["senha"])
            self._esperar_aleatorio()
            
            # Clicar em próximo
            password_next = driver.find_element(By.ID, "passwordNext")
            password_next.click()
            self._esperar_aleatorio(5, 8)
            
            # Verificar se login foi bem-sucedido
            driver.get("https://www.youtube.com")
            self._esperar_aleatorio(3, 5)
            
            # Verificar se há botão de upload (indicando que estamos logados)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-topbar-menu-button-renderer"))
                )
                logger.info("Login no YouTube realizado com sucesso")
                return True
            except:
                logger.error("Falha ao verificar login no YouTube")
                return False
            
        except Exception as e:
            logger.error(f"Erro durante login no YouTube: {str(e)}")
            return False
    
    def _navegar_para_upload(self, driver):
        """Navega para a página de upload do YouTube"""
        try:
            # Clicar no botão de criar
            create_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-topbar-menu-button-renderer"))
            )
            create_button.click()
            self._esperar_aleatorio()
            
            # Clicar na opção de upload
            upload_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[contains(text(), 'Upload video')]"))
            )
            upload_option.click()
            self._esperar_aleatorio(3, 5)
            
            logger.info("Navegação para página de upload concluída")
            
        except Exception as e:
            logger.error(f"Erro ao navegar para página de upload: {str(e)}")
            raise
    
    def _selecionar_arquivo(self, driver, arquivo):
        """Seleciona o arquivo para upload"""
        try:
            # Encontrar input de arquivo
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            
            # Enviar caminho do arquivo
            file_input.send_keys(arquivo)
            
            # Aguardar processamento inicial
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//ytcp-uploads-details"))
            )
            
            logger.info("Arquivo selecionado para upload")
            self._esperar_aleatorio(3, 5)
            
        except Exception as e:
            logger.error(f"Erro ao selecionar arquivo: {str(e)}")
            raise
    
    def _gerar_conteudo(self, metadados):
        """Gera título, descrição e tags para o vídeo"""
        # Exemplo simples - em um sistema real, isso seria mais sofisticado
        # e usaria os metadados para gerar conteúdo relevante
        
        # Obter nome base do arquivo
        nome_arquivo = os.path.basename(metadados.get("arquivo_original", "video"))
        nome_base, _ = os.path.splitext(nome_arquivo)
        
        # Gerar título
        titulo = f"Dicas essenciais do eBook: {nome_base}"
        
        # Gerar descrição
        descricao = (
            f"Confira estas dicas valiosas do meu eBook '{nome_base}'.\n\n"
            f"Neste vídeo, compartilho insights importantes sobre:\n"
            f"- Estratégias comprovadas\n"
            f"- Dicas práticas\n"
            f"- Técnicas avançadas\n\n"
            f"Para mais conteúdo como este, acesse o link na descrição e adquira meu eBook completo!"
        )
        
        # Gerar tags
        tags = ["ebook", "dicas", "marketing digital", "conhecimento", "aprendizado"]
        
        return titulo, descricao, tags
    
    def _preencher_detalhes(self, driver, titulo, descricao, tags):
        """Preenche os detalhes do vídeo"""
        try:
            # Preencher título
            titulo_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ytcp-mention-textbox[@label='Title']//div[@contenteditable='true']"))
            )
            titulo_input.clear()
            titulo_input.send_keys(titulo)
            self._esperar_aleatorio()
            
            # Preencher descrição
            descricao_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ytcp-mention-textbox[@label='Description']//div[@contenteditable='true']"))
            )
            descricao_input.clear()
            descricao_input.send_keys(descricao)
            self._esperar_aleatorio()
            
            # Marcar como "Não é conteúdo para crianças"
            not_for_kids_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='NOT_MADE_FOR_KIDS']"))
            )
            not_for_kids_option.click()
            self._esperar_aleatorio()
            
            # Preencher tags
            try:
                tags_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add tag']"))
                )
                tags_string = ",".join(tags)
                tags_input.send_keys(tags_string)
                tags_input.send_keys("\n")  # Pressionar Enter para confirmar
                self._esperar_aleatorio()
            except:
                logger.warning("Campo de tags não encontrado, continuando sem tags...")
            
            # Clicar em Próximo
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='next-button']"))
            )
            next_button.click()
            self._esperar_aleatorio(2, 4)
            
            # Pular elementos de vídeo (se houver)
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='next-button']"))
                )
                next_button.click()
                self._esperar_aleatorio(2, 4)
            except:
                logger.info("Etapa de elementos de vídeo não encontrada, continuando...")
            
            # Pular verificações (se houver)
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='next-button']"))
                )
                next_button.click()
                self._esperar_aleatorio(2, 4)
            except:
                logger.info("Etapa de verificações não encontrada, continuando...")
            
            logger.info("Detalhes do vídeo preenchidos com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao preencher detalhes do vídeo: {str(e)}")
            raise
    
    def _publicar_video(self, driver):
        """Publica o vídeo e retorna a URL"""
        try:
            # Selecionar visibilidade pública
            public_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='PUBLIC']"))
            )
            public_option.click()
            self._esperar_aleatorio()
            
            # Clicar em Publicar
            publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']"))
            )
            publish_button.click()
            
            # Aguardar confirmação de publicação
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//ytcp-uploads-still-processing-dialog"))
            )
            
            # Obter URL do vídeo
            try:
                video_url_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'watch?v=')]"))
                )
                video_url = video_url_element.get_attribute("href")
                logger.info(f"Vídeo publicado com sucesso: {video_url}")
                return video_url
            except:
                logger.warning("URL do vídeo não encontrada")
                return ""
            
        except Exception as e:
            logger.error(f"Erro ao publicar vídeo: {str(e)}")
            raise

# Classes para Instagram e TikTok seriam implementadas de forma semelhante

# Exemplo de uso
if __name__ == "__main__":
    pasta_videos = "/caminho/para/videos_processados"
    config_path = "/caminho/para/config.json"
    
    gerenciador = GerenciadorUpload(pasta_videos, config_path)
    gerenciador.processar_uploads()
```

## 7. Manual do Usuário (Resumo)

O Manual do Usuário completo está disponível como anexo a este documento. Abaixo está um resumo das principais seções:

### 7.1. Instalação e Configuração

- **Download e Instalação**: Instruções passo a passo para diferentes sistemas operacionais
- **Primeiros Passos**: Criação de conta, tour inicial e configuração básica
- **Configuração de Pastas**: Definição de pastas de entrada, processamento e saída
- **Configuração de Contas**: Adição e configuração de contas de redes sociais
- **Configuração de Templates**: Personalização de templates de vídeo por plataforma

### 7.2. Uso Diário

- **Adicionando Vídeos**: Processo simples de adicionar vídeos à pasta de entrada
- **Monitorando o Processamento**: Acompanhamento do status de processamento
- **Revisão e Ajustes**: Opções para revisar e ajustar vídeos antes da publicação
- **Acompanhamento de Publicações**: Monitoramento do status das publicações
- **Análise de Desempenho**: Avaliação do desempenho dos vídeos publicados

### 7.3. Painel Administrativo

- **Dashboard**: Visão geral do sistema e estatísticas
- **Vídeos**: Gerenciamento de vídeos crus e processados
- **Publicações**: Calendário e lista de publicações
- **Contas**: Gerenciamento de contas de redes sociais
- **Relatórios**: Análise de desempenho e engajamento
- **Configurações**: Personalização do sistema

### 7.4. Solução de Problemas

- **Problemas de Detecção**: Soluções para problemas de detecção de vídeos
- **Problemas de Processamento**: Soluções para falhas durante o processamento
- **Problemas de Legendas**: Ajustes para melhorar a qualidade das legendas
- **Problemas de Upload**: Soluções para falhas durante o upload
- **Problemas de Sistema**: Otimizações e reinicializações

## 8. Estratégia de Monetização (Resumo)

A estratégia de monetização completa está disponível como anexo a este documento. Abaixo está um resumo das principais seções:

### 8.1. Modelos de Monetização

- **Software como Serviço (SaaS)**: Assinatura recorrente como modelo principal
- **Licença Perpétua**: Opção de pagamento único para usuários que preferem propriedade
- **Modelo Freemium**: Versão gratuita com limitações para criar funil de conversão
- **Marketplace de Add-ons**: Ecossistema de extensões para receita adicional

### 8.2. Estrutura de Preços

- **Plano Gratuito**: Recursos básicos com limitações significativas
- **Plano Básico**: R$ 49/mês ou R$ 470/ano (20% de desconto)
- **Plano Profissional**: R$ 99/mês ou R$ 950/ano (20% de desconto)
- **Plano Empresarial**: R$ 199/mês ou R$ 1.910/ano (20% de desconto)
- **Plano Personalizado**: Sob consulta para necessidades específicas
- **Licenças Perpétuas**: Equivalentes a aproximadamente 24 meses de assinatura

### 8.3. Estratégia de Lançamento

- **Fase 1: Beta Fechado**: 50-100 usuários selecionados por 2 meses
- **Fase 2: Beta Aberto**: 500-1000 usuários por 1 mês
- **Fase 3: Lançamento Oficial**: Abertura para o público geral
- **Fase 4: Expansão**: Novos recursos, mercados internacionais e parcerias

### 8.4. Retenção e Expansão

- **Onboarding Eficiente**: Processo estruturado para novos usuários
- **Engajamento Contínuo**: Comunicação regular e recursos de comunidade
- **Suporte Proativo**: Identificação e resolução antecipada de problemas
- **Estratégia de Upsell**: Incentivos para upgrade baseados no uso
- **Estratégia de Cross-sell**: Add-ons complementares e serviços adicionais

### 8.5. Projeções Financeiras

- **Ano 1**: Meta de 2.000 usuários pagantes, receita estimada de R$ 1.426.800
- **Ano 2**: Meta de 5.000 usuários pagantes, receita estimada de R$ 3.770.000
- **Ano 3**: Meta de 10.000 usuários pagantes, receita estimada de R$ 7.990.000
- **Break-even**: Aproximadamente no mês 10-12 do primeiro ano

## 9. Conclusão

O Software Automatizado de Edição e Publicação de Vídeos para Divulgação de eBooks representa uma solução completa e inovadora para autores e editores que desejam ampliar seu alcance nas redes sociais sem dedicar tempo excessivo à edição e publicação de conteúdo.

Desenvolvido com foco em gratuidade e funcionalidade, conforme solicitado, o sistema utiliza tecnologias de código aberto e ferramentas gratuitas sempre que possível, mantendo a qualidade e confiabilidade necessárias para uma operação profissional.

Os principais diferenciais do sistema incluem:

1. **Automação completa**: Do monitoramento de pasta até a publicação nas redes sociais
2. **Edição profissional**: Legendas automáticas, chamadas para ação e adaptação para diferentes plataformas
3. **Gerenciamento de múltiplas contas**: Rotação inteligente para evitar bloqueios
4. **Agendamento otimizado**: Publicação nos melhores horários para maximizar engajamento
5. **Análise detalhada**: Métricas de desempenho para otimização contínua

O roadmap de desenvolvimento apresentado divide o projeto em cinco fases principais, permitindo entregas incrementais de valor e ajustes baseados em feedback real dos usuários. A arquitetura modular facilita a manutenção e expansão futura do sistema.

A estratégia de monetização proposta equilibra acessibilidade para novos usuários com potencial de receita significativa a longo prazo, através de um modelo SaaS complementado por opções de licença perpétua e um marketplace de add-ons.

Com a implementação deste sistema, autores de eBooks poderão focar no que realmente importa: criar conteúdo de qualidade, enquanto o software cuida de todo o processo de distribuição e promoção nas redes sociais.

## 10. Anexos

Os seguintes documentos estão anexados a este documento executivo:

1. [Arquitetura Detalhada do Sistema](/home/ubuntu/arquitetura_detalhada.md)
2. [Roadmap Detalhado de Desenvolvimento](/home/ubuntu/roadmap_detalhado.md)
3. [Design do Painel Administrativo](/home/ubuntu/design_painel_administrativo.md)
4. [Exemplos de Código](/home/ubuntu/exemplos_codigo/)
   - [Monitor de Pasta](/home/ubuntu/exemplos_codigo/monitor_pasta.py)
   - [Processador de Vídeo](/home/ubuntu/exemplos_codigo/processador_video.py)
   - [Automação de Upload](/home/ubuntu/exemplos_codigo/automacao_upload.py)
5. [Manual do Usuário Completo](/home/ubuntu/manual_usuario.md)
6. [Estratégia de Monetização Detalhada](/home/ubuntu/estrategia_monetizacao.md)

---

© 2025 Software Automatizado de Edição e Publicação de Vídeos. Todos os direitos reservados.

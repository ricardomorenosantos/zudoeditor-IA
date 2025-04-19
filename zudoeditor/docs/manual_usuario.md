# Manual do Usuário - Software de Automação de Vídeos para Divulgação de eBooks

## Sumário

1. [Introdução](#1-introdução)
2. [Requisitos do Sistema](#2-requisitos-do-sistema)
3. [Instalação](#3-instalação)
4. [Primeiros Passos](#4-primeiros-passos)
5. [Configuração Inicial](#5-configuração-inicial)
6. [Uso Diário](#6-uso-diário)
7. [Painel Administrativo](#7-painel-administrativo)
8. [Gerenciamento de Contas](#8-gerenciamento-de-contas)
9. [Personalização de Vídeos](#9-personalização-de-vídeos)
10. [Agendamento de Publicações](#10-agendamento-de-publicações)
11. [Relatórios e Análises](#11-relatórios-e-análises)
12. [Solução de Problemas](#12-solução-de-problemas)
13. [Perguntas Frequentes](#13-perguntas-frequentes)
14. [Suporte Técnico](#14-suporte-técnico)

## 1. Introdução

Bem-vindo ao Manual do Usuário do Software de Automação de Vídeos para Divulgação de eBooks. Este software foi desenvolvido para simplificar o processo de edição e publicação de vídeos curtos (Reels, Shorts e TikTok) para divulgar seus eBooks em múltiplas contas e plataformas.

### 1.1. Visão Geral

O software automatiza todo o fluxo de trabalho, desde o upload de vídeos crus até a publicação nas redes sociais:

- **Upload automático** de vídeos crus de uma pasta designada
- **Edição automática** com cortes dinâmicos, legendas e chamadas para ação
- **Adaptação automática** para diferentes plataformas (Instagram, YouTube, TikTok)
- **Criação automática** de títulos, descrições e hashtags
- **Publicação automática** em múltiplas contas por plataforma
- **Agendamento inteligente** baseado em horários ótimos
- **Relatórios detalhados** sobre engajamento

### 1.2. Benefícios

- **Economia de tempo**: Automatize tarefas repetitivas de edição e publicação
- **Consistência**: Mantenha um padrão visual e de qualidade em todos os vídeos
- **Escala**: Gerencie dezenas ou centenas de contas simultaneamente
- **Otimização**: Publique nos melhores horários para maximizar o alcance
- **Insights**: Obtenha dados detalhados sobre o desempenho dos seus vídeos

## 2. Requisitos do Sistema

### 2.1. Hardware Mínimo

- **Processador**: Intel Core i5 ou equivalente (2 núcleos, 2.5GHz)
- **Memória RAM**: 4GB
- **Armazenamento**: 50GB de espaço livre em disco
- **Conexão de Internet**: 10Mbps de download, 5Mbps de upload

### 2.2. Hardware Recomendado

- **Processador**: Intel Core i7 ou equivalente (4+ núcleos, 3.0GHz+)
- **Memória RAM**: 8GB+
- **Armazenamento**: 100GB+ de espaço livre em SSD
- **Conexão de Internet**: 25Mbps+ de download, 10Mbps+ de upload

### 2.3. Software Necessário

- **Sistema Operacional**: Windows 10/11, macOS 10.15+, ou Ubuntu 20.04+
- **Navegadores**: Chrome 90+ ou Firefox 88+
- **Software Adicional**: FFmpeg (instalado automaticamente)
- **Python**: Versão 3.8 ou superior (instalado automaticamente)

## 3. Instalação

### 3.1. Download

1. Acesse o site oficial em [www.videoautomation.com](http://www.videoautomation.com)
2. Clique no botão "Download" na página inicial
3. Selecione a versão compatível com seu sistema operacional
4. Faça o download do instalador

### 3.2. Processo de Instalação

#### Windows

1. Execute o arquivo `.exe` baixado
2. Siga as instruções do assistente de instalação
3. Escolha o diretório de instalação (recomendamos manter o padrão)
4. Aguarde a conclusão da instalação
5. Clique em "Finalizar" para iniciar o software

#### macOS

1. Abra o arquivo `.dmg` baixado
2. Arraste o ícone do aplicativo para a pasta Aplicativos
3. Abra a pasta Aplicativos e clique com o botão direito no ícone do software
4. Selecione "Abrir" e confirme a execução
5. Siga as instruções na tela para concluir a instalação

#### Linux

1. Abra o terminal
2. Navegue até o diretório onde o arquivo `.deb` ou `.rpm` foi baixado
3. Execute o comando de instalação:
   - Para Ubuntu/Debian: `sudo dpkg -i nome_do_arquivo.deb`
   - Para Fedora/CentOS: `sudo rpm -i nome_do_arquivo.rpm`
4. Instale dependências, se necessário: `sudo apt-get install -f`
5. Inicie o software pelo menu de aplicativos ou pelo terminal

### 3.3. Verificação da Instalação

Após a instalação, o software realizará uma verificação automática para garantir que todos os componentes necessários estão instalados corretamente. Se algum componente estiver faltando, o software oferecerá a opção de instalá-lo automaticamente.

## 4. Primeiros Passos

### 4.1. Criação de Conta

1. Ao iniciar o software pela primeira vez, você será solicitado a criar uma conta de administrador
2. Preencha os campos obrigatórios:
   - Nome completo
   - E-mail
   - Senha (mínimo de 8 caracteres, incluindo letras, números e símbolos)
3. Clique em "Criar Conta"
4. Verifique seu e-mail para confirmar a criação da conta
5. Retorne ao software e faça login com suas credenciais

### 4.2. Tour Inicial

Após o primeiro login, um tour guiado será iniciado automaticamente para apresentar as principais funcionalidades do software:

1. **Dashboard**: Visão geral do sistema e estatísticas
2. **Vídeos**: Gerenciamento de vídeos crus e processados
3. **Publicações**: Calendário e lista de publicações
4. **Contas**: Gerenciamento de contas de redes sociais
5. **Relatórios**: Análise de desempenho e engajamento
6. **Configurações**: Personalização do sistema

Você pode pular o tour a qualquer momento clicando em "Pular" ou "Concluir Tour", e retomá-lo posteriormente através do menu "Ajuda" > "Tour Guiado".

## 5. Configuração Inicial

### 5.1. Configuração de Pastas

A primeira etapa essencial é configurar as pastas que o software utilizará:

1. Acesse o menu "Configurações" > "Pastas e Armazenamento"
2. Configure as seguintes pastas:
   - **Pasta de Entrada**: Onde você colocará os vídeos crus (ex: `C:\Videos\Entrada` ou `~/Videos/Entrada`)
   - **Pasta de Processamento**: Onde os vídeos serão processados temporariamente
   - **Pasta de Saída**: Onde os vídeos processados serão armazenados
3. Clique em "Testar Acesso" para verificar se o software tem permissões adequadas
4. Clique em "Salvar Configurações"

> **Dica**: Escolha pastas em um disco com bastante espaço livre, preferencialmente um SSD para melhor performance.

### 5.2. Configuração de Contas de Redes Sociais

Para publicar automaticamente, você precisa adicionar suas contas de redes sociais:

1. Acesse o menu "Contas" > "Adicionar Nova Conta"
2. Selecione a plataforma (YouTube, Instagram ou TikTok)
3. Preencha as informações de login:
   - Nome de usuário/e-mail
   - Senha
4. Opcionalmente, configure um proxy para esta conta
5. Clique em "Testar Conexão" para verificar se as credenciais estão corretas
6. Defina limites de uso para evitar bloqueios:
   - Publicações por dia (recomendado: 3-5)
   - Intervalo mínimo entre publicações (recomendado: 2-4 horas)
7. Clique em "Adicionar Conta"

Repita este processo para adicionar todas as suas contas em cada plataforma.

> **Importante**: Suas credenciais são armazenadas com criptografia AES-256 e nunca são compartilhadas com terceiros.

### 5.3. Configuração de Templates de Vídeo

Configure os templates padrão para cada plataforma:

1. Acesse o menu "Configurações" > "Templates de Vídeo"
2. Selecione a plataforma que deseja configurar
3. Personalize as seguintes opções:
   - **Resolução**: Padrão 9:16 (1080x1920) para todas as plataformas
   - **Duração máxima**: Ajuste conforme limites da plataforma
   - **Posição das legendas**: Geralmente na parte inferior
   - **Estilo das legendas**: Fonte, tamanho, cor, fundo
   - **Chamada para ação (CTA)**: Texto e posição
   - **Marca d'água**: Logotipo ou texto, posição e opacidade
4. Clique em "Visualizar" para ver como ficará o resultado
5. Clique em "Salvar Template"

> **Dica**: Crie templates diferentes para tipos diferentes de conteúdo (ex: dicas rápidas, demonstrações, testemunhos).

### 5.4. Configuração de Geração de Conteúdo

Configure como o software gerará títulos, descrições e hashtags:

1. Acesse o menu "Configurações" > "Geração de Conteúdo"
2. Para cada plataforma, configure:
   - **Estrutura de título**: Formato e elementos do título
   - **Estrutura de descrição**: Parágrafos, chamadas para ação
   - **Hashtags**: Conjunto de hashtags relevantes para seu nicho
   - **Variações**: Diferentes formatos para evitar repetição
3. Adicione palavras-chave relacionadas ao seu nicho
4. Configure menções e links para seus eBooks
5. Clique em "Salvar Configurações"

### 5.5. Configuração de Agendamento

Configure como o software determinará os melhores horários para publicação:

1. Acesse o menu "Configurações" > "Agendamento"
2. Para cada plataforma, configure:
   - **Horários preferenciais**: Períodos do dia para publicação
   - **Dias da semana**: Quais dias publicar
   - **Distribuição**: Como distribuir publicações entre contas
   - **Frequência**: Quantas publicações por dia/semana
3. Ative a opção "Aprendizado automático" para que o sistema otimize horários com base no desempenho
4. Clique em "Salvar Configurações"

## 6. Uso Diário

### 6.1. Adicionando Vídeos Crus

O processo de uso diário é extremamente simples:

1. Grave ou crie seus vídeos crus (sem edição)
2. Copie ou mova os arquivos para a pasta de entrada configurada
3. O software detectará automaticamente os novos arquivos
4. O processamento começará automaticamente

> **Dica**: Você pode arrastar e soltar vários arquivos de uma vez na pasta de entrada.

### 6.2. Monitorando o Processamento

Você pode acompanhar o status do processamento no painel administrativo:

1. Acesse a seção "Vídeos" > "Em Processamento"
2. Visualize o progresso de cada vídeo:
   - Detecção (verificação inicial do arquivo)
   - Processamento (edição, legendas, adaptação)
   - Agendamento (determinação dos melhores horários)
   - Publicação (upload para as plataformas)
3. Clique em um vídeo para ver detalhes específicos do processamento

### 6.3. Revisão e Ajustes (Opcional)

Embora o sistema seja totalmente automatizado, você pode revisar e ajustar os vídeos antes da publicação:

1. Acesse a seção "Vídeos" > "Processados"
2. Clique no vídeo que deseja revisar
3. Visualize a prévia do vídeo processado para cada plataforma
4. Se necessário, faça ajustes:
   - Edite o título e descrição
   - Modifique as hashtags
   - Ajuste o horário de publicação
   - Selecione contas específicas para publicação
5. Clique em "Salvar Ajustes"

### 6.4. Acompanhamento de Publicações

Acompanhe o status das publicações agendadas e realizadas:

1. Acesse a seção "Publicações"
2. Visualize o calendário de publicações agendadas
3. Clique em uma publicação para ver detalhes:
   - Plataforma e conta
   - Horário programado
   - Status (agendada, em andamento, concluída, falha)
   - Métricas de engajamento (após a publicação)
4. Filtre por período, plataforma ou status

### 6.5. Análise de Desempenho

Analise o desempenho dos seus vídeos para otimizar sua estratégia:

1. Acesse a seção "Relatórios"
2. Selecione o período de análise
3. Visualize métricas por:
   - Plataforma
   - Tipo de conteúdo
   - Horário de publicação
   - Conta
4. Identifique padrões e tendências
5. Exporte relatórios em formato PDF ou CSV

## 7. Painel Administrativo

### 7.1. Dashboard

O Dashboard oferece uma visão geral do sistema:

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
  - Visão mensal/semanal/diária
  - Codificação por cores por plataforma
  - Indicadores de status

- **Atividade Recente**:
  - Últimas ações do sistema
  - Alertas e notificações
  - Status de processamento

### 7.2. Seção de Vídeos

A seção de Vídeos permite gerenciar todos os seus vídeos:

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

### 7.3. Seção de Publicações

A seção de Publicações oferece duas visualizações principais:

- **Calendário**:
  - Visão mensal, semanal ou diária
  - Codificação por cores por plataforma
  - Drag-and-drop para reagendamento

- **Lista**:
  - Todas as publicações em formato de lista
  - Filtros por status, plataforma, período
  - Opções de edição e cancelamento

Para cada publicação, você pode:
- Visualizar detalhes completos
- Editar título, descrição e hashtags
- Reagendar para outro horário
- Cancelar publicações agendadas
- Ver métricas após a publicação

### 7.4. Seção de Contas

A seção de Contas permite gerenciar todas as suas contas de redes sociais:

- **Visão Geral**:
  - Lista de todas as contas por plataforma
  - Status de cada conta (ativa, bloqueada, em uso)
  - Métricas de uso

- **Detalhes da Conta**:
  - Informações completas
  - Histórico de publicações
  - Estatísticas de desempenho
  - Opções de teste de conexão

- **Gerenciamento**:
  - Adicionar novas contas
  - Editar contas existentes
  - Configurar limites de uso
  - Definir proxies específicos

### 7.5. Seção de Relatórios

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

- **Relatórios Personalizados**:
  - Criação de relatórios específicos
  - Exportação em múltiplos formatos
  - Agendamento de relatórios recorrentes

### 7.6. Seção de Configurações

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

- **Agendamento**:
  - Configurações de horários
  - Estratégias de distribuição
  - Aprendizado automático

- **Segurança**:
  - Criptografia de credenciais
  - Configuração de proxies
  - Logs de atividade

## 8. Gerenciamento de Contas

### 8.1. Adicionando Novas Contas

Para expandir seu alcance, adicione múltiplas contas por plataforma:

1. Acesse "Contas" > "Adicionar Nova Conta"
2. Selecione a plataforma
3. Preencha as credenciais
4. Configure limites de uso:
   - Máximo de publicações por dia
   - Intervalo mínimo entre publicações
   - Horários preferenciais
5. Configure opções avançadas:
   - Proxy dedicado (recomendado para múltiplas contas)
   - User agent personalizado
   - Comportamento de login
6. Clique em "Adicionar Conta"

### 8.2. Rotação de Contas

O sistema gerencia automaticamente a rotação de contas para evitar bloqueios:

- **Distribuição Equilibrada**: Publicações distribuídas entre todas as contas
- **Respeito aos Limites**: Cada conta respeita os limites configurados
- **Períodos de Descanso**: Contas muito utilizadas recebem períodos de descanso
- **Detecção de Problemas**: Contas com sinais de restrição são temporariamente pausadas

Para configurar a estratégia de rotação:
1. Acesse "Configurações" > "Gerenciamento de Contas"
2. Selecione "Estratégia de Rotação"
3. Escolha entre:
   - Equilibrada (padrão)
   - Sequencial
   - Prioridade (contas principais usadas mais frequentemente)
   - Aleatória
4. Configure parâmet
(Content truncated due to size limit. Use line ranges to read in chunks)
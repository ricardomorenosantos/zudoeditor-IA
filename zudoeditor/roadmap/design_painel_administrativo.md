# Design Detalhado do Painel Administrativo

## 1. Visão Geral da Interface

O painel administrativo do software de automação de vídeos será desenvolvido com foco em usabilidade, clareza visual e eficiência operacional. A interface seguirá os princípios de design responsivo, garantindo uma experiência consistente em dispositivos desktop e móveis.

### 1.1. Princípios de Design

- **Simplicidade:** Interface limpa e intuitiva, sem elementos desnecessários
- **Hierarquia visual:** Informações organizadas por importância e frequência de uso
- **Consistência:** Padrões visuais e interativos uniformes em toda a aplicação
- **Feedback imediato:** Respostas visuais claras para todas as ações do usuário
- **Acessibilidade:** Conformidade com diretrizes WCAG 2.1 nível AA

### 1.2. Paleta de Cores

- **Cor primária:** #3498db (Azul)
- **Cor secundária:** #2ecc71 (Verde)
- **Cor de alerta:** #e74c3c (Vermelho)
- **Cor de aviso:** #f39c12 (Laranja)
- **Cor de fundo principal:** #f5f7fa (Cinza claro)
- **Cor de fundo secundária:** #ffffff (Branco)
- **Texto principal:** #2c3e50 (Azul escuro)
- **Texto secundário:** #7f8c8d (Cinza)

### 1.3. Tipografia

- **Fonte principal:** Roboto (sans-serif)
- **Fonte alternativa:** Open Sans (sans-serif)
- **Tamanhos:**
  - Títulos principais: 24px
  - Subtítulos: 18px
  - Texto normal: 14px
  - Texto pequeno: 12px

## 2. Estrutura da Interface

### 2.1. Layout Geral

```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               |                                               |
|               |                                               |
|    MENU       |                                               |
|    LATERAL    |             ÁREA DE CONTEÚDO                  |
|               |                                               |
|               |                                               |
|               |                                               |
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

### 2.2. Componentes Principais

#### Cabeçalho
- Logo do sistema (esquerda)
- Barra de pesquisa (centro)
- Notificações (direita)
- Menu de usuário (direita)
- Indicador de status do sistema (direita)

#### Menu Lateral
- Foto/avatar do usuário
- Links de navegação principais
- Indicadores de status
- Botão de recolher/expandir
- Acesso rápido às configurações

#### Área de Conteúdo
- Título da seção atual
- Breadcrumbs de navegação
- Filtros e controles específicos da seção
- Conteúdo principal dinâmico
- Paginação (quando aplicável)

#### Rodapé
- Informações de versão
- Links para documentação e suporte
- Status de conexão com serviços
- Copyright e informações legais

## 3. Telas Principais

### 3.1. Dashboard (Página Inicial)

#### Layout
```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               | TÍTULO: Dashboard                             |
|               +-----------------------------------------------+
|               | +----------+ +----------+ +----------+        |
|               | | ESTATÍST.| | ESTATÍST.| | ESTATÍST.|        |
|    MENU       | | RÁPIDA 1 | | RÁPIDA 2 | | RÁPIDA 3 |        |
|    LATERAL    | +----------+ +----------+ +----------+        |
|               |                                               |
|               | +-------------------+ +-------------------+   |
|               | |                   | |                   |   |
|               | |  GRÁFICO DE       | |  CALENDÁRIO DE    |   |
|               | |  DESEMPENHO       | |  PUBLICAÇÕES      |   |
|               | |                   | |                   |   |
|               | +-------------------+ +-------------------+   |
|               |                                               |
|               | +-----------------------------------------------+
|               | |                                             | |
|               | |  ATIVIDADE RECENTE                          | |
|               | |                                             | |
|               | +-----------------------------------------------+
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

#### Elementos
1. **Widgets de Estatísticas Rápidas:**
   - Total de vídeos processados (com indicador de tendência)
   - Publicações agendadas para hoje
   - Taxa média de engajamento
   - Status de saúde das contas

2. **Gráfico de Desempenho:**
   - Visualizações/engajamento por plataforma
   - Comparativo dos últimos 30 dias
   - Opções de filtro por período
   - Exportação de dados

3. **Calendário de Publicações:**
   - Visão mensal/semanal/diária
   - Indicadores visuais por plataforma
   - Preview rápido ao passar o mouse
   - Acesso rápido para edição

4. **Atividade Recente:**
   - Lista de últimas ações do sistema
   - Status de processamentos em andamento
   - Alertas e notificações importantes
   - Links rápidos para itens relacionados

### 3.2. Vídeos

#### Layout
```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               | TÍTULO: Vídeos                                |
|               +-----------------------------------------------+
|               | +---------+ +----------+ +----------------+   |
|               | | FILTROS | | ORDENAR▼ | | + NOVO VÍDEO   |   |
|    MENU       | +---------+ +----------+ +----------------+   |
|    LATERAL    |                                               |
|               | +-----------------------------------------------+
|               | | □ | MINIATURA | NOME | STATUS | PLATAFORMAS | |
|               | +-----------------------------------------------+
|               | | □ |[Thumbnail]| Video1| ✓ Pronto| YT, IG, TK | |
|               | +-----------------------------------------------+
|               | | □ |[Thumbnail]| Video2|⟳ Process| YT, IG     | |
|               | +-----------------------------------------------+
|               | | □ |[Thumbnail]| Video3| ✓ Pronto| TK         | |
|               | +-----------------------------------------------+
|               | | □ |[Thumbnail]| Video4| ⚠ Erro  | -          | |
|               | +-----------------------------------------------+
|               |                                               |
|               | +----------+  Página 1 de 5  +------------+  |
|               | | < ANTER. |                 | PRÓXIMA >  |  |
|               | +----------+                 +------------+  |
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

#### Elementos
1. **Barra de Ferramentas:**
   - Filtros (status, data, plataforma)
   - Ordenação (data, nome, status)
   - Botão de upload manual
   - Ações em lote (para seleção múltipla)

2. **Lista de Vídeos:**
   - Checkbox para seleção múltipla
   - Miniatura do vídeo
   - Nome do arquivo/título
   - Status com ícone visual (pronto, processando, erro)
   - Plataformas de destino
   - Data de upload/processamento
   - Menu de ações rápidas

3. **Detalhes Rápidos:**
   - Expansão de linha para mostrar detalhes adicionais
   - Preview do vídeo em miniatura
   - Informações técnicas (duração, resolução)
   - Log resumido de processamento
   - Links para edição/visualização

4. **Paginação:**
   - Navegação entre páginas
   - Seletor de itens por página
   - Indicador de total de itens

### 3.3. Publicações

#### Layout
```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               | TÍTULO: Publicações                           |
|               +-----------------------------------------------+
|               | +----------+ +----------+ +---------------+   |
|               | | VISUALIZ.▼| | FILTROS | | + AGENDAR     |   |
|    MENU       | +----------+ +----------+ +---------------+   |
|    LATERAL    |                                               |
|               | +-----------------------------------------------+
|               | |                                             | |
|               | |                                             | |
|               | |                                             | |
|               | |                                             | |
|               | |           CALENDÁRIO / LISTA                | |
|               | |                                             | |
|               | |                                             | |
|               | |                                             | |
|               | |                                             | |
|               | +-----------------------------------------------+
|               |                                               |
|               | +-----------------------------------------------+
|               | |                                             | |
|               | |           DETALHES DA PUBLICAÇÃO            | |
|               | |                                             | |
|               | +-----------------------------------------------+
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

#### Elementos
1. **Controles de Visualização:**
   - Alternância entre visualização de calendário e lista
   - Filtros (plataforma, status, conta, período)
   - Botão para agendar nova publicação
   - Opções de exportação

2. **Visualização de Calendário:**
   - Modos de visualização (mês, semana, dia)
   - Codificação por cores para plataformas
   - Indicadores visuais de status
   - Drag-and-drop para reagendamento
   - Zoom para detalhes

3. **Visualização em Lista:**
   - Ordenação por data/hora
   - Agrupamento por dia/plataforma
   - Status com indicadores visuais
   - Ações rápidas (editar, cancelar, reagendar)
   - Métricas resumidas

4. **Painel de Detalhes:**
   - Preview do conteúdo
   - Informações completas da publicação
   - Métricas de engajamento (se publicado)
   - Histórico de alterações
   - Opções de edição e gerenciamento

### 3.4. Contas

#### Layout
```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               | TÍTULO: Contas                                |
|               +-----------------------------------------------+
|               | +----------+ +----------+ +---------------+   |
|               | | PLATAFOR.▼| | STATUS▼ | | + NOVA CONTA  |   |
|    MENU       | +----------+ +----------+ +---------------+   |
|    LATERAL    |                                               |
|               | +-----------------------------------------------+
|               | | PLATAFORMA | CONTA      | STATUS  | AÇÕES    | |
|               | +-----------------------------------------------+
|               | | Instagram  | @conta1    | ● Ativa | ⋮        | |
|               | +-----------------------------------------------+
|               | | Instagram  | @conta2    | ● Ativa | ⋮        | |
|               | +-----------------------------------------------+
|               | | YouTube    | Canal1     | ● Ativa | ⋮        | |
|               | +-----------------------------------------------+
|               | | TikTok     | @tiktok1   | ⚠ Alerta| ⋮        | |
|               | +-----------------------------------------------+
|               | | YouTube    | Canal2     | ✕ Bloq. | ⋮        | |
|               | +-----------------------------------------------+
|               |                                               |
|               | +-----------------------------------------------+
|               | |                                             | |
|               | |           DETALHES DA CONTA                 | |
|               | |                                             | |
|               | +-----------------------------------------------+
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

#### Elementos
1. **Filtros e Controles:**
   - Filtro por plataforma
   - Filtro por status
   - Botão para adicionar nova conta
   - Opções de gerenciamento em lote

2. **Lista de Contas:**
   - Ícone da plataforma
   - Nome da conta/usuário
   - Status com indicador visual (ativa, alerta, bloqueada)
   - Data da última publicação
   - Métricas resumidas
   - Menu de ações

3. **Painel de Detalhes:**
   - Informações completas da conta
   - Estatísticas de uso
   - Histórico de publicações
   - Gráfico de saúde da conta
   - Opções de teste de conexão
   - Configurações específicas

4. **Formulário de Nova Conta:**
   - Seleção de plataforma
   - Campos de credenciais
   - Opções de proxy
   - Configurações de limites
   - Teste de conexão antes de salvar

### 3.5. Relatórios

#### Layout
```
+---------------------------------------------------------------+
|                          CABEÇALHO                            |
+---------------+-----------------------------------------------+
|               | TÍTULO: Relatórios                            |
|               +-----------------------------------------------+
|               | +----------+ +----------+ +---------------+   |
|               | | PERÍODO▼ | | MÉTRICAS▼| | EXPORTAR      |   |
|    MENU       | +----------+ +----------+ +---------------+   |
|    LATERAL    |                                               |
|               | +-------------------+ +-------------------+   |
|               | |                   | |                   |   |
|               | |  GRÁFICO DE       | |  GRÁFICO DE       |   |
|               | |  VISUALIZAÇÕES    | |  ENGAJAMENTO      |   |
|               | |                   | |                   |   |
|               | +-------------------+ +-------------------+   |
|               |                                               |
|               | +-------------------+ +-------------------+   |
|               | |                   | |                   |   |
|               | |  COMPARATIVO      | |  MELHORES         |   |
|               | |  POR PLATAFORMA   | |  HORÁRIOS         |   |
|               | |                   | |                   |   |
|               | +-------------------+ +-------------------+   |
|               |                                               |
|               | +-----------------------------------------------+
|               | |                                             | |
|               | |           TABELA DE DADOS DETALHADOS        | |
|               | |                                             | |
|               | +-----------------------------------------------+
+---------------+-----------------------------------------------+
|                           RODAPÉ                              |
+---------------------------------------------------------------+
```

#### Elementos
1. **Controles de Relatório:**
   - 
(Content truncated due to size limit. Use line ranges to read in chunks)
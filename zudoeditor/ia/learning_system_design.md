# Design do Sistema de Aprendizado para IA de Edição de Vídeos

## Visão Geral

Este documento detalha o design do sistema de aprendizado que permitirá que a IA de edição de vídeos evolua e se adapte com o uso, aprendendo com as preferências do usuário e melhorando continuamente a qualidade das edições automáticas.

O sistema de aprendizado é projetado para ser:
- **Leve**: Capaz de rodar em computadores comuns sem hardware especializado
- **Local**: Todo o processamento ocorre no computador do usuário, sem necessidade de conexão com a internet
- **Adaptativo**: Evolui com o uso, aprendendo com as preferências específicas do usuário
- **Transparente**: Permite que o usuário entenda e controle o processo de aprendizado

## Arquitetura do Sistema de Aprendizado

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Coleta de      │────▶│  Processamento  │────▶│  Modelo de      │
│  Feedback       │     │  de Dados       │     │  Preferências   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        │                                               ▼
┌─────────────────┐                           ┌─────────────────┐
│                 │                           │                 │
│  Interface de   │◀──────────────────────────│  Aplicação de   │
│  Usuário        │                           │  Preferências   │
│                 │                           │                 │
└─────────────────┘                           └─────────────────┘
```

### 1. Módulo de Coleta de Feedback

Este módulo é responsável por capturar informações sobre as preferências do usuário através de diferentes fontes:

#### 1.1 Feedback Explícito

```python
class ExplicitFeedbackCollector:
    def __init__(self, feedback_db_path="user_feedback.db"):
        """
        Inicializa o coletor de feedback explícito.
        
        Args:
            feedback_db_path (str): Caminho para o banco de dados de feedback
        """
        self.feedback_db_path = feedback_db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite para armazenar feedback."""
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        # Criar tabela de feedback se não existir
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS explicit_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            timestamp REAL,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_rating(self, video_id, rating, comment=None):
        """
        Registra uma avaliação explícita do usuário.
        
        Args:
            video_id (str): Identificador do vídeo
            rating (int): Avaliação (1-5)
            comment (str, opcional): Comentário do usuário
            
        Returns:
            bool: True se o registro foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO explicit_feedback (video_id, timestamp, rating, comment) VALUES (?, NULL, ?, ?)",
                (video_id, rating, comment)
            )
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao registrar feedback: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
    
    def record_timestamp_feedback(self, video_id, timestamp, rating, comment=None):
        """
        Registra feedback para um momento específico do vídeo.
        
        Args:
            video_id (str): Identificador do vídeo
            timestamp (float): Momento específico no vídeo (segundos)
            rating (int): Avaliação (1-5)
            comment (str, opcional): Comentário do usuário
            
        Returns:
            bool: True se o registro foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO explicit_feedback (video_id, timestamp, rating, comment) VALUES (?, ?, ?, ?)",
                (video_id, timestamp, rating, comment)
            )
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao registrar feedback de timestamp: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
```

#### 1.2 Feedback Implícito

```python
class ImplicitFeedbackCollector:
    def __init__(self, feedback_db_path="user_feedback.db"):
        """
        Inicializa o coletor de feedback implícito.
        
        Args:
            feedback_db_path (str): Caminho para o banco de dados de feedback
        """
        self.feedback_db_path = feedback_db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite para armazenar feedback implícito."""
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        # Criar tabela de edições manuais
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS manual_edits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            original_cut_point REAL,
            new_cut_point REAL,
            edit_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Criar tabela de estatísticas de uso
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            action TEXT,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_manual_edit(self, video_id, original_cut_point, new_cut_point, edit_type):
        """
        Registra uma edição manual feita pelo usuário após a edição automática.
        
        Args:
            video_id (str): Identificador do vídeo
            original_cut_point (float): Ponto de corte original (segundos)
            new_cut_point (float): Novo ponto de corte (segundos)
            edit_type (str): Tipo de edição ('add', 'remove', 'move')
            
        Returns:
            bool: True se o registro foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO manual_edits (video_id, original_cut_point, new_cut_point, edit_type) VALUES (?, ?, ?, ?)",
                (video_id, original_cut_point, new_cut_point, edit_type)
            )
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao registrar edição manual: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
    
    def record_usage_stat(self, video_id, action, value):
        """
        Registra estatísticas de uso para análise de comportamento.
        
        Args:
            video_id (str): Identificador do vídeo
            action (str): Ação realizada
            value (str): Valor associado à ação
            
        Returns:
            bool: True se o registro foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO usage_stats (video_id, action, value) VALUES (?, ?, ?)",
                (video_id, action, value)
            )
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao registrar estatística de uso: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
```

#### 1.3 Análise de Resultados Publicados

```python
class PublishedResultsAnalyzer:
    def __init__(self, results_db_path="published_results.db"):
        """
        Inicializa o analisador de resultados publicados.
        
        Args:
            results_db_path (str): Caminho para o banco de dados de resultados
        """
        self.results_db_path = results_db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite para armazenar resultados de publicações."""
        import sqlite3
        
        conn = sqlite3.connect(self.results_db_path)
        cursor = conn.cursor()
        
        # Criar tabela de métricas de engajamento
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS engagement_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            platform TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            watch_time REAL,
            retention_rate REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_engagement_metrics(self, video_id, platform, metrics):
        """
        Registra métricas de engajamento para um vídeo publicado.
        
        Args:
            video_id (str): Identificador do vídeo
            platform (str): Plataforma onde o vídeo foi publicado
            metrics (dict): Métricas de engajamento
            
        Returns:
            bool: True se o registro foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.results_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO engagement_metrics 
                (video_id, platform, views, likes, comments, shares, watch_time, retention_rate) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    video_id, 
                    platform, 
                    metrics.get('views', 0),
                    metrics.get('likes', 0),
                    metrics.get('comments', 0),
                    metrics.get('shares', 0),
                    metrics.get('watch_time', 0.0),
                    metrics.get('retention_rate', 0.0)
                )
            )
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao registrar métricas de engajamento: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
    
    def analyze_performance(self, video_id=None, platform=None, time_period=None):
        """
        Analisa o desempenho dos vídeos publicados.
        
        Args:
            video_id (str, opcional): Filtrar por ID do vídeo
            platform (str, opcional): Filtrar por plataforma
            time_period (str, opcional): Período de tempo para análise
            
        Returns:
            dict: Análise de desempenho
        """
        import sqlite3
        import datetime
        
        conn = sqlite3.connect(self.results_db_path)
        cursor = conn.cursor()
        
        # Construir consulta SQL com filtros opcionais
        query = "SELECT * FROM engagement_metrics WHERE 1=1"
        params = []
        
        if video_id:
            query += " AND video_id = ?"
            params.append(video_id)
        
        if platform:
            query += " AND platform = ?"
            params.append(platform)
        
        if time_period:
            now = datetime.datetime.now()
            if time_period == 'day':
                cutoff = now - datetime.timedelta(days=1)
            elif time_period == 'week':
                cutoff = now - datetime.timedelta(weeks=1)
            elif time_period == 'month':
                cutoff = now - datetime.timedelta(days=30)
            else:
                cutoff = now - datetime.timedelta(days=365)
            
            query += " AND created_at >= ?"
            params.append(cutoff.strftime('%Y-%m-%d %H:%M:%S'))
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Processar resultados
        if not results:
            return {"status": "No data found"}
        
        # Extrair colunas
        columns = [desc[0] for desc in cursor.description]
        
        # Converter para lista de dicionários
        metrics_list = []
        for row in results:
            metrics_dict = {}
            for i, col in enumerate(columns):
                metrics_dict[col] = row[i]
            metrics_list.append(metrics_dict)
        
        # Calcular estatísticas agregadas
        aggregated = {
            "total_videos": len(metrics_list),
            "total_views": sum(m.get('views', 0) for m in metrics_list),
            "avg_likes": sum(m.get('likes', 0) for m in metrics_list) / len(metrics_list),
            "avg_comments": sum(m.get('comments', 0) for m in metrics_list) / len(metrics_list),
            "avg_shares": sum(m.get('shares', 0) for m in metrics_list) / len(metrics_list),
            "avg_watch_time": sum(m.get('watch_time', 0) for m in metrics_list) / len(metrics_list),
            "avg_retention_rate": sum(m.get('retention_rate', 0) for m in metrics_list) / len(metrics_list),
        }
        
        conn.close()
        
        return {
            "status": "success",
            "metrics": metrics_list,
            "aggregated": aggregated
        }
```

### 2. Módulo de Processamento de Dados

Este módulo transforma os dados de feedback em informações úteis para o modelo de aprendizado:

#### 2.1 Extração de Características

```python
class FeatureExtractor:
    def __init__(self, video_features_db_path="video_features.db"):
        """
        Inicializa o extrator de características.
        
        Args:
            video_features_db_path (str): Caminho para o banco de dados de características
        """
        self.video_features_db_path = video_features_db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite para armazenar características de vídeos."""
        import sqlite3
        
        conn = sqlite3.connect(self.video_features_db_path)
        cursor = conn.cursor()
        
        # Criar tabela de características de vídeo
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            feature_name TEXT,
            feature_value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_video_features(self, video_path):
        """
        Extrai características de um vídeo.
        
        Args:
            video_path (str): Caminho para o arquivo de vídeo
            
        Returns:
            dict: Características extraídas
        """
        import os
        import numpy as np
        from moviepy.editor import VideoFileClip
        import librosa
        
        video_id = os.path.basename(video_path)
        
        # Carregar vídeo
        video = VideoFileClip(video_path)
        
        # Extrair áudio para análise
        audio = video.audio
        audio_array = audio.to_soundarray()
        
        # Características básicas do vídeo
        features = {
            "duration": video.duration,
            "fps": video.fps,
            "width": video.w,
            "height": video.h,
            "aspect_ratio": video.w / video.h,
        }
        
        # Características de áudio
        if audio is not None:
            # Converter para mono se estéreo
            if len(audio_array.shape) > 1 and audio_array.shape[1] > 1:
                audio_mono = np.mean(audio_array, axis=1)
            else:
                audio_mono = audio_array.flatten()
            
            # Calcular características de áudio
            features.update({
                "audio_rms": np.sqrt(np.mean(audio_mono**2)),
                "audio_zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(audio_mono)),
                "audio_spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=audio_mono, sr=audio.fps)[0]),
                "audio_spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=audio_mono, sr=audio.fps)[0]),
                "audio_spectral_rolloff": np.mean(librosa.feature.spectral_rolloff(y=audio_mono, sr=audio.fps)[0]),
            })
        
        # Salvar características no banco de dados
        self._save_features(video_id, features)
        
        return features
    
    def _save_features(self, video_id, features):
        """
        Salva características extraídas no banco de dados.
        
        Args:
            video_id (str): Identificador do vídeo
            features (dict): Características extraídas
            
        Returns:
            bool: True se o salvamento foi bem-sucedido
        """
        import sqlite3
        
        conn = sqlite3.connect(self.video_features_db_path)
        cursor = conn.cursor()
        
        try:
            # Inserir cada característica como uma linha
            for feature_name, feature_value in features.items():
                cursor.execute(
                    "INSERT INTO video_features (video_id, feature_name, feature_value) VALUES (?, ?, ?)",
                    (video_id, feature_name, float(feature_value))
                )
            
            conn.commit()
            success = True
        except Exception as e:
            print(f"Erro ao salvar características: {e}")
            conn.rollback()
            success = False
        finally:
            conn.close()
        
        return success
    
    def get_video_features(self, video_id):
        """
        Recupera características de um vídeo do banco de dados.
        
        Args:
            video_id (str): Identificador do vídeo
            
        Returns:
            dict: Características do vídeo
        """
        import sqlite3
        
        conn = sqlite3.connect(self.video_features_db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT feature_name, feature_value FROM video_features WHERE video_id = ?",
            (video_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return {}
        
        # Converter para dicionário
        features = {}
        for feature_name, feature_value in results:
            features[feature_name] = feature_value
        
        return features
```

#### 2.2 Análise de Padrões de Edição

```python
class EditingPatternAnalyzer:
    def __init__(self, feedback_db_path="user_feedback.db"):
        """
        Inicializa o analisador de padrões de edição.
        
        Args:
            feedback_db_path (str): Caminho para o banco de dados de feedback
        """
        self.feedback_db_path = feedback_db_path
    
    def analyze_cut_patterns(self):
        """
        Analisa padrões nos pontos de corte preferidos pelo usuário.
        
        Returns:
            dict: Padrões identificados
        """
        import sqlite3
        import numpy as np
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        # Obter todas as edições manuais
        cursor.execute("SELECT video_id, original_cut_point, new_cut_point, edit_type FROM manual_edits")
        edits = cursor.fetchall()
        
        if not edits:
            conn.close()
            return {"status": "No data found"}
        
        # Analisar padrões
        patterns = {
            "move_distances": [],
            "removed_cuts": [],
            "added_cuts": [],
            "edit_types_count": {"add": 0, "remove": 0, "move": 0}
        }
        
        for video_id, original, new, edit_type in edits:
            if edit_type == "move":
                patterns["move_distances"].append(new - original)
            elif edit_type == "remove":
                patterns["removed_cuts"].append(original)
            elif edit_type == "add":
                patterns["added_cuts"].append(new)
            
            patterns["edit_types_count"][edit_type] += 1
        
        # Calcular estatísticas
        if patterns["move_distances"]:
            patterns["avg_move_distance"] = np.mean(patterns["move_distances"])
            patterns["std_move_distance"] = np.std(patterns["move_distances"])
        
        # Verificar se há preferência por mover cortes para frente ou para trás
        if patterns["move_distances"]:
            forward_moves = sum(1 for d in patterns["move_distances"] if d > 0)
            backward_moves = sum(1 for d in patterns["move_distances"] if d < 0)
            total_moves = len(patterns["move_distances"])
            
            patterns["forward_move_ratio"] = forward_moves / total_moves if total_moves > 0 else 0
            patterns["backward_move_ratio"] = backward_moves / total_moves if total_moves > 0 else 0
        
        conn.close()
        
        return {
            "status": "success",
            "patterns": patterns
        }
    
    def analyze_edit_preferences_by_content(self):
        """
        Analisa preferências de edição com base no tipo de conteúdo.
        
        Returns:
            dict: Preferências identificadas por tipo de conteúdo
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_db_path)
        cursor = conn.cursor()
        
        # Esta análise requer junção com características de vídeo
        # Aqui assumimos que temos uma tabela de características de vídeo
        # e uma forma de categorizar vídeos
        
        # Exemplo simplificado:
        cursor.execute("""
        SELECT 
            m.edit_type,
            COUNT(*) as edit_count
        FROM 
            manual_edits m
        GROUP BY 
            m.edit_type
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return {"status": "No data found"}
        
        preferences = {}
        for edit_type, count in results:
            preferences[edit_type] = count
        
        return {
            "status": "success",
            "preferences": preferences
        }
```

#### 2.3 Processador de Feedback Integrado

```python
class FeedbackProcessor:
    def __init__(self, feedback_db_path="user_feedback.db", results_db_path="published_results.db"):
        """
        Inicializa o processador de feedback integrado.
        
        Args:
            feedback_db_path (str): Caminho para o banco de dados de feedback
            results_db_path (str): Caminho para o banco de dados de resultados
        """
        self.explicit_collector = ExplicitFeedbackCollector(feedback_db_path)
        self.implicit_collector = ImplicitFeedbackCollector(feedback_db_path)
        self.results_analyzer = PublishedResultsAnalyzer(results_db_path)
        self.pattern_analyzer = EditingPatternAnalyzer(feedback_db_path)
    
    def process_all_feedback(self):
        """
        Processa todos os tipos de feedback para gerar insights.
        
        Returns:
            dict: Insights gerados a partir do feedback
        """
        # Analisar padrões de edição
        cut_patterns = self.pattern_analyzer.analyze_cut_patterns()
        
        # Analisar preferências por tipo de conteúdo
        content_preferences = self.pattern_analyzer.analyze_edit_preferences_by_content()
        
        # Analisar desempenho de vídeos publicados
        performance = self.results_analyzer.analyze_performance()
        
        # Combinar insights
        insights = {
            "cut_patterns": cut_patterns.get("patterns", {}),
            "content_preferences": content_preferences.get("preferences", {}),
            "performance": performance.get("aggregated", {})
        }
        
        return insights
    
    def generate_learning_data(self):
        """
        Gera dados estruturados para alimentar o modelo de aprendizado.
        
        Returns:
            dict: Dados de aprendizado
        """
        import sqlite3
        import json
        
        conn = sqlite3.connect(self.explicit_collector.feedback_db_path)
        cursor = conn.cursor()
        
        # Obter feedback explícito
        cursor.execute("SELECT video_id, timestamp, rating FROM explicit_feedback")
        explicit_data = cursor.fetchall()
        
        # Obter edições manuais
        cursor.execute("SELECT video_id, original_cut_point, new_cut_point, edit_type FROM manual_edits")
        manual_edits = cursor.fetchall()
        
        conn.close()
        
        # Estruturar dados para aprendizado
        learning_data = {
            "explicit_feedback": [
                {"video_id": vid, "timestamp": ts, "rating": r}
                for vid, ts, r in explicit_data
            ],
            "manual_edits": [
                {"video_id": vid, "original": orig, "new": new, "type": t}
                for vid, orig, new, t in manual_edits
            ],
            "insights": self.process_all_feedback()
        }
        
        # Salvar dados para uso pelo modelo
        with open("learning_data.json", "w") as f:
            json.dump(learning_data, f)
        
        return learning_data
```

### 3. Módulo de Modelo de Preferências

Este módulo implementa o modelo de aprendizado que captura as preferências do usuário:

#### 3.1 Modelo Base de Preferências

```python
class BasePreferenceModel:
    def __init__(self, model_path="preference_model.pkl"):
        """
        Inicializa o modelo base de preferências.
        
        Args:
            model_path (str): Caminho para salvar/carregar o modelo
        """
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """
        Carrega o modelo de preferências do disco, ou cria um novo se não existir.
        
        Returns:
            bool: True se o modelo foi carregado com sucesso
        """
        import os
        import pickle
        
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                return True
            except Exception as e:
                print(f"Erro ao carregar modelo: {e}")
                self.initialize_model()
                return False
        else:
            self.initialize_model()
            return False
    
    def initialize_model(self):
        """
        Inicializa um novo modelo de preferências com valores padrão.
        """
        self.model = {
            "cut_preferences": {
                "min_segment_duration": 2.0,  # Duração mínima de um segmento em segundos
                "prefer_sentence_boundaries": 0.8,  # Peso para cortes em limites de sentenças
                "prefer_silence": 0.6,  # Peso para cortes em silêncios
                "avoid_mid_sentence": 0.9,  # Peso para evitar cortes no meio de frases
                "prefer_forward_cuts": 0.5,  # Preferência por mover cortes para frente (0.5 = neutro)
            },
            "style_preferences": {
                "pace": 0.5,  # 0 = lento, 1 = rápido
                "cut_frequency": 0.5,  # 0 = poucos cortes, 1 = muitos cortes
                "transition_style": "cut",  # Estilo de transição padrão
                "audio_balance": 0.5,  # 0 = priorizar clareza, 1 = priorizar ritmo
            },
            "content_preferences": {
                "keep_intro": 0.7,  # Probabilidade de manter introduções
                "keep_conclusion": 0.8,  # Probabilidade de manter conclusões
                "keep_examples": 0.6,  # Probabilidade de manter exemplos
                "remove_silence": 0.7,  # Probabilidade de remover silêncios
                "remove_filler_words": 0.5,  # Probabilidade de remover palavras de preenchimento
            },
            "training_iterations": 0,  # Contador de iterações de treinamento
            "last_updated": None  # Data da última atualização
        }
        
        self.save_model()
    
    def save_model(self):
        """
        Salva o modelo de preferências no disco.
        
        Returns:
            bool: True se o modelo foi salvo com sucesso
        """
        import pickle
        import datetime
        
        # Atualizar timestamp
        self.model["last_updated"] = datetime.datetime.now().isoformat()
        
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            return True
        except Exception as e:
            print(f"Erro ao salvar modelo: {e}")
            return False
    
    def get_preferences(self):
        """
        Retorna as preferências atuais do modelo.
        
        Returns:
            dict: Preferências atuais
        """
        return self.model
    
    def update_preference(self, category, preference, value):
        """
        Atualiza uma preferência específica no modelo.
        
        Args:
            category (str): Categoria da preferência
            preference (str): Nome da preferência
            value: Novo valor
            
        Returns:
            bool: True se a atualização foi bem-sucedida
        """
        if category in self.model and preference in self.model[category]:
            self.model[category][preference] = value
            self.save_model()
            return True
        else:
            print(f"Preferência não encontrada: {category}.{preference}")
            return False
```

#### 3.2 Modelo de Aprendizado Adaptativo

```python
class AdaptivePreferenceModel(BasePreferenceModel):
    def __init__(self, model_path="adaptive_preference_model.pkl"):
        """
        Inicializa o modelo adaptativo de preferências.
        
        Args:
            model_path (str): Caminho para salvar/carregar o modelo
        """
        super().__init__(model_path)
        
        # Adicionar parâmetros específicos do modelo adaptativo
        if "learning_rate" not in self.model:
            self.model["learning_rate"] = 0.1  # Taxa de aprendizado
        
        if "confidence" not in self.model:
            self.model["confidence"] = {}  # Confiança em cada preferência
            
            # Inicializar confiança para cada preferência
            for category in ["cut_preferences", "style_preferences", "content_preferences"]:
                self.model["confidence"][category] = {}
                for pref in self.model[category]:
                    self.model["confidence"][category][pref] = 0.5  # Confiança inicial média
    
    def learn_from_feedback(self, learning_data):
        """
        Atualiza o modelo com base nos dados de feedback.
        
        Args:
            learning_data (dict): Dados de aprendizado
            
        Returns:
            dict: Resumo das atualizações realizadas
        """
        updates = {
            "cut_preferences": {},
            "style_preferences": {},
            "content_preferences": {}
        }
        
        # Processar edições manuais
        if "manual_edits" in learning_data and learning_data["manual_edits"]:
            self._learn_from_manual_edits(learning_data["manual_edits"], updates)
        
        # Processar feedback explícito
        if "explicit_feedback" in learning_data and learning_data["explicit_feedback"]:
            self._learn_from_explicit_feedback(learning_data["explicit_feedback"], updates)
        
        # Processar insights
        if "insights" in learning_data and learning_data["insights"]:
            self._learn_from_insights(learning_data["insights"], updates)
        
        # Incrementar contador de iterações
        self.model["training_iterations"] += 1
        
        # Salvar modelo atualizado
        self.save_model()
        
        return updates
    
    def _learn_from_manual_edits(self, manual_edits, updates):
        """
        Aprende com edições manuais feitas pelo usuário.
        
        Args:
            manual_edits (list): Lista de edições manuais
            updates (dict): Dicionário para registrar atualizações
        """
        if not manual_edits:
            return
        
        # Analisar padrões nas edições manuais
        move_distances = []
        removed_cuts = []
        added_cuts = []
        
        for edit in manual_edits:
            if edit["type"] == "move":
                move_distances.append(edit["new"] - edit["original"])
            elif edit["type"] == "remove":
                removed_cuts.append(edit["original"])
            elif edit["type"] == "add":
                added_cuts.append(edit["new"])
        
        # Atualizar preferências com base nos padrões
        
        # 1. Preferência por mover cortes para frente ou para trás
        if move_distances:
            forward_moves = sum(1 for d in move_distances if d > 0)
            backward_moves = sum(1 for d in move_distances if d < 0)
            total_moves = len(move_distances)
            
            if total_moves > 0:
                forward_ratio = forward_moves / total_moves
                
                # Atualizar preferência com taxa de aprendizado
                current = self.model["cut_preferences"]["prefer_forward_cuts"]
                confidence = self.model["confidence"]["cut_preferences"]["prefer_forward_cuts"]
                
                # Quanto maior a confiança, menor o ajuste
                adjustment = self.model["learning_rate"] * (1 - confidence)
                
                # Calcular novo valor
                new_value = current + adjustment * (forward_ratio - 0.5) * 2
                # Limitar entre 0 e 1
                new_value = max(0, min(1, new_value))
                
                # Atualizar modelo
                self.model["cut_preferences"]["prefer_forward_cuts"] = new_value
                
                # Aumentar confiança
                self.model["confidence"]["cut_preferences"]["prefer_forward_cuts"] = min(
                    1.0, confidence + 0.05 * len(move_distances)
                )
                
                updates["cut_preferences"]["prefer_forward_cuts"] = {
                    "old": current,
                    "new": new_value,
                    "confidence": self.model["confidence"]["cut_preferences"]["prefer_forward_cuts"]
                }
        
        # 2. Frequência de cortes
        total_edits = len(manual_edits)
        if total_edits > 0:
            remove_ratio = len(removed_cuts) / total_edits
            add_ratio = len(added_cuts) / total_edits
            
            # Se o usuário remove mais cortes do que adiciona, ele prefere menos cortes
            if remove_ratio > add_ratio:
                current = self.model["style_preferences"]["cut_frequency"]
                confidence = self.model["confidence"]["style_preferences"]["cut_frequency"]
                
                adjustment = self.model["learning_rate"] * (1 - confidence)
                new_value = max(0, current - adjustment * (remove_ratio - add_ratio))
                
                self.model["style_preferences"]["cut_frequency"] = new_value
                self.model["confidence"]["style_preferences"]["cut_frequency"] = min(
                    1.0, confidence + 0.05 * total_edits
                )
                
                updates["style_preferences"]["cut_frequency"] = {
                    "old": current,
                    "new": new_value,
                    "confidence": self.model["confidence"]["style_preferences"]["cut_frequency"]
                }
            # Se o usuário adiciona mais cortes do que remove, ele prefere mais cortes
            elif add_ratio > remove_ratio:
                current = self.model["style_preferences"]["cut_frequency"]
                confidence = self.model["confidence"]["style_preferences"]["cut_frequency"]
                
                adjustment = self.model["learning_rate"] * (1 - confidence)
                new_value = min(1, current + adjustment * (add_ratio - remove_ratio))
                
                self.model["style_preferences"]["cut_frequency"] = new_value
                self.model["confidence"]["style_preferences"]["cut_frequency"] = min(
                    1.0, confidence + 0.05 * total_edits
                )
                
                updates["style_preferences"]["cut_frequency"] = {
                    "old": current,
                    "new": new_value,
                    "confidence": self.model["confidence"]["style_preferences"]["cut_frequency"]
                }
    
    def _learn_from_explicit_feedback(self, explicit_feedback, updates):
        """
        Aprende com feedback explícito do usuário.
        
        Args:
            explicit_feedback (list): Lista de feedbacks explícitos
            updates (dict): Dicionário para registrar atualizações
        """
        if not explicit_feedback:
            return
        
        # Calcular média das avaliações
        avg_rating = sum(f["rating"] for f in explicit_feedback) / len(explicit_feedback)
        
        # Se a média for alta (> 3), reforçar as preferências atuais
        # Se for baixa (< 3), ajustar na direção oposta
        if avg_rating > 3:
            # Aumentar confiança nas preferências atuais
            for category in ["cut_preferences", "style_preferences", "content_preferences"]:
                for pref in self.model[category]:
                    current_confidence = self.model["confidence"][category][pref]
                    # Aumentar confiança proporcionalmente à avaliação
                    confidence_boost = 0.02 * (avg_rating - 3)
                    new_confidence = min(1.0, current_confidence + confidence_boost)
                    
                    self.model["confidence"][category][pref] = new_confidence
                    
                    if category not in updates:
                        updates[category] = {}
                    
                    if pref not in updates[category]:
                        updates[category][pref] = {}
                    
                    updates[category][pref]["confidence_change"] = new_confidence - current_confidence
        
        elif avg_rating < 3:
            # Reduzir confiança e ajustar preferências na direção oposta
            for category in ["cut_preferences", "style_preferences", "content_preferences"]:
                for pref in self.model[category]:
                    current_value = self.model[category][pref]
                    current_confidence = self.model["confidence"][category][pref]
                    
                    # Reduzir confiança
                    confidence_reduction = 0.02 * (3 - avg_rating)
                    new_confidence = max(0.1, current_confidence - confidence_reduction)
                    
                    # Ajustar valor na direção oposta para valores numéricos
                    if isinstance(current_value, (int, float)) and 0 <= current_value <= 1:
                        # Quanto menor a confiança, maior o ajuste
                        adjustment = self.model["learning_rate"] * (1 - new_confidence) * (3 - avg_rating) / 2
                        
                        # Mover na direção oposta
                        if current_value > 0.5:
                            new_value = max(0, current_value - adjustment)
                        else:
                            new_value = min(1, current_value + adjustment)
                        
                        self.model[category][pref] = new_value
                        
                        if category not in updates:
                            updates[category] = {}
                        
                        if pref not in updates[category]:
                            updates[category][pref] = {}
                        
                        updates[category][pref] = {
                            "old": current_value,
                            "new": new_value,
                            "confidence": new_confidence
                        }
                    
                    self.model["confidence"][category][pref] = new_confidence
    
    def _learn_from_insights(self, insights, updates):
        """
        Aprende com insights derivados da análise de padrões.
        
        Args:
            insights (dict): Insights gerados pela análise de padrões
            updates (dict): Dicionário para registrar atualizações
        """
        # Aprender com padrões de corte
        if "cut_patterns" in insights and insights["cut_patterns"]:
            cut_patterns = insights["cut_patterns"]
            
            # Ajustar preferência de ritmo com base na média de distância de movimentos
            if "avg_move_distance" in cut_patterns:
                avg_move = cut_patterns["avg_move_distance"]
                
                # Se a média for positiva, o usuário prefere cortes mais tardios
                # Se for negativa, prefere cortes mais cedo
                if abs(avg_move) > 0.2:  # Limiar para considerar significativo
                    current = self.model["style_preferences"]["pace"]
                    confidence = self.model["confidence"]["style_preferences"]["pace"]
                    
                    # Normalizar para um valor entre -0.5 e 0.5
                    normalized_move = max(-0.5, min(0.5, avg_move / 2))
                    
                    # Ajustar com base na direção do movimento
                    adjustment = self.model["learning_rate"] * (1 - confidence) * normalized_move
                    
                    # Valores positivos de avg_move indicam preferência por ritmo mais lento
                    new_value = max(0, min(1, current - adjustment))
                    
                    self.model["style_preferences"]["pace"] = new_value
                    self.model["confidence"]["style_preferences"]["pace"] = min(
                        1.0, confidence + 0.05
                    )
                    
                    updates["style_preferences"]["pace"] = {
                        "old": current,
                        "new": new_value,
                        "confidence": self.model["confidence"]["style_preferences"]["pace"]
                    }
        
        # Aprender com preferências de conteúdo
        if "content_preferences" in insights and insights["content_preferences"]:
            content_prefs = insights["content_preferences"]
            
            # Exemplo: ajustar preferência de remoção de silêncio com base no tipo de edição mais comum
            if "add" in content_prefs and "remove" in content_prefs:
                if content_prefs["remove"] > content_prefs["add"]:
                    # Usuário tende a remover mais do que adicionar
                    current = self.model["content_preferences"]["remove_silence"]
                    confidence = self.model["confidence"]["content_preferences"]["remove_silence"]
                    
                    adjustment = self.model["learning_rate"] * (1 - confidence) * 0.2
                    new_value = min(1, current + adjustment)
                    
                    self.model["content_preferences"]["remove_silence"] = new_value
                    self.model["confidence"]["content_preferences"]["remove_silence"] = min(
                        1.0, confidence + 0.05
                    )
                    
                    updates["content_preferences"]["remove_silence"] = {
                        "old": current,
                        "new": new_value,
                        "confidence": self.model["confidence"]["content_preferences"]["remove_silence"]
                    }
        
        # Aprender com métricas de desempenho
        if "performance" in insights and insights["performance"]:
            performance = insights["performance"]
            
            # Exemplo: ajustar preferências com base na taxa de retenção média
            if "avg_retention_rate" in performance:
                retention = performance["avg_retention_rate"]
                
                # Se a retenção for alta, reforçar as preferências atuais
                if retention > 0.7:  # Bom valor de retenção
                    for category in ["cut_preferences", "style_preferences", "content_preferences"]:
                        for pref in self.model[category]:
                            current_confidence = self.model["confidence"][category][pref]
                            # Aumentar confiança proporcionalmente à retenção
                            confidence_boost = 0.02 * (retention - 0.7) * 10  # Normalizar para 0-0.6
                            new_confidence = min(1.0, current_confidence + confidence_boost)
                            
                            self.model["confidence"][category][pref] = new_confidence
```

#### 3.3 Gerenciador de Perfis de Usuário

```python
class UserProfileManager:
    def __init__(self, profiles_dir="user_profiles"):
        """
        Inicializa o gerenciador de perfis de usuário.
        
        Args:
            profiles_dir (str): Diretório para armazenar perfis de usuário
        """
        import os
        
        self.profiles_dir = profiles_dir
        
        # Criar diretório se não existir
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
        
        self.current_profile = None
        self.current_profile_name = None
    
    def list_profiles(self):
        """
        Lista todos os perfis disponíveis.
        
        Returns:
            list: Lista de nomes de perfis
        """
        import os
        
        profiles = []
        
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".pkl") and not filename.startswith("."):
                profiles.append(filename[:-4])  # Remover extensão .pkl
        
        return profiles
    
    def create_profile(self, profile_name):
        """
        Cria um novo perfil de usuário.
        
        Args:
            profile_name (str): Nome do perfil
            
        Returns:
            bool: True se o perfil foi criado com sucesso
        """
        import os
        
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.pkl")
        
        if os.path.exists(profile_path):
            print(f"Perfil '{profile_name}' já existe.")
            return False
        
        # Criar novo modelo para o perfil
        model = AdaptivePreferenceModel(profile_path)
        
        self.current_profile = model
        self.current_profile_name = profile_name
        
        return True
    
    def load_profile(self, profile_name):
        """
        Carrega um perfil existente.
        
        Args:
            profile_name (str): Nome do perfil
            
        Returns:
            bool: True se o perfil foi carregado com sucesso
        """
        import os
        
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.pkl")
        
        if not os.path.exists(profile_path):
            print(f"Perfil '{profile_name}' não encontrado.")
            return False
        
        # Carregar modelo do perfil
        model = AdaptivePreferenceModel(profile_path)
        
        self.current_profile = model
        self.current_profile_name = profile_name
        
        return True
    
    def get_current_profile(self):
        """
        Retorna o perfil atual.
        
        Returns:
            AdaptivePreferenceModel: Modelo do perfil atual
        """
        return self.current_profile
    
    def export_profile(self, profile_name, export_path):
        """
        Exporta um perfil para um arquivo externo.
        
        Args:
            profile_name (str): Nome do perfil
            export_path (str): Caminho para exportar o perfil
            
        Returns:
            bool: True se o perfil foi exportado com sucesso
        """
        import os
        import shutil
        
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.pkl")
        
        if not os.path.exists(profile_path):
            print(f"Perfil '{profile_name}' não encontrado.")
            return False
        
        try:
            shutil.copy2(profile_path, export_path)
            return True
        except Exception as e:
            print(f"Erro ao exportar perfil: {e}")
            return False
    
    def import_profile(self, import_path, profile_name=None):
        """
        Importa um perfil de um arquivo externo.
        
        Args:
            import_path (str): Caminho do arquivo a importar
            profile_name (str, opcional): Nome para o perfil importado
            
        Returns:
            bool: True se o perfil foi importado com sucesso
        """
        import os
        import shutil
        
        if not os.path.exists(import_path):
            print(f"Arquivo '{import_path}' não encontrado.")
            return False
        
        # Se o nome não for especificado, usar o nome do arquivo
        if profile_name is None:
            profile_name = os.path.basename(import_path)
            if profile_name.endswith(".pkl"):
                profile_name = profile_name[:-4]
        
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.pkl")
        
        try:
            shutil.copy2(import_path, profile_path)
            return True
        except Exception as e:
            print(f"Erro ao importar perfil: {e}")
            return False
```

### 4. Módulo de Aplicação de Preferências

Este módulo aplica as preferências aprendidas ao processo de edição de vídeo:

#### 4.1 Ajustador de Parâmetros de Edição

```python
class EditingParametersAdjuster:
    def __init__(self, preference_model):
        """
        Inicializa o ajustador de parâmetros de edição.
        
        Args:
            preference_model: Modelo de preferências do usuário
        """
        self.preference_model = preference_model
    
    def adjust_cut_detection_parameters(self):
        """
        Ajusta os parâmetros para detecção de pontos de corte com base nas preferências.
        
        Returns:
            dict: Parâmetros ajustados
        """
        preferences = self.preference_model.get_preferences()
        
        # Extrair preferências relevantes
        cut_prefs = preferences["cut_preferences"]
        style_prefs = preferences["style_preferences"]
        
        # Parâmetros base para detecção de cortes
        params = {
            "min_segment_duration": cut_prefs["min_segment_duration"],
            "sentence_boundary_weight": cut_prefs["prefer_sentence_boundaries"],
            "silence_weight": cut_prefs["prefer_silence"],
            "mid_sentence_penalty": cut_prefs["avoid_mid_sentence"],
            "forward_cut_bias": (cut_prefs["prefer_forward_cuts"] - 0.5) * 2,  # Converter para [-1, 1]
            
            # Parâmetros derivados do estilo
            "target_cut_frequency": style_prefs["cut_frequency"],
            "pace_factor": style_prefs["pace"],
            "transition_style": style_prefs["transition_style"],
            "audio_clarity_weight": 1 - style_prefs["audio_balance"],
            "audio_rhythm_weight": style_prefs["audio_balance"],
        }
        
        # Ajustar duração mínima de segmento com base no ritmo desejado
        # Ritmo mais rápido = segmentos mais curtos
        pace_adjustment = (1 - style_prefs["pace"]) * 3  # 0 = rápido (1s), 1 = lento (4s)
        params["min_segment_duration"] = max(1.0, params["min_segment_duration"] + pace_adjustment)
        
        return params
    
    def adjust_content_filtering_parameters(self):
        """
        Ajusta os parâmetros para filtragem de conteúdo com base nas preferências.
        
        Returns:
            dict: Parâmetros ajustados
        """
        preferences = self.preference_model.get_preferences()
        
        # Extrair preferências de conteúdo
        content_prefs = preferences["content_preferences"]
        
        # Parâmetros para filtragem de conteúdo
        params = {
            "intro_threshold": content_prefs["keep_intro"],
            "conclusion_threshold": content_prefs["keep_conclusion"],
            "example_threshold": content_prefs["keep_examples"],
            "silence_removal_threshold": content_prefs["remove_silence"],
            "filler_word_removal_threshold": content_prefs["remove_filler_words"],
        }
        
        return params
    
    def get_all_adjusted_parameters(self):
        """
        Retorna todos os parâmetros ajustados para o processo de edição.
        
        Returns:
            dict: Todos os parâmetros ajustados
        """
        cut_params = self.adjust_cut_detection_parameters()
        content_params = self.adjust_content_filtering_parameters()
        
        # Combinar todos os parâmetros
        all_params = {
            "cut_detection": cut_params,
            "content_filtering": content_params,
            "model_confidence": self.preference_model.model.get("confidence", {}),
            "model_version": {
                "iterations": self.preference_model.model.get("training_iterations", 0),
                "last_updated": self.preference_model.model.get("last_updated", None)
            }
        }
        
        return all_params
```

#### 4.2 Integrador de Edição Inteligente

```python
class IntelligentEditingIntegrator:
    def __init__(self, preference_model=None, profile_manager=None):
        """
        Inicializa o integrador de edição inteligente.
        
        Args:
            preference_model: Modelo de preferências do usuário
            profile_manager: Gerenciador de perfis de usuário
        """
        self.profile_manager = profile_manager
        
        if preference_model:
            self.preference_model = preference_model
        elif profile_manager and profile_manager.get_current_profile():
            self.preference_model = profile_manager.get_current_profile()
        else:
            # Criar modelo padrão
            self.preference_model = AdaptivePreferenceModel()
        
        self.parameters_adjuster = EditingParametersAdjuster(self.preference_model)
        self.feedback_processor = FeedbackProcessor()
    
    def process_video(self, video_path, output_path, user_preferences=None):
        """
        Processa um vídeo com edição inteligente baseada nas preferências aprendidas.
        
        Args:
            video_path (str): Caminho para o arquivo de vídeo de entrada
            output_path (str): Caminho para salvar o vídeo editado
            user_preferences (dict, opcional): Preferências específicas para esta edição
            
        Returns:
            dict: Resultados do processamento
        """
        import os
        import json
        import time
        
        # Gerar ID único para o vídeo
        video_id = f"{os.path.basename(video_path)}_{int(time.time())}"
        
        # Obter parâmetros ajustados
        params = self.parameters_adjuster.get_all_adjusted_parameters()
        
        # Sobrescrever com preferências específicas para esta edição
        if user_preferences:
            for category in user_preferences:
                if category in params:
                    for param, value in user_preferences[category].items():
                        if param in params[category]:
                            params[category][param] = value
        
        # Salvar parâmetros para referência
        params_path = f"{output_path}_params.json"
        with open(params_path, 'w') as f:
            json.dump(params, f, indent=2)
        
        # Aqui chamaria a função de processamento de vídeo com os parâmetros ajustados
        # Esta é uma implementação simulada
        result = {
            "video_id": video_id,
            "input_path": video_path,
            "output_path": output_path,
            "parameters": params,
            "processing_time": 0,
            "status": "success"
        }
        
        # Simulação de processamento
        print(f"Processando vídeo {video_path} com parâmetros personalizados...")
        time.sleep(1)  # Simulação de tempo de processamento
        
        # Em uma implementação real, aqui chamaria:
        # from audio_analysis import process_video_with_intelligent_editing
        # process_video_with_intelligent_editing(video_path, output_path, params=params)
        
        result["processing_time"] = 1.0  # Tempo simulado
        
        return result
    
    def update_model_from_feedback(self):
        """
        Atualiza o modelo de preferências com base no feedback coletado.
        
        Returns:
            dict: Resumo das atualizações realizadas
        """
        # Gerar dados de aprendizado a partir do feedback
        learning_data = self.feedback_processor.generate_learning_data()
        
        # Atualizar modelo com os dados
        updates = self.preference_model.learn_from_feedback(learning_data)
        
        return {
            "status": "success",
            "updates": updates,
            "model_info": {
                "iterations": self.preference_model.model["training_iterations"],
                "last_updated": self.preference_model.model["last_updated"]
            }
        }
    
    def record_feedback(self, video_id, feedback_type, data):
        """
        Registra feedback do usuário para uso futuro no aprendizado.
        
        Args:
            video_id (str): Identificador do vídeo
            feedback_type (str): Tipo de feedback ('explicit', 'manual_edit', 'engagement')
            data (dict): Dados do feedback
            
        Returns:
            bool: True se o feedback foi registrado com sucesso
        """
        if feedback_type == "explicit":
            if "rating" in data:
                return self.feedback_processor.explicit_collector.record_rating(
                    video_id, data["rating"], data.get("comment")
                )
            elif "timestamp" in data and "rating" in data:
                return self.feedback_processor.explicit_collector.record_timestamp_feedback(
                    video_id, data["timestamp"], data["rating"], data.get("comment")
                )
        
        elif feedback_type == "manual_edit":
            if all(k in data for k in ["original_cut_point", "new_cut_point", "edit_type"]):
                return self.feedback_processor.implicit_collector.record_manual_edit(
                    video_id, data["original_cut_point"], data["new_cut_point"], data["edit_type"]
                )
        
        elif feedback_type == "engagement":
            if "platform" in data and isinstance(data.get("metrics"), dict):
                return self.feedback_processor.results_analyzer.record_engagement_metrics(
                    video_id, data["platform"], data["metrics"]
                )
        
        return False
```

### 5. Interface de Usuário para o Sistema de Aprendizado

Este módulo fornece uma interface para o usuário interagir com o sistema de aprendizado:

#### 5.1 Interface de Configuração de Preferências

```python
class PreferenceConfigUI:
    def __init__(self, preference_model, profile_manager=None):
        """
        Inicializa a interface de configuração de preferências.
        
        Args:
            preference_model: Modelo de preferências do usuário
            profile_manager: Gerenciador de perfis de usuário
        """
        self.preference_model = preference_model
        self.profile_manager = profile_manager
    
    def generate_config_ui_data(self):
        """
        Gera dados para a interface de configuração de preferências.
        
        Returns:
            dict: Dados para a interface
        """
        preferences = self.preference_model.get_preferences()
        
        # Estruturar dados para a interface
        ui_data = {
            "sections": [
                {
                    "id": "cut_preferences",
                    "title": "Preferências de Corte",
                    "description": "Configure como o sistema deve decidir onde fazer cortes no vídeo.",
                    "controls": []
                },
                {
                    "id": "style_preferences",
                    "title": "Preferências de Estilo",
                    "description": "Ajuste o estilo geral da edição.",
                    "controls": []
                },
                {
                    "id": "content_preferences",
                    "title": "Preferências de Conteúdo",
                    "description": "Defina quais tipos de conteúdo devem ser mantidos ou removidos.",
                    "controls": []
                }
            ],
            "profiles": []
        }
        
        # Adicionar controles para cada preferência
        
        # Seção de preferências de corte
        cut_section = ui_data["sections"][0]
        for pref, value in preferences["cut_preferences"].items():
            control = self._create_control_for_preference("cut_preferences", pref, value)
            if control:
                cut_section["controls"].append(control)
        
        # Seção de preferências de estilo
        style_section = ui_data["sections"][1]
        for pref, value in preferences["style_preferences"].items():
            control = self._create_control_for_preference("style_preferences", pref, value)
            if control:
                style_section["controls"].append(control)
        
        # Seção de preferências de conteúdo
        content_section = ui_data["sections"][2]
        for pref, value in preferences["content_preferences"].items():
            control = self._create_control_for_preference("content_preferences", pref, value)
            if control:
                content_section["controls"].append(control)
        
        # Adicionar perfis disponíveis
        if self.profile_manager:
            ui_data["profiles"] = self.profile_manager.list_profiles()
            ui_data["current_profile"] = self.profile_manager.current_profile_name
        
        # Adicionar informações do modelo
        ui_data["model_info"] = {
            "training_iterations": preferences.get("training_iterations", 0),
            "last_updated": preferences.get("last_updated", None)
        }
        
        return ui_data
    
    def _create_control_for_preference(self, category, pref, value):
        """
        Cria um controle de interface para uma preferência específica.
        
        Args:
            category (str): Categoria da preferência
            pref (str): Nome da preferência
            value: Valor atual da preferência
            
        Returns:
            dict: Definição do controle
        """
        # Mapear nomes de preferências para rótulos amigáveis
        labels = {
            "min_segment_duration": "Duração Mínima de Segmento",
            "prefer_sentence_boundaries": "Priorizar Limites de Frases",
            "prefer_silence": "Priorizar Silêncios",
            "avoid_mid_sentence": "Evitar Cortes no Meio de Frases",
            "prefer_forward_cuts": "Preferência por Cortes Adiantados/Atrasados",
            
            "pace": "Ritmo da Edição",
            "cut_frequency": "Frequência de Cortes",
            "transition_style": "Estilo de Transição",
            "audio_balance": "Equilíbrio de Áudio",
            
            "keep_intro": "Manter Introduções",
            "keep_conclusion": "Manter Conclusões",
            "keep_examples": "Manter Exemplos",
            "remove_silence": "Remover Silêncios",
            "remove_filler_words": "Remover Palavras de Preenchimento"
        }
        
        # Mapear nomes de preferências para descrições
        descriptions = {
            "min_segment_duration": "Duração mínima (em segundos) que um segmento deve ter para ser mantido.",
            "prefer_sentence_boundaries": "Quanto maior o valor, mais o sistema priorizará cortes no final de frases.",
            "prefer_silence": "Quanto maior o valor, mais o sistema priorizará cortes em momentos de silêncio.",
            "avoid_mid_sentence": "Quanto maior o valor, mais o sistema evitará cortes no meio de frases.",
            "prefer_forward_cuts": "Valores abaixo de 0.5 favorecem cortes antecipados, acima de 0.5 favorecem cortes tardios.",
            
            "pace": "Valores baixos resultam em edições mais rápidas, valores altos em edições mais lentas.",
            "cut_frequency": "Valores baixos resultam em menos cortes, valores altos em mais cortes.",
            "transition_style": "Estilo de transição entre segmentos.",
            "audio_balance": "Valores baixos priorizam clareza, valores altos priorizam ritmo.",
            
            "keep_intro": "Probabilidade de manter seções introdutórias.",
            "keep_conclusion": "Probabilidade de manter conclusões e resumos.",
            "keep_examples": "Probabilidade de manter exemplos e demonstrações.",
            "remove_silence": "Probabilidade de remover períodos de silêncio.",
            "remove_filler_words": "Probabilidade de remover palavras de preenchimento (\"hum\", \"é\", etc.)."
        }
        
        # Obter confiança no valor atual
        confidence = 0.5
        if "confidence" in self.preference_model.model and category in self.preference_model.model["confidence"]:
            if pref in self.preference_model.model["confidence"][category]:
                confidence = self.preference_model.model["confidence"][category][pref]
        
        # Criar controle com base no tipo de valor
        control = {
            "id": pref,
            "label": labels.get(pref, pref),
            "description": descriptions.get(pref, ""),
            "confidence": confidence
        }
        
        if isinstance(value, (int, float)) and pref != "min_segment_duration":
            # Slider para valores entre 0 e 1
            control["type"] = "slider"
            control["min"] = 0
            control["max"] = 1
            control["step"] = 0.05
            control["value"] = value
            
            # Adicionar rótulos específicos para alguns controles
            if pref == "prefer_forward_cuts":
                control["min_label"] = "Cortes Antecipados"
                control["max_label"] = "Cortes Tardios"
            elif pref == "pace":
                control["min_label"] = "Rápido"
                control["max_label"] = "Lento"
            elif pref == "cut_frequency":
                control["min_label"] = "Poucos Cortes"
                control["max_label"] = "Muitos Cortes"
            elif pref == "audio_balance":
                control["min_label"] = "Priorizar Clareza"
                control["max_label"] = "Priorizar Ritmo"
        
        elif pref == "min_segment_duration":
            # Slider para duração em segundos
            control["type"] = "slider"
            control["min"] = 0.5
            control["max"] = 10
            control["step"] = 0.5
            control["value"] = value
            control["unit"] = "segundos"
        
        elif pref == "transition_style":
            # Seletor para estilo de transição
            control["type"] = "select"
            control["options"] = [
                {"value": "cut", "label": "Corte Seco"},
                {"value": "fade", "label": "Fade"},
                {"value": "dissolve", "label": "Dissolve"},
                {"value": "wipe", "label": "Wipe"}
            ]
            control["value"] = value
        
        else:
            # Tipo não suportado
            return None
        
        return control
    
    def apply_ui_preferences(self, ui_preferences):
        """
        Aplica preferências definidas pelo usuário na interface.
        
        Args:
            ui_preferences (dict): Preferências definidas pelo usuário
            
        Returns:
            dict: Resultado da aplicação
        """
        updates = {"applied": [], "errors": []}
        
        for section in ui_preferences.get("sections", []):
            category = section["id"]
            
            for control in section.get("controls", []):
                pref_id = control["id"]
                value = control["value"]
                
                # Validar valor
                if not self._validate_preference_value(category, pref_id, value):
                    updates["errors"].append(f"Valor inválido para {category}.{pref_id}: {value}")
                    continue
                
                # Atualizar preferência
                success = self.preference_model.update_preference(category, pref_id, value)
                
                if success:
                    updates["applied"].append(f"{category}.{pref_id}")
                else:
                    updates["errors"].append(f"Falha ao atualizar {category}.{pref_id}")
        
        # Salvar modelo
        self.preference_model.save_model()
        
        return updates
    
    def _validate_preference_value(self, category, pref, value):
        """
        Valida um valor de preferência.
        
        Args:
            category (str): Categoria da preferência
            pref (str): Nome da preferência
            value: Valor a validar
            
        Returns:
            bool: True se o valor é válido
        """
        # Validações específicas por categoria e preferência
        if category in ["cut_preferences", "style_preferences", "content_preferences"]:
            if pref in ["min_segment_duration"]:
                return isinstance(value, (int, float)) and 0.5 <= value <= 10
            
            elif pref in ["transition_style"]:
                return value in ["cut", "fade", "dissolve", "wipe"]
            
            elif pref in [
                "prefer_sentence_boundaries", "prefer_silence", "avoid_mid_sentence",
                "prefer_forward_cuts", "pace", "cut_frequency", "audio_balance",
                "keep_intro", "keep_conclusion", "keep_examples",
                "remove_silence", "remove_filler_words"
            ]:
                return isinstance(value, (int, float)) and 0 <= value <= 1
        
        return False
```

#### 5.2 Visualizador de Aprendizado

```python
class LearningVisualizer:
    def __init__(self, preference_model, feedback_processor):
        """
        Inicializa o visualizador de aprendizado.
        
        Args:
            preference_model: Modelo de preferências do usuário
            feedback_processor: Processador de feedback
        """
        self.preference_model = preference_model
        self.feedback_processor = feedback_processor
    
    def generate_learning_visualization_data(self):
        """
        Gera dados para visualização do processo de aprendizado.
        
        Returns:
            dict: Dados para visualização
        """
        # Obter preferências atuais
        preferences = self.preference_model.get_preferences()
        
        # Obter histórico de feedback
        feedback_history = self._get_feedback_history()
        
        # Gerar dados para gráficos
        visualization_data = {
            "preference_evolution": self._generate_preference_evolution_data(),
            "confidence_levels": self._generate_confidence_levels_data(),
            "feedback_summary": self._generate_feedback_summary_data(feedback_history),
            "performance_metrics": self._generate_performance_metrics_data()
        }
        
        return visualization_data
    
    def _get_feedback_history(self):
        """
        Obtém o histórico de feedback do usuário.
        
        Returns:
            dict: Histórico de feedback
        """
        import sqlite3
        
        conn = sqlite3.connect(self.feedback_processor.explicit_collector.feedback_db_path)
        cursor = conn.cursor()
        
        # Obter feedback explícito
        cursor.execute("""
        SELECT video_id, timestamp, rating, created_at 
        FROM explicit_feedback 
        ORDER BY created_at
        """)
        explicit_feedback = cursor.fetchall()
        
        # Obter edições manuais
        cursor.execute("""
        SELECT video_id, edit_type, created_at 
        FROM manual_edits 
        ORDER BY created_at
        """)
        manual_edits = cursor.fetchall()
        
        conn.close()
        
        # Estruturar dados
        history = {
            "explicit_feedback": [
                {
                    "video_id": row[0],
                    "timestamp": row[1],
                    "rating": row[2],
                    "date": row[3]
                }
                for row in explicit_feedback
            ],
            "manual_edits": [
                {
                    "video_id": row[0],
                    "edit_type": row[1],
                    "date": row[2]
                }
                for row in manual_edits
            ]
        }
        
        return history
    
    def _generate_preference_evolution_data(self):
        """
        Gera dados sobre a evolução das preferências ao longo do tempo.
        
        Returns:
            dict: Dados de evolução de preferências
        """
        # Em uma implementação real, isso exigiria armazenar o histórico de valores
        # Aqui, simulamos alguns dados para demonstração
        
        # Categorias e preferências a visualizar
        categories = ["cut_preferences", "style_preferences", "content_preferences"]
        key_preferences = {
            "cut_preferences": ["prefer_sentence_boundaries", "prefer_silence"],
            "style_preferences": ["pace", "cut_frequency"],
            "content_preferences": ["remove_silence", "keep_intro"]
        }
        
        # Gerar dados simulados
        evolution_data = {}
        
        for category in categories:
            evolution_data[category] = {}
            
            for pref in key_preferences[category]:
                # Valor atual
                current_value = self.preference_model.model[category][pref]
                
                # Simular histórico (5 pontos no passado)
                history = []
                for i in range(5):
                    # Variação aleatória em torno do valor atual
                    import random
                    variation = (random.random() - 0.5) * 0.2
                    historical_value = max(0, min(1, current_value + variation))
                    
                    # Data simulada (dias no passado)
                    import datetime
                    days_ago = (5 - i) * 7  # Semanas no passado
                    date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).isoformat()
                    
                    history.append({
                        "date": date,
                        "value": historical_value
                    })
                
                # Adicionar valor atual
                history.append({
                    "date": datetime.datetime.now().isoformat(),
                    "value": current_value
                })
                
                evolution_data[category][pref] = history
        
        return evolution_data
    
    def _generate_confidence_levels_data(self):
        """
        Gera dados sobre os níveis de confiança nas preferências.
        
        Returns:
            dict: Dados de níveis de confiança
        """
        confidence_data = {}
        
        # Verificar se o modelo tem dados de confiança
        if "confidence" in self.preference_model.model:
            confidence = self.preference_model.model["confidence"]
            
            for category in confidence:
                confidence_data[category] = {}
                
                for pref, value in confidence[category].items():
                    confidence_data[category][pref] = value
        
        return confidence_data
    
    def _generate_feedback_summary_data(self, feedback_history):
        """
        Gera um resumo dos dados de feedback.
        
        Args:
            feedback_history (dict): Histórico de feedback
            
        Returns:
            dict: Resumo dos dados de feedback
        """
        # Contar avaliações por valor
        ratings_count = {}
        for feedback in feedback_history["explicit_feedback"]:
            rating = feedback["rating"]
            if rating not in ratings_count:
                ratings_count[rating] = 0
            ratings_count[rating] += 1
        
        # Contar edições por tipo
        edits_count = {}
        for edit in feedback_history["manual_edits"]:
            edit_type = edit["edit_type"]
            if edit_type not in edits_count:
                edits_count[edit_type] = 0
            edits_count[edit_type] += 1
        
        # Estruturar resumo
        summary = {
            "total_explicit_feedback": len(feedback_history["explicit_feedback"]),
            "total_manual_edits": len(feedback_history["manual_edits"]),
            "ratings_distribution": ratings_count,
            "edits_distribution": edits_count
        }
        
        return summary
    
    def _generate_performance_metrics_data(self):
        """
        Gera métricas de desempenho dos vídeos editados.
        
        Returns:
            dict: Métricas de desempenho
        """
        # Em uma implementação real, isso viria do banco de dados de resultados
        # Aqui, simulamos alguns dados para demonstração
        
        metrics = {
            "avg_retention_rate": 0.72,
            "avg_engagement_score": 0.68,
            "platform_performance": {
                "youtube": {"views": 1250, "likes": 87, "comments": 23},
                "instagram": {"views": 2100, "likes": 145, "comments": 18},
                "tiktok": {"views": 3500, "likes": 210, "comments": 42}
            }
        }
        
        return metrics
```

## Integração com o Sistema Principal

O sistema de aprendizado será integrado ao software de automação de vídeos existente através dos seguintes componentes:

### 1. Inicialização e Configuração

```python
def initialize_learning_system(config_path=None):
    """
    Inicializa o sistema de aprendizado.
    
    Args:
        config_path (str, opcional): Caminho para arquivo de configuração
        
    Returns:
        tuple: (profile_manager, editing_integrator)
    """
    import os
    import json
    
    # Diretórios padrão
    base_dir = os.path.expanduser("~/.videobook_ai")
    profiles_dir = os.path.join(base_dir, "profiles")
    feedback_db_path = os.path.join(base_dir, "feedback.db")
    results_db_path = os.path.join(base_dir, "results.db")
    
    # Criar diretórios se não existirem
    for directory in [base_dir, profiles_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Carregar configuração personalizada
    config = {}
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
    
    # Aplicar configurações personalizadas
    profiles_dir = config.get("profiles_dir", profiles_dir)
    feedback_db_path = config.get("feedback_db_path", feedback_db_path)
    results_db_path = config.get("results_db_path", results_db_path)
    
    # Inicializar componentes
    profile_manager = UserProfileManager(profiles_dir)
    
    # Carregar perfil padrão ou criar um novo
    profiles = profile_manager.list_profiles()
    if profiles:
        profile_manager.load_profile(profiles[0])
    else:
        profile_manager.create_profile("default")
    
    # Inicializar integrador de edição
    editing_integrator = IntelligentEditingIntegrator(
        preference_model=profile_manager.get_current_profile(),
        profile_manager=profile_manager
    )
    
    return profile_manager, editing_integrator
```

### 2. Fluxo de Processamento de Vídeo

```python
def process_video_with_learning(video_path, output_path, user_preferences=None):
    """
    Processa um vídeo com o sistema de aprendizado.
    
    Args:
        video_path (str): Caminho para o arquivo de vídeo
        output_path (str): Caminho para salvar o vídeo editado
        user_preferences (dict, opcional): Preferências específicas para esta edição
        
    Returns:
        dict: Resultados do processamento
    """
    # Inicializar sistema de aprendizado
    profile_manager, editing_integrator = initialize_learning_system()
    
    # Processar vídeo
    result = editing_integrator.process_video(video_path, output_path, user_preferences)
    
    return result
```

### 3. Coleta de Feedback

```python
def record_user_feedback(video_id, feedback_type, data):
    """
    Registra feedback do usuário para uso futuro no aprendizado.
    
    Args:
        video_id (str): Identificador do vídeo
        feedback_type (str): Tipo de feedback ('explicit', 'manual_edit', 'engagement')
        data (dict): Dados do feedback
        
    Returns:
        bool: True se o feedback foi registrado com sucesso
    """
    # Inicializar sistema de aprendizado
    profile_manager, editing_integrator = initialize_learning_system()
    
    # Registrar feedback
    success = editing_integrator.record_feedback(video_id, feedback_type, data)
    
    return success
```

### 4. Atualização do Modelo

```python
def update_learning_model():
    """
    Atualiza o modelo de aprendizado com base no feedback coletado.
    
    Returns:
        dict: Resumo das atualizações realizadas
    """
    # Inicializar sistema de aprendizado
    profile_manager, editing_integrator = initialize_learning_system()
    
    # Atualizar modelo
    updates = editing_integrator.update_model_from_feedback()
    
    return updates
```

### 5. Interface de Configuração

```python
def generate_preferences_ui_data():
    """
    Gera dados para a interface de configuração de preferências.
    
    Returns:
        dict: Dados para a interface
    """
    # Inicializar sistema de aprendizado
    profile_manager, editing_integrator = initialize_learning_system()
    
    # Criar interface de configuração
    config_ui = PreferenceConfigUI(
        preference_model=profile_manager.get_current_profile(),
        profile_manager=profile_manager
    )
    
    # Gerar dados para a interface
    ui_data = config_ui.generate_config_ui_data()
    
    return ui_data
```

## Requisitos de Sistema

Para garantir que o sistema de aprendizado possa funcionar em computadores comuns sem necessidade de hardware especializado:

- **Python**: 3.8 ou superior
- **Bibliotecas**:
  - `numpy`: Para cálculos numéricos
  - `scikit-learn`: Para algoritmos básicos de aprendizado de máquina
  - `sqlite3`: Para armazenamento de dados (parte da biblioteca padrão)
  - `matplotlib`: Para visualização (opcional)
- **Armazenamento**: ~50MB para modelos e bancos de dados
- **Memória**: ~200MB durante o processamento

## Considerações de Implementação

### Privacidade e Processamento Local

- Todo o processamento e aprendizado ocorre localmente no computador do usuário
- Nenhum dado é enviado para servidores externos
- Os perfis de usuário podem ser exportados e importados para transferência entre dispositivos

### Desempenho em Hardware Comum

- O sistema é projetado para funcionar em computadores comuns sem hardware especializado
- Modelos leves são usados para garantir desempenho adequado
- O processamento é otimizado para minimizar o uso de recursos

### Evolução Gradual

- O sistema começa com configurações padrão razoáveis
- A adaptação é gradual para evitar mudanças bruscas na experiência do usuário
- A confiança nas preferências aumenta com o tempo e uso

## Próximos Passos

1. Implementação dos componentes básicos do sistema de aprendizado
2. Integração com o módulo de análise de áudio
3. Desenvolvimento da interface de usuário para configuração e feedback
4. Testes com diferentes tipos de conteúdo e usuários
5. Otimização de desempenho e uso de recursos
6. Implementação de recursos avançados de visualização e análise

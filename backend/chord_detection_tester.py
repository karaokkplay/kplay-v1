import music21
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import tempfile

class ChordDetectionTester:
    """
    Classe para testar a precisão da detecção de acordes em arquivos MIDI.
    """
    
    def __init__(self, extractor, test_files_dir=None, ground_truth_file=None):
        """
        Inicializa o testador de detecção de acordes.
        
        Args:
            extractor: Instância do extrator de acordes a ser testado
            test_files_dir (str, optional): Diretório contendo arquivos MIDI de teste
            ground_truth_file (str, optional): Arquivo JSON com acordes corretos para comparação
        """
        self.extractor = extractor
        self.test_files_dir = test_files_dir
        self.ground_truth_file = ground_truth_file
        self.ground_truth = self._load_ground_truth()
        self.results = {}
        
    def _load_ground_truth(self):
        """
        Carrega os dados de ground truth para comparação.
        """
        if not self.ground_truth_file or not os.path.exists(self.ground_truth_file):
            return {}
        
        try:
            with open(self.ground_truth_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar ground truth: {e}")
            return {}
    
    def test_file(self, midi_file_path, save_visualization=False, output_dir=None):
        """
        Testa a detecção de acordes em um único arquivo MIDI.
        
        Args:
            midi_file_path (str): Caminho para o arquivo MIDI
            save_visualization (bool): Se deve salvar visualizações dos resultados
            output_dir (str, optional): Diretório para salvar visualizações
            
        Returns:
            dict: Resultados do teste
        """
        try:
            # Extrair acordes usando o extrator fornecido
            detected_chords = self.extractor.extract_chords(midi_file_path)
            
            # Obter o nome do arquivo sem o caminho
            file_name = os.path.basename(midi_file_path)
            
            # Verificar se temos ground truth para este arquivo
            ground_truth_chords = self.ground_truth.get(file_name, [])
            
            # Calcular métricas
            metrics = self._calculate_metrics(detected_chords, ground_truth_chords)
            
            # Salvar resultados
            result = {
                'file_name': file_name,
                'detected_chords': detected_chords,
                'ground_truth_chords': ground_truth_chords,
                'metrics': metrics
            }
            
            self.results[file_name] = result
            
            # Criar visualizações se solicitado
            if save_visualization:
                self._create_visualizations(result, output_dir)
            
            return result
            
        except Exception as e:
            print(f"Erro ao testar arquivo {midi_file_path}: {e}")
            return {
                'file_name': os.path.basename(midi_file_path),
                'error': str(e)
            }
    
    def test_directory(self, save_visualization=False, output_dir=None):
        """
        Testa a detecção de acordes em todos os arquivos MIDI no diretório de teste.
        
        Args:
            save_visualization (bool): Se deve salvar visualizações dos resultados
            output_dir (str, optional): Diretório para salvar visualizações
            
        Returns:
            dict: Resultados agregados dos testes
        """
        if not self.test_files_dir or not os.path.exists(self.test_files_dir):
            print("Diretório de teste não especificado ou não existe.")
            return {}
        
        # Limpar resultados anteriores
        self.results = {}
        
        # Encontrar todos os arquivos MIDI no diretório
        midi_files = []
        for root, _, files in os.walk(self.test_files_dir):
            for file in files:
                if file.lower().endswith(('.mid', '.midi', '.kar')):
                    midi_files.append(os.path.join(root, file))
        
        # Testar cada arquivo
        for midi_file in midi_files:
            self.test_file(midi_file, save_visualization, output_dir)
        
        # Calcular métricas agregadas
        return self._aggregate_results()
    
    def _calculate_metrics(self, detected_chords, ground_truth_chords):
        """
        Calcula métricas de precisão para os acordes detectados.
        
        Args:
            detected_chords (list): Acordes detectados pelo extrator
            ground_truth_chords (list): Acordes corretos para comparação
            
        Returns:
            dict: Métricas calculadas
        """
        # Se não temos ground truth, não podemos calcular métricas
        if not ground_truth_chords:
            return {
                'precision': None,
                'recall': None,
                'f1_score': None,
                'accuracy': None,
                'error_rate': None,
                'confidence': sum(chord.get('confidence', 0) for chord in detected_chords) / len(detected_chords) if detected_chords else 0
            }
        
        # Simplificar para comparação (apenas nomes de acordes)
        detected_names = [chord['name'] for chord in detected_chords if 'name' in chord]
        ground_truth_names = [chord['name'] for chord in ground_truth_chords if 'name' in chord]
        
        # Calcular verdadeiros positivos, falsos positivos e falsos negativos
        true_positives = sum(1 for chord in detected_names if chord in ground_truth_names)
        false_positives = len(detected_names) - true_positives
        false_negatives = len(ground_truth_names) - true_positives
        
        # Calcular métricas
        precision = true_positives / len(detected_names) if detected_names else 0
        recall = true_positives / len(ground_truth_names) if ground_truth_names else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = true_positives / (true_positives + false_positives + false_negatives) if (true_positives + false_positives + false_negatives) > 0 else 0
        error_rate = 1 - accuracy
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'error_rate': error_rate,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'confidence': sum(chord.get('confidence', 0) for chord in detected_chords) / len(detected_chords) if detected_chords else 0
        }
    
    def _aggregate_results(self):
        """
        Agrega os resultados de todos os testes.
        
        Returns:
            dict: Resultados agregados
        """
        if not self.results:
            return {}
        
        # Filtrar resultados com métricas
        valid_results = [r for r in self.results.values() if 'metrics' in r and r['metrics'].get('precision') is not None]
        
        if not valid_results:
            return {
                'average_precision': None,
                'average_recall': None,
                'average_f1_score': None,
                'average_accuracy': None,
                'average_error_rate': None,
                'average_confidence': None,
                'file_count': len(self.results),
                'valid_file_count': 0
            }
        
        # Calcular médias
        avg_precision = sum(r['metrics']['precision'] for r in valid_results) / len(valid_results)
        avg_recall = sum(r['metrics']['recall'] for r in valid_results) / len(valid_results)
        avg_f1_score = sum(r['metrics']['f1_score'] for r in valid_results) / len(valid_results)
        avg_accuracy = sum(r['metrics']['accuracy'] for r in valid_results) / len(valid_results)
        avg_error_rate = sum(r['metrics']['error_rate'] for r in valid_results) / len(valid_results)
        avg_confidence = sum(r['metrics']['confidence'] for r in valid_results) / len(valid_results)
        
        return {
            'average_precision': avg_precision,
            'average_recall': avg_recall,
            'average_f1_score': avg_f1_score,
            'average_accuracy': avg_accuracy,
            'average_error_rate': avg_error_rate,
            'average_confidence': avg_confidence,
            'file_count': len(self.results),
            'valid_file_count': len(valid_results)
        }
    
    def _create_visualizations(self, result, output_dir=None):
        """
        Cria visualizações dos resultados do teste.
        
        Args:
            result (dict): Resultado do teste para um arquivo
            output_dir (str, optional): Diretório para salvar visualizações
        """
        if not output_dir:
            output_dir = tempfile.gettempdir()
        
        os.makedirs(output_dir, exist_ok=True)
        
        file_name = result['file_name'].replace('.mid', '').replace('.midi', '').replace('.kar', '')
        
        # Visualização de acordes detectados vs. ground truth
        self._visualize_chord_comparison(result, os.path.join(output_dir, f"{file_name}_chord_comparison.png"))
        
        # Visualização de métricas
        self._visualize_metrics(result, os.path.join(output_dir, f"{file_name}_metrics.png"))
        
        # Visualização de confiança
        self._visualize_confidence(result, os.path.join(output_dir, f"{file_name}_confidence.png"))
    
    def _visualize_chord_comparison(self, result, output_path):
        """
        Cria uma visualização comparando acordes detectados e ground truth.
        
        Args:
            result (dict): Resultado do teste para um arquivo
            output_path (str): Caminho para salvar a visualização
        """
        detected_chords = result['detected_chords']
        ground_truth_chords = result['ground_truth_chords']
        
        # Se não temos ground truth, apenas visualizar os acordes detectados
        if not ground_truth_chords:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Extrair tempos e nomes dos acordes detectados
            times = [chord['start'] for chord in detected_chords if 'start' in chord]
            names = [chord['name'] for chord in detected_chords if 'name' in chord]
            
            # Plotar acordes detectados
            ax.scatter(times, [1] * len(times), marker='|', s=100, color='#ff8c00', label='Acordes Detectados')
            
            # Adicionar rótulos
            for i, (time, name) in enumerate(zip(times, names)):
                ax.annotate(name, (time, 1), xytext=(0, 10), 
                           textcoords='offset points', ha='center', va='bottom',
                           rotation=45, fontsize=8, color='white')
            
            ax.set_yticks([])
            ax.set_xlabel('Tempo (quartos de nota)')
            ax.set_title(f'Acordes Detectados: {result["file_name"]}')
            ax.grid(True, alpha=0.3)
            
            # Definir cores do tema escuro
            ax.set_facecolor('#222')
            fig.patch.set_facecolor('#111')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('#444')
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return
        
        # Visualização com ground truth
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Extrair tempos e nomes dos acordes
        detected_times = [chord['start'] for chord in detected_chords if 'start' in chord]
        detected_names = [chord['name'] for chord in detected_chords if 'name' in chord]
        
        ground_truth_times = [chord['start'] for chord in ground_truth_chords if 'start' in chord]
        ground_truth_names = [chord['name'] for chord in ground_truth_chords if 'name' in chord]
        
        # Plotar acordes
        ax.scatter(detected_times, [1.2] * len(detected_times), marker='|', s=100, color='#ff8c00', label='Detectados')
        ax.scatter(ground_truth_times, [0.8] * len(ground_truth_times), marker='|', s=100, color='white', label='Ground Truth')
        
        # Adicionar rótulos
        for i, (time, name) in enumerate(zip(detected_times, detected_names)):
            ax.annotate(name, (time, 1.2), xytext=(0, 10), 
                       textcoords='offset points', ha='center', va='bottom',
                       rotation=45, fontsize=8, color='#ff8c00')
        
        for i, (time, name) in enumerate(zip(ground_truth_times, ground_truth_names)):
            ax.annotate(name, (time, 0.8), xytext=(0, -20), 
                       textcoords='offset points', ha='center', va='top',
                       rotation=45, fontsize=8, color='white')
        
        ax.set_yticks([0.8, 1.2])
        ax.set_yticklabels(['Ground Truth', 'Detectados'])
        ax.set_xlabel('Tempo (quartos de nota)')
        ax.set_title(f'Comparação de Acordes: {result["file_name"]}')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Definir cores do tema escuro
        ax.set_facecolor('#222')
        fig.patch.set_facecolor('#111')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#444')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _visualize_metrics(self, result, output_path):
        """
        Cria uma visualização das métricas de precisão.
        
        Args:
            result (dict): Resultado do teste para um arquivo
            output_path (str): Caminho para salvar a visualização
        """
        metrics = result['metrics']
        
        # Se não temos métricas válidas, pular
        if metrics.get('precision') is None:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Métricas a serem plotadas
        metric_names = ['Precisão', 'Recall', 'F1-Score', 'Acurácia']
        metric_values = [metrics['precision'], metrics['recall'], metrics['f1_score'], metrics['accuracy']]
        
        # Criar barras
        bars = ax.bar(metric_names, metric_values, color='#ff8c00')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom',
                       color='white')
        
        ax.set_ylim(0, 1.1)
        ax.set_ylabel('Valor')
        ax.set_title(f'Métricas de Precisão: {result["file_name"]}')
        
        # Definir cores do tema escuro
        ax.set_facecolor('#222')
        fig.patch.set_facecolor('#111')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#444')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _visualize_confidence(self, result, output_path):
        """
        Cria uma visualização da confiança dos acordes detectados.
        
        Args:
        
(Content truncated due to size limit. Use line ranges to read in chunks)
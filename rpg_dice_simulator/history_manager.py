"""
Gerenciador de histórico de rolagens.

Este módulo gerencia o histórico de todas as rolagens realizadas,
permitindo visualização e exportação dos dados.
"""

from typing import Dict, List
from datetime import datetime
import json


class RollHistory:
    """Gerencia o histórico de rolagens de dados."""
    
    def __init__(self):
        """Inicializa o histórico vazio."""
        self.history: List[Dict] = []
    
    def add_roll(self, roll_data: Dict) -> None:
        """
        Adiciona uma rolagem ao histórico.
        
        Args:
            roll_data: Dicionário com os dados da rolagem
        """
        self.history.append(roll_data)
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Retorna o histórico de rolagens (mais recentes primeiro).
        
        Args:
            limit: Número máximo de rolagens a retornar
            
        Returns:
            Lista com as últimas rolagens
        """
        return self.history[-limit:][::-1]  # Últimas N rolagens, invertidas
    
    def get_all_history(self) -> List[Dict]:
        """
        Retorna todo o histórico de rolagens.
        
        Returns:
            Lista completa do histórico
        """
        return self.history[::-1]  # Histórico completo invertido
    
    def clear_history(self) -> None:
        """Limpa todo o histórico."""
        self.history.clear()
    
    def get_statistics(self) -> Dict:
        """
        Calcula estatísticas do histórico de rolagens.
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.history:
            return {
                'total_rolls': 0,
                'dice_usage': {},
                'average_total': 0,
                'max_roll': 0,
                'min_roll': 0
            }
        
        dice_usage = {}
        totals = []
        
        for roll in self.history:
            dice_type = roll.get('dice_type', 'UNKNOWN')
            dice_usage[dice_type] = dice_usage.get(dice_type, 0) + 1
            totals.append(roll.get('total', 0))
        
        return {
            'total_rolls': len(self.history),
            'dice_usage': dice_usage,
            'average_total': sum(totals) / len(totals) if totals else 0,
            'max_roll': max(totals) if totals else 0,
            'min_roll': min(totals) if totals else 0
        }
    
    def export_to_file(self, filename: str) -> None:
        """
        Exporta o histórico para um arquivo JSON.
        
        Args:
            filename: Nome do arquivo de destino
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'exported_at': datetime.now().isoformat(),
                    'total_rolls': len(self.history),
                    'rolls': self.history
                }, f, ensure_ascii=False, indent=2)
            print(f"✅ Histórico exportado para: {filename}")
        except Exception as e:
            print(f"❌ Erro ao exportar histórico: {e}")
    
    def import_from_file(self, filename: str) -> bool:
        """
        Importa histórico de um arquivo JSON.
        
        Args:
            filename: Nome do arquivo a importar
            
        Returns:
            True se importação bem-sucedida, False caso contrário
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'rolls' in data:
                    self.history.extend(data['rolls'])
                    print(f"✅ Histórico importado: {len(data['rolls'])} rolagens")
                    return True
                else:
                    print("❌ Arquivo não contém dados de rolagens válidos")
                    return False
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filename}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Erro ao ler arquivo JSON: {filename}")
            return False
        except Exception as e:
            print(f"❌ Erro ao importar histórico: {e}")
            return False

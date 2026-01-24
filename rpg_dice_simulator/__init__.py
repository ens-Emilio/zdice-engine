# Pacote do Simulador de Dados RPG
"""
Simulador de Dados RPG

Um simulador completo de dados para jogos de RPG com suporte a:
- Todos os tipos de dados padrão (D4, D6, D8, D10, D12, D20, D100)
- Vantagem/Desvantagem (D&D 5e)
- Explosão de dados
- Histórico e estatísticas
- Exportação/Importação de dados
- Configurações salvas persistentes
- Parser de notação padrão
"""

__version__ = "2.0.0"
__author__ = "ZenSemilio"
__license__ = "MIT"

from .dice_engine import Dice, DiceRoller
from .history_manager import RollHistory
from .config_manager import SavedConfigurations
from .dice_parser import DiceNotationParser

__all__ = ['Dice', 'DiceRoller', 'RollHistory', 'SavedConfigurations', 'DiceNotationParser']

"""
Motor de rolagem de dados para RPG.

Este módulo contém as classes principais para rolagem de dados:
- Dice: Representa um dado individual
- DiceRoller: Gerencia múltiplos tipos de dados e rolagens complexas
"""

import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class Dice:
    """Representa um dado individual com um número específico de faces."""
    
    def __init__(self, sides: int):
        """
        Inicializa um dado.
        
        Args:
            sides: Número de faces do dado (4, 6, 8, 10, 12, 20, 100)
        """
        if sides not in [4, 6, 8, 10, 12, 20, 100]:
            raise ValueError(f"Número de lados inválido: {sides}. Use 4, 6, 8, 10, 12, 20 ou 100.")
        self.sides = sides
    
    def roll(self) -> int:
        """
        Rola um único dado.
        
        Returns:
            Resultado da rolagem (1 até self.sides)
        """
        return random.randint(1, self.sides)
    
    def roll_multiple(self, quantity: int, explode: bool = False, 
                     advantage: bool = False, disadvantage: bool = False) -> List[int]:
        """
        Rola múltiplos dados com opções especiais.
        
        Args:
            quantity: Número de dados a rolar
            explode: Se True, rola novamente quando sair o valor máximo
            advantage: Se True (apenas D20), rola 2 dados e pega o maior
            disadvantage: Se True (apenas D20), rola 2 dados e pega o menor
            
        Returns:
            Lista com os resultados de cada rolagem
        """
        if quantity < 1:
            raise ValueError("Quantidade deve ser maior que zero.")
        
        # Vantagem/Desvantagem só funciona com D20 e quantidade 1
        if (advantage or disadvantage) and self.sides == 20 and quantity == 1:
            roll1 = self.roll()
            roll2 = self.roll()
            if advantage:
                return [max(roll1, roll2), roll1, roll2]  # Retorna melhor resultado + ambas rolagens
            else:
                return [min(roll1, roll2), roll1, roll2]  # Retorna pior resultado + ambas rolagens
        
        results = []
        for _ in range(quantity):
            result = self.roll()
            results.append(result)
            
            # Explosão de dados (limitado a 10 explosões para evitar loops infinitos)
            if explode:
                explosion_count = 0
                while result == self.sides and explosion_count < 10:
                    result = self.roll()
                    results.append(result)
                    explosion_count += 1
        
        return results


class DiceRoller:
    """Gerencia múltiplos tipos de dados e rolagens complexas."""
    
    def __init__(self):
        """Inicializa o roller com todos os tipos de dados disponíveis."""
        self.dice_types = {
            'D4': Dice(4),
            'D6': Dice(6),
            'D8': Dice(8),
            'D10': Dice(10),
            'D12': Dice(12),
            'D20': Dice(20),
            'D100': Dice(100)
        }
    
    def roll(self, dice_type: str, quantity: int = 1, modifier: int = 0,
             explode: bool = False, advantage: bool = False, 
             disadvantage: bool = False) -> Dict:
        """
        Método principal para rolagem de dados.
        
        Args:
            dice_type: Tipo de dado (D4, D6, D8, D10, D12, D20, D100)
            quantity: Quantidade de dados a rolar
            modifier: Modificador a adicionar ao total (+/-)
            explode: Se True, dados com valor máximo rolam novamente
            advantage: Se True (D20), rola 2 e pega o melhor
            disadvantage: Se True (D20), rola 2 e pega o pior
            
        Returns:
            Dicionário com informações detalhadas da rolagem
        """
        dice_type = dice_type.upper()
        
        if dice_type not in self.dice_types:
            raise ValueError(f"Tipo de dado inválido: {dice_type}")
        
        if advantage and disadvantage:
            raise ValueError("Não é possível ter vantagem e desvantagem ao mesmo tempo.")
        
        dice = self.dice_types[dice_type]
        rolls = dice.roll_multiple(quantity, explode, advantage, disadvantage)
        
        # Para vantagem/desvantagem, o primeiro elemento é o resultado usado
        if (advantage or disadvantage) and dice_type == 'D20':
            used_roll = rolls[0]
            all_rolls = rolls[1:]  # Rolls[1] e rolls[2] são as rolagens originais
            total = used_roll + modifier
        else:
            all_rolls = rolls
            total = sum(rolls) + modifier
        
        return {
            'dice_type': dice_type,
            'quantity': quantity,
            'rolls': all_rolls,
            'modifier': modifier,
            'total': total,
            'explode': explode,
            'advantage': advantage,
            'disadvantage': disadvantage,
            'timestamp': datetime.now().isoformat()
        }
    
    def roll_d100_special(self) -> Dict:
        """
        Trata D100 como dois dados D10 (dezenas e unidades).
        
        Returns:
            Dicionário com informações da rolagem D100 especial
        """
        d10_tens = Dice(10)
        d10_units = Dice(10)
        
        tens = d10_tens.roll()
        units = d10_units.roll()
        
        # Converte para formato D100 (00-99, onde 00 = 100)
        if tens == 10 and units == 10:
            total = 100
        else:
            total = ((tens % 10) * 10) + (units % 10)
            if total == 0:
                total = 100
        
        return {
            'dice_type': 'D100_SPECIAL',
            'quantity': 1,
            'rolls': [tens, units],
            'tens_die': tens,
            'units_die': units,
            'modifier': 0,
            'total': total,
            'explode': False,
            'advantage': False,
            'disadvantage': False,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_available_dice(self) -> List[str]:
        """
        Retorna lista de tipos de dados disponíveis.
        
        Returns:
            Lista com nomes dos tipos de dados
        """
        return list(self.dice_types.keys())

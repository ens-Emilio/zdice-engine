"""
Parser de notação padrão de dados de RPG.

Este módulo converte notação comum de RPG (ex: "2d6+3", "1d20a")
em parâmetros que podem ser usados pelo DiceRoller.
"""

import re
from typing import Dict, Optional, Tuple


class DiceNotationParser:
    """Parser para notação padrão de dados de RPG."""
    
    # Tipos de dados válidos
    VALID_DICE_TYPES = [4, 6, 8, 10, 12, 20, 100]
    
    # Padrão regex para notação de dados
    # Formato: <quantidade>d<faces>[a|d|!][+|-<modificador>]*
    # Exemplos: 2d6, 1d20+5, 3d8-2, 1d20a, 2d6!, 1d20+5+2
    DICE_PATTERN = re.compile(
        r'^(\d+)d(\d+)([ad!]?)([+\-\d]+)?$',
        re.IGNORECASE
    )
    
    def __init__(self):
        """Inicializa o parser."""
        pass
    
    def parse(self, notation: str) -> Optional[Dict]:
        """
        Converte notação de dados em parâmetros para DiceRoller.
        
        Args:
            notation: String com notação de dados (ex: "2d6+3", "1d20a")
            
        Returns:
            Dicionário com parâmetros ou None se inválido
            
        Formato do retorno:
        {
            'dice_type': 'D20',
            'quantity': 1,
            'modifier': 5,
            'advantage': False,
            'disadvantage': False,
            'explode': False
        }
        """
        # Remove espaços em branco
        notation = notation.strip().replace(' ', '')
        
        if not notation:
            print("❌ Notação vazia.")
            return None
        
        # Tenta fazer o match com o padrão
        match = self.DICE_PATTERN.match(notation)
        
        if not match:
            print(f"❌ Notação inválida: '{notation}'")
            print("   Formato esperado: <qtd>d<faces>[a|d|!][+|-<mod>]")
            print("   Exemplos: 2d6, 1d20+5, 1d20a, 3d8!")
            return None
        
        # Extrai componentes
        quantity_str, faces_str, special, modifiers_str = match.groups()
        
        # Valida e converte quantidade
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                print("❌ Quantidade deve ser maior que zero.")
                return None
            if quantity > 100:
                print("❌ Quantidade muito alta (máximo: 100).")
                return None
        except ValueError:
            print(f"❌ Quantidade inválida: '{quantity_str}'")
            return None
        
        # Valida e converte faces
        try:
            faces = int(faces_str)
            if faces not in self.VALID_DICE_TYPES:
                print(f"❌ Tipo de dado inválido: D{faces}")
                print(f"   Válidos: D{', D'.join(map(str, self.VALID_DICE_TYPES))}")
                return None
        except ValueError:
            print(f"❌ Número de faces inválido: '{faces_str}'")
            return None
        
        # Processa modificadores especiais
        advantage = False
        disadvantage = False
        explode = False
        
        if special:
            special = special.lower()
            if special == 'a':
                advantage = True
                if faces != 20:
                    print("⚠️  Vantagem (a) só funciona com D20, ignorando...")
                    advantage = False
                if quantity != 1:
                    print("⚠️  Vantagem requer quantidade = 1, ajustando...")
                    quantity = 1
            elif special == 'd':
                disadvantage = True
                if faces != 20:
                    print("⚠️  Desvantagem (d) só funciona com D20, ignorando...")
                    disadvantage = False
                if quantity != 1:
                    print("⚠️  Desvantagem requer quantidade = 1, ajustando...")
                    quantity = 1
            elif special == '!':
                explode = True
        
        # Processa modificadores numéricos
        modifier = 0
        if modifiers_str:
            # Adiciona espaços antes de + e - para facilitar split
            modifiers_str = modifiers_str.replace('+', ' +').replace('-', ' -')
            parts = modifiers_str.split()
            
            for part in parts:
                try:
                    modifier += int(part)
                except ValueError:
                    print(f"⚠️  Modificador inválido ignorado: '{part}'")
        
        # Valida modificador total
        if modifier < -1000 or modifier > 1000:
            print("⚠️  Modificador muito extremo, limitando a ±1000")
            modifier = max(-1000, min(1000, modifier))
        
        # Monta resultado
        result = {
            'dice_type': f'D{faces}',
            'quantity': quantity,
            'modifier': modifier,
            'advantage': advantage,
            'disadvantage': disadvantage,
            'explode': explode,
            'original_notation': notation
        }
        
        return result
    
    def validate_notation(self, notation: str) -> bool:
        """
        Valida se uma notação é válida sem fazer parse completo.
        
        Args:
            notation: Notação a validar
            
        Returns:
            True se válida, False caso contrário
        """
        return self.parse(notation) is not None
    
    def get_notation_examples(self) -> list[str]:
        """
        Retorna exemplos de notações válidas.
        
        Returns:
            Lista de exemplos
        """
        return [
            "2d6        # 2 dados de 6 faces",
            "1d20+5     # 1 dado de 20 faces +5",
            "3d8-2      # 3 dados de 8 faces -2",
            "1d20a      # D20 com vantagem",
            "1d20d      # D20 com desvantagem",
            "2d6!       # 2D6 com explosão",
            "1d20+5+2   # D20 +7 (soma modificadores)",
            "4d6        # 4 dados de 6 faces (atributos D&D)"
        ]
    
    def parse_and_describe(self, notation: str) -> str:
        """
        Faz parse e retorna descrição legível.
        
        Args:
            notation: Notação a processar
            
        Returns:
            Descrição em português ou mensagem de erro
        """
        result = self.parse(notation)
        
        if not result:
            return "Notação inválida"
        
        # Monta descrição
        desc = f"{result['quantity']}{result['dice_type']}"
        
        # Modificador
        if result['modifier'] > 0:
            desc += f" +{result['modifier']}"
        elif result['modifier'] < 0:
            desc += f" {result['modifier']}"
        
        # Especiais
        extras = []
        if result['advantage']:
            extras.append("VANTAGEM")
        if result['disadvantage']:
            extras.append("DESVANTAGEM")
        if result['explode']:
            extras.append("EXPLOSÃO")
        
        if extras:
            desc += f" ({', '.join(extras)})"
        
        return desc
    
    @staticmethod
    def notation_to_readable(dice_type: str, quantity: int, modifier: int = 0,
                            advantage: bool = False, disadvantage: bool = False,
                            explode: bool = False) -> str:
        """
        Converte parâmetros de volta para notação.
        
        Args:
            dice_type: Tipo de dado (ex: 'D20')
            quantity: Quantidade de dados
            modifier: Modificador
            advantage: Vantagem?
            disadvantage: Desvantagem?
            explode: Explosão?
            
        Returns:
            String com notação
        """
        # Remove o 'D' para pegar apenas o número
        faces = dice_type[1:] if dice_type.startswith('D') else dice_type
        
        notation = f"{quantity}d{faces}"
        
        # Especiais
        if advantage:
            notation += "a"
        elif disadvantage:
            notation += "d"
        elif explode:
            notation += "!"
        
        # Modificador
        if modifier > 0:
            notation += f"+{modifier}"
        elif modifier < 0:
            notation += str(modifier)
        
        return notation

#!/usr/bin/env python3
"""
Script de demonstração do Simulador de Dados RPG.
Executa vários exemplos de rolagens para demonstrar as funcionalidades.
"""

import sys
import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpg_dice_simulator.dice_engine import DiceRoller
from history_manager import RollHistory
from utils import format_roll_result

def main():
    print("=" * 70)
    print("🎲 DEMONSTRAÇÃO DO SIMULADOR DE DADOS RPG")
    print("=" * 70)
    print()
    
    roller = DiceRoller()
    history = RollHistory()
    
    # Exemplo 1: Rolagem simples D20
    print("📌 Exemplo 1: Rolagem simples de D20")
    result = roller.roll('D20', quantity=1, modifier=0)
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Exemplo 2: Múltiplos dados com modificador
    print("\n📌 Exemplo 2: 3D6 + 5 (ataque comum)")
    result = roller.roll('D6', quantity=3, modifier=5)
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Exemplo 3: Vantagem (D&D 5e)
    print("\n📌 Exemplo 3: D20 com VANTAGEM")
    result = roller.roll('D20', quantity=1, advantage=True)
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Exemplo 4: Desvantagem (D&D 5e)
    print("\n📌 Exemplo 4: D20 com DESVANTAGEM")
    result = roller.roll('D20', quantity=1, disadvantage=True)
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Exemplo 5: D100 Especial
    print("\n📌 Exemplo 5: D100 Especial (2xD10)")
    result = roller.roll_d100_special()
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Exemplo 6: Explosão de dados
    print("\n📌 Exemplo 6: 2D6 com EXPLOSÃO")
    result = roller.roll('D6', quantity=2, explode=True)
    history.add_roll(result)
    print(format_roll_result(result))
    
    # Estatísticas
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS DAS ROLAGENS")
    print("=" * 70)
    stats = history.get_statistics()
    print(f"Total de rolagens: {stats['total_rolls']}")
    print(f"Média dos totais: {stats['average_total']:.2f}")
    print(f"Maior total: {stats['max_roll']}")
    print(f"Menor total: {stats['min_roll']}")
    
    print("\n✅ Demonstração concluída!")
    print("=" * 70)
    print("\n💡 Para usar o simulador interativo, execute:")
    print("   cd rpg_dice_simulator && python main.py")
    print()

if __name__ == "__main__":
    main()

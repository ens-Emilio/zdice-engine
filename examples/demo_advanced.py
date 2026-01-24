#!/usr/bin/env python3
"""
Demonstração das funcionalidades da Fase 2 do Simulador de Dados RPG.
"""

import sys
import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpg_dice_simulator.dice_parser import DiceNotationParser
from rpg_dice_simulator.config_manager import SavedConfigurations
from rpg_dice_simulator.dice_engine import DiceRoller

def main():
    print("=" * 70)
    print("🎉 DEMONSTRAÇÃO FASE 2 - FUNCIONALIDADES AVANÇADAS")
    print("=" * 70)
    print()
    
    # 1. Parser de Notação
    print("📝 1. PARSER DE NOTAÇÃO")
    print("-" * 70)
    parser = DiceNotationParser()
    
    test_notations = [
        "2d6+3",
        "1d20a",
        "3d8!",
        "1d20+5+2",
    ]
    
    for notation in test_notations:
        result = parser.parse(notation)
        desc = parser.parse_and_describe(notation)
        print(f"  {notation:15s} → {desc}")
    
    print()
    
    # 2. Configurações Salvas
    print("💾 2. CONFIGURAÇÕES SALVAS")
    print("-" * 70)
    configs = SavedConfigurations("demo_configs.json")
    
    # Salva algumas configurações de exemplo
    configs.save_config("Ataque Básico", "1d20+5")
    configs.save_config("Dano Espada", "1d8+3")
    configs.save_config("Furtividade", "1d20+7")
    
    print(f"  Configurações salvas: {configs.get_config_count()}")
    for name, notation in configs.list_configs().items():
        print(f"    • {name}: {notation}")
    
    print()
    
    # 3. Integração Completa: Config → Parser → Roller
    print("🎲 3. INTEGRAÇÃO COMPLETA")
    print("-" * 70)
    roller = DiceRoller()
    
    # Usa uma configuração salva
    notation = configs.load_config("Ataque Básico")
    params = parser.parse(notation)
    result = roller.roll(**params)
    
    print(f"  Configuração: Ataque Básico")
    print(f"  Notação: {notation}")
    print(f"  Rolagem: {result['dice_type']} x{result['quantity']} +{result['modifier']}")
    print(f"  Resultado Individual: {result['rolls']}")
    print(f"  ➜ TOTAL: {result['total']}")
    
    print()
    
    # 4. Teste de Notações Avançadas
    print("⚡ 4. NOTAÇÕES AVANÇADAS")
    print("-" * 70)
    
    advanced = [
        ("Vantagem", "1d20a"),
        ("Desvantagem", "1d20d"),
        ("Explosão", "2d6!"),
        ("Múltiplos Mods", "1d20+5+3-2"),
    ]
    
    for name, notation in advanced:
        params = parser.parse(notation)
        result = roller.roll(**params)
        print(f"  {name:15s}: {notation:12s} → Total: {result['total']:3d}")
    
    print()
    print("=" * 70)
    print("✅ FASE 2 COMPLETA E FUNCIONAL!")
    print("=" * 70)
    print()
    print("💡 Para usar o sistema completo, execute:")
    print("   cd rpg_dice_simulator && python main.py")
    print()
    
    # Limpeza
    import os
    if os.path.exists("demo_configs.json"):
        os.remove("demo_configs.json")

if __name__ == "__main__":
    main()

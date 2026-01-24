#!/usr/bin/env python3
"""
Demonstração completa do Simulador de Dados RPG - Todas as Fases.
"""

import sys
import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("=" * 70)
print("🎉 SIMULADOR DE DADOS RPG - DEMONSTRAÇÃO COMPLETA")
print("=" * 70)
print()

# Fase 1 - MVP
print("✅ FASE 1 - MVP")
print("  • Motor de rolagem (dice_engine.py)")
print("  • Histórico (history_manager.py)")
print("  • Interface CLI básica")
print()

# Fase 2 - Funcionalidades Avançadas  
print("✅ FASE 2 - FUNCIONALIDADES AVANÇADAS")
print("  • Parser de notação (2d6+3, 1d20a)")
print("  • Configurações salvas (config_manager.py)")
print("  • CLI expandida com 9 opções")
print()

# Fase 3 - Temas
print("✅ FASE 3 - TEMAS E UX")
from rpg_dice_simulator.themes import ThemeManager, THEMES
from rpg_dice_simulator.user_settings import UserSettings

tm = ThemeManager()
print(f"  • Sistema de temas: {len(THEMES)} temas disponíveis")
print(f"    Temas: {', '.join(THEMES.keys())}")

settings = UserSettings("demo_settings.json")
print(f"  • Configurações de usuário persistentes")
print(f"    Tema atual: {settings.get_theme()}")
print()

# Fase 4 - GUI
print("✅ FASE 4 - INTERFACE GRÁFICA")
print("  • GUI completa com Tkinter")
print("  • Botões para todos os dados (D4-D100)")
print("  • Opções: Vantagem, Desvantagem, Explosão")
print("  • Três abas: Resultado, Histórico, Configurações")
print("  • Menu com Export/Import")
print("  • Configurações salvas integradas")
print()

print("=" * 70)
print("📁 ESTRUTURA DO PROJETO")
print("=" * 70)
print("""
zdice-engine/
├── README.md
├── main_gui.py                    # GUI Tkinter
├── demo.py                        # Demo Fase 1
├── demo_phase2.py                 # Demo Fase 2
├── demo_complete.py               # Esta demo
├── test_dice_simulator.py         # Testes Fase 1
├── test_phase2.py                 # Testes Fase 2
└── rpg_dice_simulator/
    ├── __init__.py
    ├── main.py                    # CLI
    ├── dice_engine.py             # ✅ Fase 1
    ├── history_manager.py         # ✅ Fase 1
    ├── utils.py                   # ✅ Fase 1
    ├── config_manager.py          # ✅ Fase 2
    ├── dice_parser.py             # ✅ Fase 2
    ├── themes.py                  # ✅ Fase 3
    ├── user_settings.py           # ✅ Fase 3
    ├── ui/
    │   ├── __init__.py
    │   └── cli_interface.py       # ✅ CLI completa
    └── gui/
        ├── __init__.py
        └── gui_interface.py       # ✅ GUI Tkinter
""")

print("=" * 70)
print("🚀 COMO EXECUTAR")
print("=" * 70)
print()
print("CLI (Terminal):")
print("  cd rpg_dice_simulator")
print("  python main.py")
print()
print("GUI (Interface Gráfica):")
print("  python main_gui.py")
print()

print("=" * 70)
print("📊 ESTATÍSTICAS DO PROJETO")
print("=" * 70)

import os

def count_lines(filepath):
    try:
        with open(filepath, 'r') as f:
            return len(f.readlines())
    except:
        return 0

files = {
    "dice_engine.py": "rpg_dice_simulator/dice_engine.py",
    "history_manager.py": "rpg_dice_simulator/history_manager.py",
    "utils.py": "rpg_dice_simulator/utils.py",
    "config_manager.py": "rpg_dice_simulator/config_manager.py",
    "dice_parser.py": "rpg_dice_simulator/dice_parser.py",
    "themes.py": "rpg_dice_simulator/themes.py",
    "user_settings.py": "rpg_dice_simulator/user_settings.py",
    "cli_interface.py": "rpg_dice_simulator/ui/cli_interface.py",
    "gui_interface.py": "rpg_dice_simulator/gui/gui_interface.py",
}

total_lines = 0
print("\nLinhas de código por módulo:")
for name, path in files.items():
    lines = count_lines(path)
    total_lines += lines
    print(f"  {name:<25s}: {lines:>4d} linhas")

print(f"\n  {'TOTAL':<25s}: {total_lines:>4d} linhas")

print()
print("=" * 70)
print("✨ PROJETO COMPLETO - TODAS AS 4 FASES IMPLEMENTADAS!")
print("=" * 70)
print()

# Limpeza
import os
if os.path.exists("demo_settings.json"):
    os.remove("demo_settings.json")

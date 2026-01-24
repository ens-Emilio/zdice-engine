#!/usr/bin/env python3
"""
Ponto de entrada GUI para o Simulador de Dados RPG.

Executa a interface gráfica com Tkinter.

Uso:
    python main_gui.py
"""

import sys
import os

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rpg_dice_simulator.gui.gui_interface import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

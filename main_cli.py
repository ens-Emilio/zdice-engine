"""
Simulador de Dados RPG - Ponto de Entrada Principal

Este é o arquivo principal para executar o simulador de dados RPG.
Executa a interface CLI por padrão.

Uso:
    python main.py
"""

import sys
import os

# Adiciona o diretório pai ao path para permitir imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rpg_dice_simulator.ui.cli_interface import main as cli_main


def main():
    """Ponto de entrada principal da aplicação."""
    print("🎲 Iniciando Simulador de Dados RPG...\n")
    cli_main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)

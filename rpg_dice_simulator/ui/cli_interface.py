"""
Interface de linha de comando (CLI) para o simulador de dados RPG.
"""

import sys
from typing import Optional
from ..dice_engine import DiceRoller
from ..history_manager import RollHistory
from ..config_manager import SavedConfigurations
from ..dice_parser import DiceNotationParser
from ..utils import (
    format_roll_result, format_history, format_statistics, format_saved_configs,
    validate_integer_input, clear_screen
)


class CLIInterface:
    """Interface de linha de comando para o simulador de dados."""
    
    def __init__(self):
        """Inicializa a interface CLI."""
        self.roller = DiceRoller()
        self.history = RollHistory()
        self.configs = SavedConfigurations()
        self.parser = DiceNotationParser()
        self.running = True
    
    def show_banner(self):
        """Exibe o banner de boas-vindas."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🎲  SIMULADOR DE DADOS RPG  🎲                      ║
║                                                              ║
║          Bem-vindo ao seu companheiro de mesa!               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def show_menu(self):
        """Exibe o menu principal."""
        menu = """
╔══════════════════════════════════════════════════════════════╗
║                      MENU PRINCIPAL                          ║
╠══════════════════════════════════════════════════════════════╣
║  1. 🎲 Rolar dados                                           ║
║  2. 📜 Ver histórico                                         ║
║  3. 📊 Ver estatísticas                                      ║
║  4. 🧹 Limpar histórico                                      ║
║  5. 💾 Exportar histórico                                    ║
║  6. 📥 Importar histórico                                    ║
║  7. 📝 Gerenciar configurações                               ║
║  8. ⚡ Rolagem rápida (notação)                              ║
║  9. ❌ Sair                                                   ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(menu)
    
    def roll_dice_menu(self):
        """Menu para rolagem de dados."""
        print("\n" + "═" * 60)
        print("🎲 ROLAGEM DE DADOS")
        print("═" * 60)
        
        # Escolher tipo de dado
        print("\nTipos de dados disponíveis:")
        dice_types = self.roller.get_available_dice()
        for i, dice in enumerate(dice_types, 1):
            print(f"  {i}. {dice}")
        print(f"  {len(dice_types) + 1}. D100 Especial (2xD10)")
        
        try:
            choice = validate_integer_input(
                "\nEscolha o tipo de dado (número): ",
                min_value=1,
                max_value=len(dice_types) + 1
            )
        except KeyboardInterrupt:
            return
        
        # D100 Especial
        if choice == len(dice_types) + 1:
            result = self.roller.roll_d100_special()
            self.history.add_roll(result)
            print(format_roll_result(result))
            input("\nPressione Enter para continuar...")
            return
        
        dice_type = dice_types[choice - 1]
        
        # Quantidade de dados
        try:
            quantity = validate_integer_input(
                "\nQuantidade de dados (1-100, padrão=1): ",
                min_value=1,
                max_value=100,
                default=1
            )
        except KeyboardInterrupt:
            return
        
        # Modificador
        try:
            modifier = validate_integer_input(
                "Modificador (+/-): (padrão=0): ",
                min_value=-1000,
                max_value=1000,
                default=0
            )
        except KeyboardInterrupt:
            return
        
        # Opções especiais
        explode = False
        advantage = False
        disadvantage = False
        
        print("\n🔧 Opções especiais:")
        print("  1. Normal (sem opções)")
        print("  2. Explosão de dados (rolar novamente no máximo)")
        if dice_type == 'D20':
            print("  3. Vantagem (rolar 2d20, pegar o melhor)")
            print("  4. Desvantagem (rolar 2d20, pegar o pior)")
        
        try:
            max_options = 4 if dice_type == 'D20' else 2
            option = validate_integer_input(
                "\nEscolha uma opção (número): ",
                min_value=1,
                max_value=max_options,
                default=1
            )
        except KeyboardInterrupt:
            return
        
        if option == 2:
            explode = True
        elif option == 3 and dice_type == 'D20':
            advantage = True
            quantity = 1  # Força quantidade = 1 para vantagem
        elif option == 4 and dice_type == 'D20':
            disadvantage = True
            quantity = 1  # Força quantidade = 1 para desvantagem
        
        # Realizar rolagem
        try:
            result = self.roller.roll(
                dice_type=dice_type,
                quantity=quantity,
                modifier=modifier,
                explode=explode,
                advantage=advantage,
                disadvantage=disadvantage
            )
            self.history.add_roll(result)
            print(format_roll_result(result))
        except Exception as e:
            print(f"\n❌ Erro ao rolar dados: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def show_history_menu(self):
        """Exibe o histórico de rolagens."""
        try:
            limit = validate_integer_input(
                "\nQuantas rolagens exibir? (padrão=10): ",
                min_value=1,
                max_value=1000,
                default=10
            )
        except KeyboardInterrupt:
            return
        
        history = self.history.get_history(limit)
        print(format_history(history, limit))
        input("\nPressione Enter para continuar...")
    
    def show_statistics_menu(self):
        """Exibe estatísticas do histórico."""
        stats = self.history.get_statistics()
        print(format_statistics(stats))
        input("\nPressione Enter para continuar...")
    
    def clear_history_menu(self):
        """Limpa o histórico de rolagens."""
        confirm = input("\n⚠️  Tem certeza que deseja limpar o histórico? (s/N): ").strip().lower()
        if confirm == 's':
            self.history.clear_history()
            print("✅ Histórico limpo com sucesso!")
        else:
            print("❌ Operação cancelada.")
        input("\nPressione Enter para continuar...")
    
    def export_history_menu(self):
        """Exporta o histórico para arquivo."""
        filename = input("\nNome do arquivo (padrão=historico_dados.json): ").strip()
        if not filename:
            filename = "historico_dados.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        self.history.export_to_file(filename)
        input("\nPressione Enter para continuar...")
    
    def import_history_menu(self):
        """Importa histórico de arquivo."""
        filename = input("\nNome do arquivo para importar: ").strip()
        if filename:
            self.history.import_from_file(filename)
        else:
            print("❌ Nome de arquivo não fornecido.")
        input("\nPressione Enter para continuar...")
    

    def manage_configs_menu(self):
        """Menu para gerenciar configurações salvas."""
        while True:
            print("\n" + "═" * 60)
            print("📝 GERENCIAR CONFIGURAÇÕES")
            print("═" * 60)
            print("\n1. Salvar nova configuração")
            print("2. Listar configurações")
            print("3. Usar configuração salva")
            print("4. Excluir configuração")
            print("5. Exportar configurações")
            print("6. Importar configurações")
            print("7. Voltar ao menu principal")
            
            try:
                from utils import validate_integer_input
                choice = validate_integer_input(
                    "\nEscolha uma opção: ",
                    min_value=1,
                    max_value=7
                )
            except KeyboardInterrupt:
                return
            
            if choice == 1:
                self.save_config_menu()
            elif choice == 2:
                self.list_configs_menu()
            elif choice == 3:
                self.use_saved_config_menu()
            elif choice == 4:
                self.delete_config_menu()
            elif choice == 5:
                self.export_configs_menu()
            elif choice == 6:
                self.import_configs_menu()
            elif choice == 7:
                return
    
    
    def save_config_menu(self):
        """Salva uma nova configuração."""
        print("\n" + "═" * 60)
        print("💾 SALVAR CONFIGURAÇÃO")
        print("═" * 60)
        
        name = input("\nNome da configuração (ex: 'Ataque', 'Dano'): ").strip()
        if not name:
            print("❌ Nome não pode ser vazio.")
            input("\nPressione Enter para continuar...")
            return
        
        print("\nExemplos de notação:")
        for example in self.parser.get_notation_examples():
            print(f"  {example}")
        
        notation = input("\nNotação da rolagem (ex: '1d20+5', '2d6'): ").strip()
        if not notation:
            print("❌ Notação não pode ser vazia.")
            input("\nPressione Enter para continuar...")
            return
        
        # Valida a notação
        if self.parser.validate_notation(notation):
            self.configs.save_config(name, notation)
        else:
            print("❌ Notação inválida, não foi salva.")
        
        input("\nPressione Enter para continuar...")
    
    
    def list_configs_menu(self):
        """Lista todas as configurações salvas."""
        from utils import format_saved_configs
        configs = self.configs.list_configs()
        print(format_saved_configs(configs))
        input("\nPressione Enter para continuar...")
    
    
    def use_saved_config_menu(self):
        """Usa uma configuração salva."""
        from utils import format_saved_configs, format_roll_result
        configs = self.configs.list_configs()
        
        if not configs:
            print("\n📝 Nenhuma configuração salva.")
            input("\nPressione Enter para continuar...")
            return
        
        print(format_saved_configs(configs))
        
        name = input("Nome da configuração a usar (ou Enter para cancelar): ").strip()
        if not name:
            return
        
        notation = self.configs.load_config(name)
        if notation:
            # Faz o parse e executa
            params = self.parser.parse(notation)
            if params:
                try:
                    result = self.roller.roll(**params)
                    self.history.add_roll(result)
                    print(f"\n✅ Executando: {name} ({notation})")
                    print(format_roll_result(result))
                except Exception as e:
                    print(f"\n❌ Erro ao executar rolagem: {e}")
        
        input("\nPressione Enter para continuar...")
    
    
    def delete_config_menu(self):
        """Exclui uma configuração salva."""
        from utils import format_saved_configs
        configs = self.configs.list_configs()
        
        if not configs:
            print("\n📝 Nenhuma configuração salva.")
            input("\nPressione Enter para continuar...")
            return
        
        print(format_saved_configs(configs))
        
        name = input("Nome da configuração a excluir (ou Enter para cancelar): ").strip()
        if name:
            confirm = input(f"⚠️  Confirma exclusão de '{name}'? (s/N): ").strip().lower()
            if confirm == 's':
                self.configs.delete_config(name)
        
        input("\nPressione Enter para continuar...")
    
    
    def export_configs_menu(self):
        """Exporta configurações para arquivo."""
        filename = input("\nNome do arquivo (padrão=configs.json): ").strip()
        if not filename:
            filename = "configs.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        self.configs.export_configs(filename)
        input("\nPressione Enter para continuar...")
    
    
    def import_configs_menu(self):
        """Importa configurações de arquivo."""
        filename = input("\nNome do arquivo para importar: ").strip()
        if filename:
            self.configs.import_configs(filename)
        else:
            print("❌ Nome de arquivo não fornecido.")
        input("\nPressione Enter para continuar...")
    
    
    def quick_roll_menu(self):
        """Menu de rolagem rápida usando notação."""
        from utils import format_roll_result
        print("\n" + "═" * 60)
        print("⚡ ROLAGEM RÁPIDA")
        print("═" * 60)
        
        print("\nExemplos de notação:")
        for example in self.parser.get_notation_examples():
            print(f"  {example}")
        
        notation = input("\nDigite a notação (ou Enter para cancelar): ").strip()
        if not notation:
            return
        
        # Faz o parse
        params = self.parser.parse(notation)
        if not params:
            input("\nPressione Enter para continuar...")
            return
        
        # Mostra descrição
        desc = self.parser.parse_and_describe(notation)
        print(f"\n📋 Rolagem: {desc}")
        
        # Executa
        try:
            result = self.roller.roll(**params)
            self.history.add_roll(result)
            print(format_roll_result(result))
        except Exception as e:
            print(f"\n❌ Erro ao executar rolagem: {e}")
        
        input("\nPressione Enter para continuar...")

    def run(self):
        """Loop principal da interface."""
        clear_screen()
        self.show_banner()
        input("Pressione Enter para iniciar...")
        
        while self.running:
            clear_screen()
            self.show_menu()
            
            try:
                choice = validate_integer_input(
                    "\nEscolha uma opção: ",
                    min_value=1,
                    max_value=9
                )
                
                if choice == 1:
                    self.roll_dice_menu()
                elif choice == 2:
                    self.show_history_menu()
                elif choice == 3:
                    self.show_statistics_menu()
                elif choice == 4:
                    self.clear_history_menu()
                elif choice == 5:
                    self.export_history_menu()
                elif choice == 6:
                    self.import_history_menu()
                elif choice == 7:
                    self.manage_configs_menu()
                elif choice == 8:
                    self.quick_roll_menu()
                elif choice == 9:
                    print("\n👋 Até logo, aventureiro! Boas rolagens!\n")
                    self.running = False
                    
            except KeyboardInterrupt:
                print("\n\n👋 Até logo, aventureiro! Boas rolagens!\n")
                self.running = False
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\nPressione Enter para continuar...")


def main():
    """Ponto de entrada da interface CLI."""
    try:
        cli = CLIInterface()
        cli.run()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Testes unitários para o Config Manager e Dice Parser.

Para executar:
    python test_phase2.py
"""

import unittest
import sys
import os
import json

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpg_dice_simulator.config_manager import SavedConfigurations
from rpg_dice_simulator.dice_parser import DiceNotationParser
from rpg_dice_simulator.dice_engine import DiceRoller


class TestConfigManager(unittest.TestCase):
    """Testes para a classe SavedConfigurations."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.test_file = "test_configs.json"
        self.configs = SavedConfigurations(self.test_file)
    
    def tearDown(self):
        """Limpa o ambiente de teste."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_config(self):
        """Testa salvar e carregar configuração."""
        self.configs.save_config("Ataque", "1d20+5")
        notation = self.configs.load_config("Ataque")
        self.assertEqual(notation, "1d20+5")
    
    def test_list_configs(self):
        """Testa listar configurações."""
        self.configs.save_config("Ataque", "1d20+5")
        self.configs.save_config("Dano", "2d6+3")
        configs = self.configs.list_configs()
        self.assertEqual(len(configs), 2)
        self.assertIn("Ataque", configs)
        self.assertIn("Dano", configs)
    
    def test_delete_config(self):
        """Testa excluir configuração."""
        self.configs.save_config("Teste", "1d6")
        self.assertTrue(self.configs.config_exists("Teste"))
        self.configs.delete_config("Teste")
        self.assertFalse(self.configs.config_exists("Teste"))
    
    def test_persistence(self):
        """Testa persistência em arquivo."""
        self.configs.save_config("Persistente", "3d8")
        
        # Cria nova instância
        configs2 = SavedConfigurations(self.test_file)
        notation = configs2.load_config("Persistente")
        self.assertEqual(notation, "3d8")
    
    def test_export_import(self):
        """Testa exportar e importar configurações."""
        export_file = "test_export.json"
        
        try:
            self.configs.save_config("Config1", "1d20")
            self.configs.export_configs(export_file)
            
            # Cria nova instância e importa
            configs2 = SavedConfigurations("test_configs2.json")
            configs2.import_configs(export_file)
            
            notation = configs2.load_config("Config1")
            self.assertEqual(notation, "1d20")
            
        finally:
            if os.path.exists(export_file):
                os.remove(export_file)
            if os.path.exists("test_configs2.json"):
                os.remove("test_configs2.json")


class TestDiceParser(unittest.TestCase):
    """Testes para a classe DiceNotationParser."""
    
    def setUp(self):
        """Configura o parser."""
        self.parser = DiceNotationParser()
    
    def test_basic_notation(self):
        """Testa notação básica."""
        result = self.parser.parse("2d6")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D6')
        self.assertEqual(result['quantity'], 2)
        self.assertEqual(result['modifier'], 0)
    
    def test_notation_with_positive_modifier(self):
        """Testa notação com modificador positivo."""
        result = self.parser.parse("1d20+5")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D20')
        self.assertEqual(result['quantity'], 1)
        self.assertEqual(result['modifier'], 5)
    
    def test_notation_with_negative_modifier(self):
        """Testa notação com modificador negativo."""
        result = self.parser.parse("3d8-2")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D8')
        self.assertEqual(result['quantity'], 3)
        self.assertEqual(result['modifier'], -2)
    
    def test_advantage_notation(self):
        """Testa notação com vantagem."""
        result = self.parser.parse("1d20a")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D20')
        self.assertTrue(result['advantage'])
        self.assertFalse(result['disadvantage'])
    
    def test_disadvantage_notation(self):
        """Testa notação com desvantagem."""
        result = self.parser.parse("1d20d")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D20')
        self.assertTrue(result['disadvantage'])
        self.assertFalse(result['advantage'])
    
    def test_explode_notation(self):
        """Testa notação com explosão."""
        result = self.parser.parse("2d6!")
        self.assertIsNotNone(result)
        self.assertEqual(result['dice_type'], 'D6')
        self.assertEqual(result['quantity'], 2)
        self.assertTrue(result['explode'])
    
    def test_multiple_modifiers(self):
        """Testa modificadores múltiplos."""
        result = self.parser.parse("1d20+5+2")
        self.assertIsNotNone(result)
        self.assertEqual(result['modifier'], 7)
        
        result2 = self.parser.parse("1d20+10-3")
        self.assertIsNotNone(result2)
        self.assertEqual(result2['modifier'], 7)
    
    def test_invalid_notation(self):
        """Testa notação inválida."""
        result = self.parser.parse("d20")  # Sem quantidade
        self.assertIsNone(result)
        
        result2 = self.parser.parse("2d7")  # D7 não existe
        self.assertIsNone(result2)
        
        result3 = self.parser.parse("abc")  # Sintaxe inválida
        self.assertIsNone(result3)
    
    def test_notation_to_readable(self):
        """Testa conversor de parâmetros para notação."""
        notation = DiceNotationParser.notation_to_readable('D20', 1, 5)
        self.assertEqual(notation, "1d20+5")
        
        notation2 = DiceNotationParser.notation_to_readable('D6', 3, -2)
        self.assertEqual(notation2, "3d6-2")
    
    def test_parse_and_describe(self):
        """Testa descrição da notação."""
        desc = self.parser.parse_and_describe("2d6+3")
        self.assertIn("2D6", desc)
        self.assertIn("+3", desc)


class TestIntegration(unittest.TestCase):
    """Testes de integração entre parser, config e roller."""
    
    def test_parser_to_roller(self):
        """Testa parse direto para rolagem."""
        parser = DiceNotationParser()
        roller = DiceRoller()
        
        params = parser.parse("2d6+3")
        result = roller.roll(**params)
        
        self.assertEqual(result['dice_type'], 'D6')
        self.assertEqual(result['quantity'], 2)
        self.assertEqual(result['modifier'], 3)
        self.assertGreaterEqual(result['total'], 5)  # Mín: 1+1+3
        self.assertLessEqual(result['total'], 15)   # Máx: 6+6+3
    
    def test_saved_config_execution(self):
        """Testa salvar configuração e executar."""
        test_file = "test_integration.json"
        
        try:
            configs = SavedConfigurations(test_file)
            parser = DiceNotationParser()
            roller = DiceRoller()
            
            # Salva configuração
            configs.save_config("MeuAtaque", "1d20+5")
            
            # Carrega e executa
            notation = configs.load_config("MeuAtaque")
            params = parser.parse(notation)
            result = roller.roll(**params)
            
            self.assertEqual(result['dice_type'], 'D20')
            self.assertGreaterEqual(result['total'], 6)  # Mín: 1+5
            self.assertLessEqual(result['total'], 25)   # Máx: 20+5
            
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


def run_tests():
    """Executa todos os testes."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDiceParser))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 TESTES DA FASE 2 - Config Manager & Dice Parser")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

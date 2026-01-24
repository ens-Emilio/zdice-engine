"""
Testes unitários para o Simulador de Dados RPG.

Para executar os testes:
    python -m pytest test_dice_simulator.py -v
    
Ou, se não tiver pytest instalado:
    python test_dice_simulator.py
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpg_dice_simulator.dice_engine import Dice, DiceRoller
from rpg_dice_simulator.history_manager import RollHistory


class TestDice(unittest.TestCase):
    """Testes para a classe Dice."""
    
    def test_dice_creation(self):
        """Testa criação de dados com diferentes números de faces."""
        for sides in [4, 6, 8, 10, 12, 20, 100]:
            dice = Dice(sides)
            self.assertEqual(dice.sides, sides)
    
    def test_invalid_dice_creation(self):
        """Testa que dados inválidos geram erro."""
        with self.assertRaises(ValueError):
            Dice(7)  # 7 faces não é válido
        
        with self.assertRaises(ValueError):
            Dice(100000)  # Muito grande
    
    def test_roll_in_range(self):
        """Testa que rolagens estão no intervalo correto."""
        for sides in [4, 6, 8, 10, 12, 20, 100]:
            dice = Dice(sides)
            for _ in range(100):  # Testa 100 vezes
                result = dice.roll()
                self.assertGreaterEqual(result, 1)
                self.assertLessEqual(result, sides)
    
    def test_roll_multiple(self):
        """Testa rolagem múltipla de dados."""
        dice = Dice(6)
        results = dice.roll_multiple(5)
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)
    
    def test_roll_multiple_invalid_quantity(self):
        """Testa que quantidade inválida gera erro."""
        dice = Dice(6)
        with self.assertRaises(ValueError):
            dice.roll_multiple(0)
        
        with self.assertRaises(ValueError):
            dice.roll_multiple(-5)


class TestDiceRoller(unittest.TestCase):
    """Testes para a classe DiceRoller."""
    
    def setUp(self):
        """Configura o roller para cada teste."""
        self.roller = DiceRoller()
    
    def test_available_dice(self):
        """Testa que todos os dados esperados estão disponíveis."""
        expected = ['D4', 'D6', 'D8', 'D10', 'D12', 'D20', 'D100']
        available = self.roller.get_available_dice()
        self.assertEqual(set(available), set(expected))
    
    def test_basic_roll(self):
        """Testa rolagem básica."""
        result = self.roller.roll('D6', quantity=1, modifier=0)
        
        self.assertEqual(result['dice_type'], 'D6')
        self.assertEqual(result['quantity'], 1)
        self.assertEqual(len(result['rolls']), 1)
        self.assertGreaterEqual(result['total'], 1)
        self.assertLessEqual(result['total'], 6)
    
    def test_roll_with_modifier(self):
        """Testa rolagem com modificador."""
        # Modificador positivo
        result = self.roller.roll('D6', quantity=1, modifier=5)
        self.assertEqual(result['modifier'], 5)
        self.assertEqual(result['total'], result['rolls'][0] + 5)
        
        # Modificador negativo
        result = self.roller.roll('D6', quantity=1, modifier=-2)
        self.assertEqual(result['modifier'], -2)
        self.assertEqual(result['total'], result['rolls'][0] - 2)
    
    def test_multiple_dice(self):
        """Testa rolagem de múltiplos dados."""
        result = self.roller.roll('D6', quantity=3, modifier=0)
        self.assertEqual(len(result['rolls']), 3)
        self.assertEqual(result['total'], sum(result['rolls']))
    
    def test_invalid_dice_type(self):
        """Testa que tipo de dado inválido gera erro."""
        with self.assertRaises(ValueError):
            self.roller.roll('D7')  # Não existe D7
    
    def test_advantage(self):
        """Testa rolagem com vantagem (D20)."""
        result = self.roller.roll('D20', quantity=1, advantage=True)
        
        self.assertTrue(result['advantage'])
        self.assertEqual(len(result['rolls']), 2)  # Duas rolagens
        # O total deve ser o maior dos dois + modificador
        self.assertEqual(result['total'], max(result['rolls']))
    
    def test_disadvantage(self):
        """Testa rolagem com desvantagem (D20)."""
        result = self.roller.roll('D20', quantity=1, disadvantage=True)
        
        self.assertTrue(result['disadvantage'])
        self.assertEqual(len(result['rolls']), 2)  # Duas rolagens
        # O total deve ser o menor dos dois + modificador
        self.assertEqual(result['total'], min(result['rolls']))
    
    def test_advantage_and_disadvantage_error(self):
        """Testa que vantagem e desvantagem juntas geram erro."""
        with self.assertRaises(ValueError):
            self.roller.roll('D20', advantage=True, disadvantage=True)
    
    def test_d100_special(self):
        """Testa rolagem D100 especial (2xD10)."""
        result = self.roller.roll_d100_special()
        
        self.assertEqual(result['dice_type'], 'D100_SPECIAL')
        self.assertEqual(len(result['rolls']), 2)
        self.assertGreaterEqual(result['total'], 1)
        self.assertLessEqual(result['total'], 100)
        
        # Verifica que os dados D10 estão no intervalo correto
        self.assertGreaterEqual(result['tens_die'], 1)
        self.assertLessEqual(result['tens_die'], 10)
        self.assertGreaterEqual(result['units_die'], 1)
        self.assertLessEqual(result['units_die'], 10)


class TestRollHistory(unittest.TestCase):
    """Testes para a classe RollHistory."""
    
    def setUp(self):
        """Configura o histórico para cada teste."""
        self.history = RollHistory()
        self.roller = DiceRoller()
    
    def test_empty_history(self):
        """Testa histórico vazio."""
        self.assertEqual(len(self.history.history), 0)
        self.assertEqual(len(self.history.get_history()), 0)
    
    def test_add_roll(self):
        """Testa adição de rolagem ao histórico."""
        roll = self.roller.roll('D6')
        self.history.add_roll(roll)
        
        self.assertEqual(len(self.history.history), 1)
        self.assertEqual(self.history.history[0], roll)
    
    def test_get_history_limit(self):
        """Testa limite de histórico."""
        # Adiciona 20 rolagens
        for _ in range(20):
            roll = self.roller.roll('D6')
            self.history.add_roll(roll)
        
        # Pega apenas as últimas 10
        recent = self.history.get_history(limit=10)
        self.assertEqual(len(recent), 10)
    
    def test_clear_history(self):
        """Testa limpeza do histórico."""
        # Adiciona algumas rolagens
        for _ in range(5):
            roll = self.roller.roll('D6')
            self.history.add_roll(roll)
        
        # Limpa
        self.history.clear_history()
        self.assertEqual(len(self.history.history), 0)
    
    def test_statistics_empty(self):
        """Testa estatísticas com histórico vazio."""
        stats = self.history.get_statistics()
        self.assertEqual(stats['total_rolls'], 0)
    
    def test_statistics_with_data(self):
        """Testa estatísticas com dados."""
        # Adiciona algumas rolagens
        for _ in range(10):
            roll = self.roller.roll('D6', modifier=0)
            self.history.add_roll(roll)
        
        stats = self.history.get_statistics()
        self.assertEqual(stats['total_rolls'], 10)
        self.assertIn('D6', stats['dice_usage'])
        self.assertEqual(stats['dice_usage']['D6'], 10)


class TestStatisticalDistribution(unittest.TestCase):
    """Testes estatísticos de distribuição de rolagens."""
    
    def test_d6_distribution(self):
        """Testa que a distribuição de D6 é aproximadamente uniforme."""
        dice = Dice(6)
        results = [dice.roll() for _ in range(6000)]  # 6000 rolagens
        
        # Conta ocorrências de cada face
        counts = {i: results.count(i) for i in range(1, 7)}
        
        # Esperamos ~1000 de cada (com margem de 20%)
        for count in counts.values():
            self.assertGreater(count, 800)  # Pelo menos 800
            self.assertLess(count, 1200)    # No máximo 1200
    
    def test_d20_distribution(self):
        """Testa que a distribuição de D20 é aproximadamente uniforme."""
        dice = Dice(20)
        results = [dice.roll() for _ in range(2000)]  # 2000 rolagens
        
        # Conta ocorrências de cada face
        counts = {i: results.count(i) for i in range(1, 21)}
        
        # Esperamos ~100 de cada (com margem de 50%)
        for count in counts.values():
            self.assertGreater(count, 50)   # Pelo menos 50
            self.assertLess(count, 150)     # No máximo 150


def run_tests():
    """Executa todos os testes."""
    # Cria uma suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona todos os testes
    suite.addTests(loader.loadTestsFromTestCase(TestDice))
    suite.addTests(loader.loadTestsFromTestCase(TestDiceRoller))
    suite.addTests(loader.loadTestsFromTestCase(TestRollHistory))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalDistribution))
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retorna True se todos passaram
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 EXECUTANDO TESTES DO SIMULADOR DE DADOS RPG")
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

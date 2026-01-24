"""
Funções utilitárias para o simulador de dados RPG.
"""

from typing import Dict, List


def format_roll_result(roll_data: Dict) -> str:
    """
    Formata o resultado de uma rolagem para exibição.
    
    Args:
        roll_data: Dicionário com dados da rolagem
        
    Returns:
        String formatada com o resultado
    """
    dice_type = roll_data.get('dice_type', 'UNKNOWN')
    quantity = roll_data.get('quantity', 1)
    rolls = roll_data.get('rolls', [])
    modifier = roll_data.get('modifier', 0)
    total = roll_data.get('total', 0)
    advantage = roll_data.get('advantage', False)
    disadvantage = roll_data.get('disadvantage', False)
    explode = roll_data.get('explode', False)
    
    # Caso especial para D100_SPECIAL
    if dice_type == 'D100_SPECIAL':
        tens = roll_data.get('tens_die', 0)
        units = roll_data.get('units_die', 0)
        return f"""
╔══════════════════════════════════════════════╗
║          🎲 ROLAGEM D100 ESPECIAL           ║
╠══════════════════════════════════════════════╣
║  Dado de Dezenas:  {tens:2d}0                      ║
║  Dado de Unidades: {units:2d}                       ║
║                                              ║
║  ➜ RESULTADO FINAL: {total:3d}                    ║
╚══════════════════════════════════════════════╝
"""
    
    # Cabeçalho
    header = f"🎲 {quantity}{dice_type}"
    
    # Modificador
    if modifier > 0:
        header += f" +{modifier}"
    elif modifier < 0:
        header += f" {modifier}"
    
    # Indicadores especiais
    extras = []
    if advantage:
        extras.append("VANTAGEM")
    if disadvantage:
        extras.append("DESVANTAGEM")
    if explode:
        extras.append("EXPLOSÃO")
    
    if extras:
        header += f" ({', '.join(extras)})"
    
    # Rolagens individuais
    rolls_str = " + ".join([str(r) for r in rolls])
    if modifier != 0:
        rolls_str += f" {'+' if modifier > 0 else ''}{modifier}"
    
    # Vantagem/Desvantagem mostra ambas as rolagens
    if advantage or disadvantage:
        type_label = "VANTAGEM" if advantage else "DESVANTAGEM"
        return f"""
╔══════════════════════════════════════════════╗
║          {header:^40s}          ║
╠══════════════════════════════════════════════╣
║  Rolagem 1: {rolls[0]:2d}                             ║
║  Rolagem 2: {rolls[1]:2d}                             ║
║                                              ║
║  {type_label}: Usando {total - modifier:2d}                   ║
║  ➜ RESULTADO FINAL: {total:3d}                    ║
╚══════════════════════════════════════════════╝
"""
    
    # Resultado padrão
    return f"""
╔══════════════════════════════════════════════╗
║          {header:^40s}          ║
╠══════════════════════════════════════════════╣
║  Rolagens: {rolls_str:<31s} ║
║  ➜ RESULTADO FINAL: {total:3d}                    ║
╚══════════════════════════════════════════════╝
"""


def format_history(history: List[Dict], limit: int = 10) -> str:
    """
    Formata o histórico de rolagens para exibição.
    
    Args:
        history: Lista de rolagens
        limit: Número máximo de rolagens a exibir
        
    Returns:
        String formatada com o histórico
    """
    if not history:
        return "\n📜 Nenhuma rolagem no histórico.\n"
    
    output = "\n" + "═" * 50 + "\n"
    output += "📜 HISTÓRICO DE ROLAGENS (últimas primeiro)\n"
    output += "═" * 50 + "\n\n"
    
    for i, roll in enumerate(history[:limit], 1):
        dice_type = roll.get('dice_type', 'UNKNOWN')
        quantity = roll.get('quantity', 1)
        total = roll.get('total', 0)
        modifier = roll.get('modifier', 0)
        
        mod_str = ""
        if modifier > 0:
            mod_str = f" +{modifier}"
        elif modifier < 0:
            mod_str = f" {modifier}"
        
        output += f"{i:2d}. {quantity}{dice_type}{mod_str} = {total}\n"
    
    if len(history) > limit:
        output += f"\n... e mais {len(history) - limit} rolagens\n"
    
    output += "\n" + "═" * 50 + "\n"
    return output


def format_statistics(stats: Dict) -> str:
    """
    Formata estatísticas do histórico.
    
    Args:
        stats: Dicionário com estatísticas
        
    Returns:
        String formatada com as estatísticas
    """
    if stats['total_rolls'] == 0:
        return "\n📊 Nenhuma estatística disponível.\n"
    
    output = "\n" + "═" * 50 + "\n"
    output += "📊 ESTATÍSTICAS DE ROLAGENS\n"
    output += "═" * 50 + "\n\n"
    
    output += f"Total de rolagens: {stats['total_rolls']}\n"
    output += f"Média dos totais: {stats['average_total']:.2f}\n"
    output += f"Maior total: {stats['max_roll']}\n"
    output += f"Menor total: {stats['min_roll']}\n\n"
    
    output += "Uso de dados:\n"
    for dice_type, count in stats['dice_usage'].items():
        percentage = (count / stats['total_rolls']) * 100
        output += f"  {dice_type}: {count} ({percentage:.1f}%)\n"
    
    output += "\n" + "═" * 50 + "\n"
    return output


def validate_integer_input(prompt: str, min_value: int = None, 
                          max_value: int = None, default: int = None) -> int:
    """
    Solicita e valida entrada de número inteiro.
    
    Args:
        prompt: Mensagem a exibir
        min_value: Valor mínimo aceito
        max_value: Valor máximo aceito
        default: Valor padrão se usuário pressionar Enter
        
    Returns:
        Número inteiro validado
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Se usuário pressionar Enter e houver default
            if not user_input and default is not None:
                return default
            
            value = int(user_input)
            
            # Validar limites
            if min_value is not None and value < min_value:
                print(f"❌ Valor mínimo: {min_value}")
                continue
            
            if max_value is not None and value > max_value:
                print(f"❌ Valor máximo: {max_value}")
                continue
            
            return value
            
        except ValueError:
            print("❌ Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada.")
            raise


def format_saved_configs(configs: Dict[str, str]) -> str:
    """
    Formata lista de configurações salvas para exibição.
    
    Args:
        configs: Dicionário com nome -> notação
        
    Returns:
        String formatada
    """
    if not configs:
        return "\n📝 Nenhuma configuração salva.\n"
    
    output = "\n" + "═" * 60 + "\n"
    output += "📝 CONFIGURAÇÕES SALVAS\n"
    output += "═" * 60 + "\n\n"
    
    for i, (name, notation) in enumerate(sorted(configs.items()), 1):
        output += f"{i:2d}. {name:<30s} → {notation}\n"
    
    output += "\n" + "═" * 60 + "\n"
    return output


def clear_screen():
    """Limpa a tela do terminal (multiplataforma)."""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')


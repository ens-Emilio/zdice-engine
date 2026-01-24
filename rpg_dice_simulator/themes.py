"""
Sistema de temas coloridos para CLI usando códigos ANSI.

Este módulo fornece diferentes esquemas de cores para melhorar
a experiência visual do usuário na interface de linha de comando.
"""

from typing import Dict


class Colors:
    """Códigos de cores ANSI."""
    
    # Reset
    RESET = '\033[0m'
    
    # Estilos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Cores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Cores brilhantes
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Cores de fundo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class Theme:
    """Define um esquema de cores para a interface."""
    
    def __init__(self, name: str, colors: Dict[str, str]):
        """
        Inicializa um tema.
        
        Args:
            name: Nome do tema
            colors: Dicionário com mapeamento de elementos -> cor ANSI
        """
        self.name = name
        self.colors = colors
    
    def get(self, element: str, default: str = '') -> str:
        """
        Obtém a cor de um elemento.
        
        Args:
            element: Nome do elemento (ex: 'header', 'success', 'error')
            default: Cor padrão se elemento não existir
            
        Returns:
            Código de cor ANSI
        """
        return self.colors.get(element, default)
    
    def colorize(self, text: str, element: str) -> str:
        """
        Aplica cor a um texto.
        
        Args:
            text: Texto a colorir
            element: Tipo de elemento
            
        Returns:
            Texto com códigos ANSI de cor
        """
        color = self.get(element)
        if color:
            return f"{color}{text}{Colors.RESET}"
        return text


# Definição dos temas
THEMES = {
    'padrao': Theme('Padrão', {
        'header': Colors.BOLD + Colors.CYAN,
        'menu': Colors.CYAN,
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'info': Colors.BLUE,
        'dice': Colors.BOLD + Colors.MAGENTA,
        'result': Colors.BOLD + Colors.GREEN,
        'prompt': Colors.WHITE,
        'separator': Colors.BRIGHT_BLACK,
    }),
    
    'escuro': Theme('Escuro', {
        'header': Colors.BOLD + Colors.BRIGHT_CYAN,
        'menu': Colors.BRIGHT_CYAN,
        'success': Colors.BRIGHT_GREEN,
        'error': Colors.BRIGHT_RED,
        'warning': Colors.BRIGHT_YELLOW,
        'info': Colors.BRIGHT_BLUE,
        'dice': Colors.BOLD + Colors.BRIGHT_MAGENTA,
        'result': Colors.BOLD + Colors.BRIGHT_GREEN,
        'prompt': Colors.BRIGHT_WHITE,
        'separator': Colors.BRIGHT_BLACK,
    }),
    
    'claro': Theme('Claro', {
        'header': Colors.BOLD + Colors.BLUE,
        'menu': Colors.BLUE,
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'info': Colors.CYAN,
        'dice': Colors.BOLD + Colors.MAGENTA,
        'result': Colors.BOLD + Colors.GREEN,
        'prompt': Colors.BLACK,
        'separator': Colors.BLACK,
    }),
    
    'neon': Theme('Neon', {
        'header': Colors.BOLD + Colors.BRIGHT_MAGENTA,
        'menu': Colors.BRIGHT_CYAN,
        'success': Colors.BRIGHT_GREEN,
        'error': Colors.BRIGHT_RED,
        'warning': Colors.BRIGHT_YELLOW,
        'info': Colors.BRIGHT_BLUE,
        'dice': Colors.BOLD + Colors.BRIGHT_YELLOW,
        'result': Colors.BOLD + Colors.BRIGHT_CYAN,
        'prompt': Colors.BRIGHT_WHITE,
        'separator': Colors.BRIGHT_MAGENTA,
    }),
    
    'monocromatico': Theme('Monocromático', {
        'header': Colors.BOLD,
        'menu': '',
        'success': '',
        'error': '',
        'warning': '',
        'info': '',
        'dice': Colors.BOLD,
        'result': Colors.BOLD,
        'prompt': '',
        'separator': '',
    }),
}


class ThemeManager:
    """Gerencia o tema atual da aplicação."""
    
    def __init__(self, theme_name: str = 'padrao'):
        """
        Inicializa o gerenciador de temas.
        
        Args:
            theme_name: Nome do tema inicial
        """
        self.current_theme_name = theme_name
        self.current_theme = THEMES.get(theme_name, THEMES['padrao'])
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Define o tema atual.
        
        Args:
            theme_name: Nome do tema
            
        Returns:
            True se tema foi alterado, False se tema não existe
        """
        if theme_name in THEMES:
            self.current_theme_name = theme_name
            self.current_theme = THEMES[theme_name]
            return True
        return False
    
    def get_theme(self) -> Theme:
        """
        Obtém o tema atual.
        
        Returns:
            Objeto Theme atual
        """
        return self.current_theme
    
    def list_themes(self) -> list[str]:
        """
        Lista todos os temas disponíveis.
        
        Returns:
            Lista com nomes dos temas
        """
        return list(THEMES.keys())
    
    def colorize(self, text: str, element: str) -> str:
        """
        Aplica cor do tema atual a um texto.
        
        Args:
            text: Texto a colorir
            element: Tipo de elemento
            
        Returns:
            Texto colorido
        """
        return self.current_theme.colorize(text, element)
    
    def print_colored(self, text: str, element: str):
        """
        Imprime texto colorido.
        
        Args:
            text: Texto a imprimir
            element: Tipo de elemento
        """
        print(self.colorize(text, element))


# Instância global do gerenciador de temas
_theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """
    Obtém a instância global do gerenciador de temas.
    
    Returns:
        Instância de ThemeManager
    """
    return _theme_manager


def set_theme(theme_name: str) -> bool:
    """
    Atalho para definir o tema global.
    
    Args:
        theme_name: Nome do tema
        
    Returns:
        True se sucesso
    """
    return _theme_manager.set_theme(theme_name)


def colorize(text: str, element: str) -> str:
    """
    Atalho para colorir texto com o tema global.
    
    Args:
        text: Texto a colorir
        element: Tipo de elemento
        
    Returns:
        Texto colorido
    """
    return _theme_manager.colorize(text, element)

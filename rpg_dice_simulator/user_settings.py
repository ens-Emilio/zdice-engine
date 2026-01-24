"""
Configurações de usuário persistentes.

Este módulo gerencia as preferências do usuário, como tema preferido,
formato de exibição e outras configurações personalizadas.
"""

import json
import os
from typing import Dict, Any
from datetime import datetime


class UserSettings:
    """Gerencia configurações de usuário com persistência."""
    
    DEFAULT_SETTINGS = {
        'theme': 'padrao',
        'language': 'pt',
        'show_confirmations': True,
        'result_format': 'detailed',  # 'detailed' ou 'compact'
        'auto_save_history': True,
        'sound_enabled': False,
    }
    
    def __init__(self, settings_file: str = "user_settings.json"):
        """
        Inicializa as configurações de usuário.
        
        Args:
            settings_file: Caminho do arquivo de configurações
        """
        self.settings_file = settings_file
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém uma configuração.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se não existir
            
        Returns:
            Valor da configuração
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Define uma configuração.
        
        Args:
            key: Chave da configuração
            value: Novo valor
        """
        self.settings[key] = value
        self.save()
    
    def update(self, settings_dict: Dict[str, Any]) -> None:
        """
        Atualiza múltiplas configurações.
        
        Args:
            settings_dict: Dicionário com configurações a atualizar
        """
        self.settings.update(settings_dict)
        self.save()
    
    def reset(self) -> None:
        """Restaura configurações padrão."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
        print("✅ Configurações restauradas para os valores padrão.")
    
    def load(self) -> bool:
        """
        Carrega configurações do arquivo.
        
        Returns:
            True se carregou com sucesso
        """
        if not os.path.exists(self.settings_file):
            return False
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'settings' in data:
                self.settings.update(data['settings'])
                return True
            return False
            
        except Exception as e:
            print(f"⚠️  Erro ao carregar configurações: {e}")
            return False
    
    def save(self) -> bool:
        """
        Salva configurações no arquivo.
        
        Returns:
            True se salvou com sucesso
        """
        try:
            data = {
                'settings': self.settings,
                'last_modified': datetime.now().isoformat()
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao salvar configurações: {e}")
            return False
    
    def show_settings(self) -> str:
        """
        Retorna uma representação formatada das configurações.
        
        Returns:
            String formatada
        """
        output = "\n" + "═" * 60 + "\n"
        output += "⚙️  CONFIGURAÇÕES DO USUÁRIO\n"
        output += "═" * 60 + "\n\n"
        
        labels = {
            'theme': 'Tema',
            'language': 'Idioma',
            'show_confirmations': 'Mostrar confirmações',
            'result_format': 'Formato de resultado',
            'auto_save_history': 'Salvar histórico automaticamente',
            'sound_enabled': 'Som habilitado',
        }
        
        for key, value in self.settings.items():
            label = labels.get(key, key)
            
            # Formata valores booleanos
            if isinstance(value, bool):
                value_str = "Sim" if value else "Não"
            else:
                value_str = str(value)
            
            output += f"  {label:<35s}: {value_str}\n"
        
        output += "\n" + "═" * 60 + "\n"
        return output
    
    def get_theme(self) -> str:
        """
        Retorna o tema preferido.
        
        Returns:
            Nome do tema
        """
        return self.get('theme', 'padrao')
    
    def set_theme(self, theme: str) -> None:
        """
        Define o tema preferido.
        
        Args:
            theme: Nome do tema
        """
        self.set('theme', theme)
    
    def toggle_confirmations(self) -> bool:
        """
        Alterna exibição de confirmações.
        
        Returns:
            Novo estado
        """
        new_value = not self.get('show_confirmations', True)
        self.set('show_confirmations', new_value)
        return new_value
    
    def toggle_auto_save(self) -> bool:
        """
        Alterna salvamento automático de histórico.
        
        Returns:
            Novo estado
        """
        new_value = not self.get('auto_save_history', True)
        self.set('auto_save_history', new_value)
        return new_value


# Instância global de configurações
_user_settings = UserSettings()


def get_user_settings() -> UserSettings:
    """
    Obtém a instância global de configurações.
    
    Returns:
        Instância de UserSettings
    """
    return _user_settings

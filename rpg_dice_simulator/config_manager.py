"""
Gerenciador de configurações salvas para rolagens pré-definidas.

Este módulo permite salvar, carregar e gerenciar rolagens de dados
pré-configuradas com nomes descritivos e persistência em arquivo JSON.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class SavedConfigurations:
    """Gerencia configurações de rolagens salvas com persistência em arquivo."""
    
    def __init__(self, config_file: str = "saved_configs.json"):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_file: Nome do arquivo JSON para persistência
        """
        self.config_file = config_file
        self.configs: Dict[str, str] = {}
        self.load_from_file()
    
    def save_config(self, name: str, dice_notation: str) -> bool:
        """
        Salva uma nova configuração de rolagem.
        
        Args:
            name: Nome descritivo da configuração (ex: "Ataque", "Dano")
            dice_notation: Notação da rolagem (ex: "1d20+5", "2d6+3")
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if not name or not dice_notation:
            print("❌ Nome e notação não podem ser vazios.")
            return False
        
        # Avisa se estiver sobrescrevendo
        if name in self.configs:
            print(f"⚠️  Configuração '{name}' já existe e será sobrescrita.")
        
        self.configs[name] = dice_notation
        self.save_to_file()
        print(f"✅ Configuração '{name}' salva: {dice_notation}")
        return True
    
    def load_config(self, name: str) -> Optional[str]:
        """
        Carrega uma configuração salva por nome.
        
        Args:
            name: Nome da configuração a carregar
            
        Returns:
            Notação da rolagem ou None se não encontrada
        """
        if name not in self.configs:
            print(f"❌ Configuração '{name}' não encontrada.")
            return None
        
        return self.configs[name]
    
    def list_configs(self) -> Dict[str, str]:
        """
        Lista todas as configurações salvas.
        
        Returns:
            Dicionário com nome -> notação
        """
        return self.configs.copy()
    
    def delete_config(self, name: str) -> bool:
        """
        Exclui uma configuração salva.
        
        Args:
            name: Nome da configuração a excluir
            
        Returns:
            True se excluiu com sucesso, False caso contrário
        """
        if name not in self.configs:
            print(f"❌ Configuração '{name}' não encontrada.")
            return False
        
        del self.configs[name]
        self.save_to_file()
        print(f"✅ Configuração '{name}' excluída.")
        return True
    
    def config_exists(self, name: str) -> bool:
        """
        Verifica se uma configuração existe.
        
        Args:
            name: Nome da configuração
            
        Returns:
            True se existe, False caso contrário
        """
        return name in self.configs
    
    def get_config_count(self) -> int:
        """
        Retorna o número de configurações salvas.
        
        Returns:
            Quantidade de configurações
        """
        return len(self.configs)
    
    def save_to_file(self) -> bool:
        """
        Salva as configurações para o arquivo JSON.
        
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            data = {
                'configs': self.configs,
                'last_modified': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def load_from_file(self) -> bool:
        """
        Carrega configurações do arquivo JSON.
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        if not os.path.exists(self.config_file):
            # Arquivo não existe ainda, não é erro
            return True
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'configs' in data:
                self.configs = data['configs']
                print(f"✅ {len(self.configs)} configuração(ões) carregada(s).")
                return True
            else:
                print("⚠️  Arquivo de configuração inválido.")
                return False
                
        except json.JSONDecodeError:
            print(f"❌ Erro ao ler arquivo JSON: {self.config_file}")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            return False
    
    def clear_all_configs(self) -> bool:
        """
        Remove todas as configurações salvas.
        
        Returns:
            True se limpou com sucesso
        """
        self.configs.clear()
        self.save_to_file()
        print("✅ Todas as configurações foram removidas.")
        return True
    
    def import_configs(self, filename: str) -> bool:
        """
        Importa configurações de outro arquivo JSON.
        
        Args:
            filename: Caminho do arquivo a importar
            
        Returns:
            True se importou com sucesso, False caso contrário
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'configs' in data:
                # Mescla com configurações existentes
                imported_count = 0
                for name, notation in data['configs'].items():
                    if name not in self.configs:
                        self.configs[name] = notation
                        imported_count += 1
                    else:
                        print(f"⚠️  '{name}' já existe, pulando...")
                
                self.save_to_file()
                print(f"✅ {imported_count} configuração(ões) importada(s).")
                return True
            else:
                print("❌ Arquivo não contém configurações válidas.")
                return False
                
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filename}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Erro ao ler arquivo JSON: {filename}")
            return False
        except Exception as e:
            print(f"❌ Erro ao importar configurações: {e}")
            return False
    
    def export_configs(self, filename: str) -> bool:
        """
        Exporta configurações para um arquivo JSON.
        
        Args:
            filename: Caminho do arquivo de destino
            
        Returns:
            True se exportou com sucesso, False caso contrário
        """
        try:
            data = {
                'configs': self.configs,
                'exported_at': datetime.now().isoformat(),
                'count': len(self.configs)
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {len(self.configs)} configuração(ões) exportada(s) para: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao exportar configurações: {e}")
            return False

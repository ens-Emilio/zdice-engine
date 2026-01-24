# 🎲 Simulador de Dados RPG (zdice-engine)

Um simulador de dados completo, potente e visual para sessões de RPG, desenvolvido em Python. Suporta desde rolagens simples até notação complexa, histórico persistente, configurações salvas e uma interface gráfica moderna.

## ✨ Características

- **Motor de Dados Robusto**: Suporte a D4, D6, D8, D10, D12, D20 e D100.
- **Notação de RPG Padrão**: Suporte a strings como `2d6+3`, `1d20a` (vantagem), `1d20d` (desvantagem) e `2d6!` (explosão).
- **Interface Dupla**:
    - **CLI (Terminal)**: Colorida com temas ANSI e menus intuitivos.
    - **GUI (Gráfica)**: Interface moderna construída com Tkinter.
- **Persistência**:
    - Histórico de rolagens com estatísticas.
    - Configurações de rolagens salvas (ex: "Ataque com Espada").
    - Preferências de usuário (temas, formatos).
- **Sem Dependências**: Desenvolvido inteiramente com a biblioteca padrão do Python.

## 📂 Estrutura do Projeto

```
zdice-engine/
├── main_cli.py            # Ponto de entrada para a Interface de Terminal (CLI)
├── main_gui.py            # Ponto de entrada para a Interface Gráfica (GUI)
├── rpg_dice_simulator/    # Pacote principal contendo a lógica
│   ├── ui/                # Interface de linha de comando
│   ├── gui/               # Interface gráfica
│   └── (módulos core)     # Engine, Parser, Configs, Themes, etc.
├── tests/                 # Suite de testes unitários
├── examples/              # Demonstrações de uso
└── docs/                  # Guias detalhados e documentação
```

## 🚀 Como Executar

Certifique-se de ter o Python 3.7 ou superior instalado.

### 🖥️ Interface Gráfica (Recomendado)
```bash
python main_gui.py
```

### 💻 Interface de Terminal
```bash
python main_cli.py
```

### 🧪 Executar Testes
```bash
python -m unittest discover tests
```

## 📖 Notação Suportada

O simulador entende a linguagem padrão dos RPGs:
- `2d6`: Rola dois dados de 6 faces.
- `1d20+5`: Rola um D20 e soma 5.
- `3d8-2`: Rola três D8 e subtrai 2.
- `1d20a`: Rola com **Vantagem** (pega o maior de 2 dados).
- `1d20d`: Rola com **Desvantagem** (pega o menor de 2 dados).
- `2d6!`: **Explosão** (rola novamente ao tirar o valor máximo).

## 🎨 Temas da CLI

A versão de terminal suporta 5 temas visuais:
1. **Padrão**: Cores balanceadas.
2. **Escuro**: Para terminais com fundo preto.
3. **Claro**: Para terminais com fundo branco.
4. **Neon**: Cores vibrantes e futuristas.
5. **Monocromático**: Sem cores ANSI.

## 🛠️ Tecnologias
- Python 3.x
- Tkinter (GUI)
- JSON (Persistência)
- Unittest

---
Desenvolvido com ❤️ para a comunidade de RPG.

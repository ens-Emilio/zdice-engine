# Guia de Uso - Simulador de Dados RPG

Este documento fornece instruções detalhadas sobre como aproveitar ao máximo os recursos do Simulador de Dados RPG.

## 💻 Interface de Terminal (CLI)

Ao executar `python main_cli.py`, você terá acesso ao menu principal:

### 1. Rolar Dados
- Selecione o tipo de dado (D4 a D100).
- Insira a quantidade (ex: 3).
- Insira o modificador (ex: +2 ou -1).
- Escolha opções especiais como **Explosão** ou **Vantagem/Desvantagem** (apenas para D20).

### 2. Histórico e Estatísticas
- Verifique suas rolagens anteriores.
- Veja estatísticas de desempenho e uso de dados.
- Exporte seu histórico para um arquivo `.json` para manter um registro de suas sessões.

### 3. Gerenciar Configurações
- Salve rolagens frequentes com nomes personalizados (ex: "Ataque Espada Longa" -> `1d20+7`).
- Recupere e execute rapidamente essas configurações.

### 4. Temas e Preferências
- Alterne entre os 5 temas coloridos para personalizar o visual do seu terminal.

---

## 🖥️ Interface Gráfica (GUI)

Executando `python main_gui.py`, você terá uma janela com:

### Painel de Controle (Superior)
- **Botões de Dados**: Clique em um dado para selecioná-lo.
- **Opções**: Ajuste quantidade, modificador e marque flags como Vantagem ou Explosão.
- **Rolagem Rápida**: Digite a notação (ex: `2d6+3`) e pressione "Parse" para configurar tudo automaticamente.

### Visualização (Meio e Inferior)
- **Aba Resultado**: Mostra o detalhamento da última rolagem em letras garrafais.
- **Aba Histórico**: Lista cronológica de todas as rolagens desta sessão.
- **Aba Configurações**: Lista de todas as suas configurações salvas. Clique em uma e use o botão "Usar" para carregar os parâmetros.

---

## 📝 Notação de Dados

O simulador suporta a seguinte gramática de notação:

- `[Qtd]d[Faces][Modificadores][Opções]`

### Exemplos:
- `1d20`: Um D20 simples.
- `2d6+4`: Dois D6 somados, com +4 de bônus.
- `1d20a+5`: Um D20 com vantagem e +5 de bônus.
- `3d8!`: Três D8 com regra de explosão.

---

## 🛠️ Manutenção e Organização

- **Configurações**: Salvas em `saved_configs.json`.
- **Preferências**: Salvas em `user_settings.json`.
- **Histórico**: Pode ser exportado manualmente ou configurado para auto-save.

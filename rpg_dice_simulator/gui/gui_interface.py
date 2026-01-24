"""
Interface Gráfica (GUI) para o Simulador de Dados RPG.

Desenvolvida com Tkinter para uma experiência visual moderna e intuitiva.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ..dice_engine import DiceRoller
from ..history_manager import RollHistory
from ..config_manager import SavedConfigurations
from ..dice_parser import DiceNotationParser


class DiceSimulatorGUI:
    """Interface gráfica principal do simulador de dados."""
    
    def __init__(self, root):
        """
        Inicializa a GUI.
        
        Args:
            root: Janela principal Tkinter
        """
        self.root = root
        self.root.title("🎲 Simulador de Dados RPG")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Inicializa componentes do sistema
        self.roller = DiceRoller()
        self.history = RollHistory()
        self.configs = SavedConfigurations()
        self.parser = DiceNotationParser()
        
        # Variáveis da interface
        self.selected_dice = tk.StringVar(value="D20")
        self.quantity = tk.IntVar(value=1)
        self.modifier = tk.IntVar(value=0)
        self.advantage = tk.BooleanVar(value=False)
        self.disadvantage = tk.BooleanVar(value=False)
        self.explode = tk.BooleanVar(value=False)
        
        # Configura estilo
        self.setup_style()
        
        # Cria interface
        self.create_widgets()
        
        # Centraliza janela
        self.center_window()
    
    def setup_style(self):
        """Configura o estilo da interface."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2E86AB')
        style.configure('Dice.TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('Roll.TButton', font=('Arial', 14, 'bold'), padding=15)
    
    def center_window(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text="🎲 Simulador de Dados RPG", style='Title.TLabel')
        title.grid(row=0, column=0, pady=10)
        
        # Container superior (dados e opções)
        top_container = ttk.Frame(main_frame)
        top_container.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        top_container.columnconfigure(0, weight=1)
        top_container.columnconfigure(1, weight=1)
        
        # Frame de dados (esquerda)
        self.create_dice_frame(top_container)
        
        # Frame de opções (direita)
        self.create_options_frame(top_container)
        
        # Botão de rolar (grande e destacado)
        roll_button = ttk.Button(
            main_frame,
            text="🎲 ROLAR DADOS",
            style='Roll.TButton',
            command=self.roll_dice
        )
        roll_button.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Container inferior (resultado e histórico)
        bottom_container = ttk.Frame(main_frame)
        bottom_container.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        bottom_container.columnconfigure(0, weight=1)
        bottom_container.rowconfigure(0, weight=1)
        
        # Frame de resultado e histórico
        self.create_result_frame(bottom_container)
        
        # Menu superior
        self.create_menu()
    
    def create_dice_frame(self, parent):
        """Cria o frame de seleção de dados."""
        frame = ttk.LabelFrame(parent, text="Tipo de Dado", padding="10")
        frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N))
        
        # Botões de dados
        dice_types = ['D4', 'D6', 'D8', 'D10', 'D12', 'D20', 'D100']
        
        for i, dice in enumerate(dice_types):
            row = i // 3
            col = i % 3
            btn = ttk.Radiobutton(
                frame,
                text=dice,
                variable=self.selected_dice,
                value=dice,
                style='Dice.TButton'
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configura colunas para distribuir uniformemente
        for i in range(3):
            frame.columnconfigure(i, weight=1)
    
    def create_options_frame(self, parent):
        """Cria o frame de opções."""
        frame = ttk.LabelFrame(parent, text="Opções", padding="10")
        frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N))
        
        # Quantidade
        qty_frame = ttk.Frame(frame)
        qty_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Label(qty_frame, text="Quantidade:").pack(side=tk.LEFT, padx=5)
        qty_spin = ttk.Spinbox(qty_frame, from_=1, to=100, textvariable=self.quantity, width=10)
        qty_spin.pack(side=tk.LEFT, padx=5)
        
        # Modificador
        mod_frame = ttk.Frame(frame)
        mod_frame.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        ttk.Label(mod_frame, text="Modificador:").pack(side=tk.LEFT, padx=5)
        mod_spin = ttk.Spinbox(mod_frame, from_=-100, to=100, textvariable=self.modifier, width=10)
        mod_spin.pack(side=tk.LEFT, padx=5)
        
        # Checkboxes
        ttk.Checkbutton(frame, text="Vantagem (D20)", variable=self.advantage).grid(row=2, column=0, pady=2, sticky=tk.W)
        ttk.Checkbutton(frame, text="Desvantagem (D20)", variable=self.disadvantage).grid(row=3, column=0, pady=2, sticky=tk.W)
        ttk.Checkbutton(frame, text="Explosão", variable=self.explode).grid(row=4, column=0, pady=2, sticky=tk.W)
        
        # Rolagem rápida
        quick_frame = ttk.LabelFrame(frame, text="Rolagem Rápida", padding="5")
        quick_frame.grid(row=5, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.quick_entry = ttk.Entry(quick_frame, width=15)
        self.quick_entry.pack(side=tk.LEFT, padx=5)
        self.quick_entry.insert(0, "Ex: 2d6+3")
        
        ttk.Button(quick_frame, text="Parse", command=self.parse_notation).pack(side=tk.LEFT)
    
    def create_result_frame(self, parent):
        """Cria o frame de resultados e histórico."""
        # Notebook (abas)
        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de Resultado
        result_frame = ttk.Frame(notebook)
        notebook.add(result_frame, text="📊 Resultado")
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=15,
            font=('Courier', 11),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba de Histórico
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="📜 Histórico")
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            height=15,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba de Configurações Salvas
        configs_frame = ttk.Frame(notebook)
        notebook.add(configs_frame, text="💾 Configurações")
        
        self.create_configs_tab(configs_frame)
    
    def create_configs_tab(self, parent):
        """Cria a aba de configurações salvas."""
        # Lista de configurações
        self.configs_listbox = tk.Listbox(parent, height=10)
        self.configs_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Usar", command=self.use_saved_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Salvar Atual", command=self.save_current_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Atualizar", command=self.refresh_configs).pack(side=tk.LEFT, padx=2)
        
        self.refresh_configs()
   
    def create_menu(self):
        """Cria a barra de menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Exportar Histórico", command=self.export_history)
        file_menu.add_command(label="Importar Histórico", command=self.import_history)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
    
    def roll_dice(self):
        """Executa a rolagem de dados."""
        try:
            # Validações
            if self.advantage.get() and self.disadvantage.get():
                messagebox.showerror("Erro", "Não pode ter vantagem e desvantagem ao mesmo tempo!")
                return
            
            # Realiza rolagem
            result = self.roller.roll(
                dice_type=self.selected_dice.get(),
                quantity=self.quantity.get(),
                modifier=self.modifier.get(),
                advantage=self.advantage.get(),
                disadvantage=self.disadvantage.get(),
                explode=self.explode.get()
            )
            
            # Adiciona ao histórico
            self.history.add_roll(result)
            
            # Exibe resultado
            self.display_result(result)
            self.update_history_display()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao rolar dados: {e}")
    
    def display_result(self, result):
        """Exibe o resultado da rolagem."""
        self.result_text.delete('1.0', tk.END)
        
        # Formata resultado
        output = f"\n{'='*50}\n"
        output += f"🎲 {result['quantity']}{result['dice_type']}"
        
        if result['modifier'] > 0:
            output += f" +{result['modifier']}"
        elif result['modifier'] < 0:
            output += f" {result['modifier']}"
        
        output += f"\n{'='*50}\n\n"
        
        # Rolagens individuais
        output += f"Rolagens: {' + '.join(map(str, result['rolls']))}"
        if result['modifier'] != 0:
            output += f" {'+' if result['modifier'] > 0 else ''}{result['modifier']}"
        
        output += f"\n\n{'='*50}\n"
        output += f"➜ RESULTADO FINAL: {result['total']}\n"
        output += f"{'='*50}\n"
        
        self.result_text.insert('1.0', output)
    
    def update_history_display(self):
        """Atualiza a exibição do histórico."""
        self.history_text.delete('1.0', tk.END)
        
        history = self.history.get_history(20)
        if not history:
            self.history_text.insert('1.0', "\nNenhuma rolagem no histórico.\n")
            return
        
        output = "\nHistórico de Rolagens (últimas primeiro):\n"
        output += "="*50 + "\n\n"
        
        for i, roll in enumerate(history, 1):
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
        
        self.history_text.insert('1.0', output)
    
    def parse_notation(self):
        """Faz parse da notação rápida."""
        notation = self.quick_entry.get()
        if notation and notation != "Ex: 2d6+3":
            params = self.parser.parse(notation)
            if params:
                # Atualiza campos
                self.selected_dice.set(params['dice_type'])
                self.quantity.set(params['quantity'])
                self.modifier.set(params['modifier'])
                self.advantage.set(params['advantage'])
                self.disadvantage.set(params['disadvantage'])
                self.explode.set(params['explode'])
                
                messagebox.showinfo("Sucesso", f"Notação '{notation}' aplicada!")
            else:
                messagebox.showerror("Erro", "Notação inválida!")
    
    def refresh_configs(self):
        """Atualiza a lista de configurações."""
        self.configs_listbox.delete(0, tk.END)
        configs = self.configs.list_configs()
        for name, notation in configs.items():
            self.configs_listbox.insert(tk.END, f"{name} → {notation}")
    
    def use_saved_config(self):
        """Usa uma configuração salva."""
        selection = self.configs_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma configuração!")
            return
        
        item = self.configs_listbox.get(selection[0])
        name = item.split(" → ")[0]
        notation = self.configs.load_config(name)
        
        if notation:
            self.quick_entry.delete(0, tk.END)
            self.quick_entry.insert(0, notation)
            self.parse_notation()
    
    def save_current_config(self):
        """Salva a configuração atual."""
        name = tk.simpledialog.askstring("Salvar Configuração", "Nome da configuração:")
        if name:
            notation = self.parser.notation_to_readable(
                self.selected_dice.get(),
                self.quantity.get(),
                self.modifier.get(),
                self.advantage.get(),
                self.disadvantage.get(),
                self.explode.get()
            )
            self.configs.save_config(name, notation)
            self.refresh_configs()
            messagebox.showinfo("Sucesso", f"Configuração '{name}' salva!")
    
    def delete_config(self):
        """Exclui uma configuração."""
        selection = self.configs_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma configuração!")
            return
        
        item = self.configs_listbox.get(selection[0])
        name = item.split(" → ")[0]
        
        if messagebox.askyesno("Confirmar", f"Excluir configuração '{name}'?"):
            self.configs.delete_config(name)
            self.refresh_configs()
    
    def export_history(self):
        """Exporta o histórico."""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.history.export_to_file(filename)
            messagebox.showinfo("Sucesso", f"Histórico exportado para {filename}")
    
    def import_history(self):
        """Importa histórico."""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.history.import_from_file(filename)
            self.update_history_display()
            messagebox.showinfo("Sucesso", "Histórico importado!")
    
    def show_about(self):
        """Mostra informações sobre o aplicativo."""
        messagebox.showinfo(
            "Sobre",
            "🎲 Simulador de Dados RPG v2.0\n\n"
            "Desenvolvido com Python e Tkinter\n\n"
            "Suporte a todos os dados padrão de RPG:\n"
            "D4, D6, D8, D10, D12, D20, D100\n\n"
            "Recursos:\n"
            "• Vantagem/Desvantagem\n"
            "• Explosão de dados\n"
            "• Configurações salvas\n"
            "• Histórico persistente\n"
            "• Notação padrão (ex: 2d6+3)"
        )


def main():
    """Ponto de entrada da GUI."""
    root = tk.Tk()
    app = DiceSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk, messagebox
from dados_oficina import OficinaApp

class InterfaceOficina:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento - Oficina")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.app = OficinaApp()
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        # Criar a interface
        self.criar_interface()
        
    def criar_interface(self):
        """Cria a interface gráfica principal"""
        
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, text="Registrar Serviço", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Frame para dados do carro
        frame_carro = ttk.LabelFrame(frame_principal, text="Dados do Carro", padding="10")
        frame_carro.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_carro, text="Marca:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_marca = ttk.Entry(frame_carro, width=30)
        self.entry_marca.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(frame_carro, text="Modelo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_modelo = ttk.Entry(frame_carro, width=30)
        self.entry_modelo.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(frame_carro, text="Ano:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_ano = ttk.Entry(frame_carro, width=30)
        self.entry_ano.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(frame_carro, text="Placa:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_placa = ttk.Entry(frame_carro, width=30)
        self.entry_placa.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        frame_carro.columnconfigure(1, weight=1)
        
        # Frame para dados do serviço
        frame_servico = ttk.LabelFrame(frame_principal, text="Dados do Serviço", padding="10")
        frame_servico.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_servico, text="Tipo de Serviço:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_servico = ttk.Combobox(frame_servico, width=27, state="readonly",
                                          values=self.app.get_tipos_servico())
        self.combo_servico.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(frame_servico, text="Descrição (opcional):").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.text_descricao = tk.Text(frame_servico, width=38, height=4, font=("Arial", 10))
        self.text_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        frame_servico.columnconfigure(1, weight=1)
        
        # Frame de botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill=tk.X, pady=20)
        
        btn_salvar = ttk.Button(frame_botoes, text="Salvar Registro", 
                               command=self.salvar_registro)
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = ttk.Button(frame_botoes, text="Limpar", 
                               command=self.limpar_campos)
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        btn_view = ttk.Button(frame_botoes, text="Ver Registros", 
                             command=self.ver_registros)
        btn_view.pack(side=tk.LEFT, padx=5)
        
    def salvar_registro(self):
        """Salva o registro no arquivo CSV"""
        marca = self.entry_marca.get().strip()
        modelo = self.entry_modelo.get().strip()
        ano = self.entry_ano.get().strip()
        placa = self.entry_placa.get().strip()
        servico = self.combo_servico.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        # Validações
        if not all([marca, modelo, ano, placa, servico]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            # Validar ano como número
            int(ano)
        except ValueError:
            messagebox.showerror("Erro", "O ano deve ser um número válido!")
            return
        
        # Salvar registro
        sucesso = self.app.adicionar_registro(marca, modelo, ano, placa, servico, descricao)
        
        if sucesso:
            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o registro.")
    
    def limpar_campos(self):
        """Limpa todos os campos da interface"""
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.combo_servico.set("")
        self.text_descricao.delete("1.0", tk.END)
        self.entry_marca.focus()
    
    def ver_registros(self):
        """Abre uma janela para visualizar todos os registros"""
        registros = self.app.obter_registros()
        
        if not registros:
            messagebox.showinfo("Informação", "Nenhum registro encontrado.")
            return
        
        # Criar nova janela
        janela_registros = tk.Toplevel(self.root)
        janela_registros.title("Registros da Oficina")
        janela_registros.geometry("900x400")
        
        # Criar Treeview
        colunas = ("Marca", "Modelo", "Ano", "Placa", "Serviço", "Descrição", "Data")
        tree = ttk.Treeview(janela_registros, columns=colunas, height=15, show="tree headings")
        
        # Definir largura das colunas
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Marca", anchor=tk.W, width=80)
        tree.column("Modelo", anchor=tk.W, width=80)
        tree.column("Ano", anchor=tk.CENTER, width=50)
        tree.column("Placa", anchor=tk.CENTER, width=70)
        tree.column("Serviço", anchor=tk.W, width=100)
        tree.column("Descrição", anchor=tk.W, width=250)
        tree.column("Data", anchor=tk.CENTER, width=100)
        
        # Definir cabeçalhos
        for col in colunas:
            tree.heading(col, text=col)
        
        # Inserir dados
        for i, registro in enumerate(registros):
            tree.insert("", tk.END, values=registro)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(janela_registros, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Frame para botões
        frame_botoes_registros = ttk.Frame(janela_registros)
        frame_botoes_registros.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        def editar_selecionado():
            selecimento = tree.selection()
            if not selecimento:
                messagebox.showwarning("Aviso", "Selecione um registro para editar!")
                return
            indice = tree.index(selecimento[0])
            # Obter registro fresco do banco de dados
            todos_registros = self.app.obter_registros()
            if 0 <= indice < len(todos_registros):
                self.editar_registro_dialog(indice, todos_registros[indice], janela_registros)
            else:
                messagebox.showerror("Erro", "Registro não encontrado!")
        
        def deletar_selecionado():
            selecimento = tree.selection()
            if not selecimento:
                messagebox.showwarning("Aviso", "Selecione um registro para deletar!")
                return
            
            if messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este registro?"):
                indice = tree.index(selecimento[0])
                if self.app.deletar_registro(indice):
                    messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
                    tree.delete(selecimento[0])
                else:
                    messagebox.showerror("Erro", "Não foi possível deletar o registro.")
        
        btn_editar = ttk.Button(frame_botoes_registros, text="✏️ Editar", command=editar_selecionado)
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_deletar = ttk.Button(frame_botoes_registros, text="🗑️ Deletar", command=deletar_selecionado)
        btn_deletar.pack(side=tk.LEFT, padx=5)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def editar_registro_dialog(self, indice, registro, janela_pai):
        """Abre um diálogo para editar um registro"""
        # Debug: imprimir dados recebidos
        print(f"DEBUG: Indice={indice}, Registro={registro}")
        
        janela_edicao = tk.Toplevel(janela_pai)
        janela_edicao.title("Editar Registro")
        janela_edicao.geometry("500x450")
        janela_edicao.resizable(False, False)
        
        # Frame principal
        frame_edicao = ttk.Frame(janela_edicao, padding="15")
        frame_edicao.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_edicao, text="Editar Dados do Registro", 
                          font=("Arial", 12, "bold"))
        titulo.pack(pady=(0, 15))
        
        # Campos de entrada
        ttk.Label(frame_edicao, text="Marca:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_marca = ttk.Entry(frame_edicao, width=35)
        entry_marca.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_marca.insert(0, str(registro[0]))
        
        ttk.Label(frame_edicao, text="Modelo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_modelo = ttk.Entry(frame_edicao, width=35)
        entry_modelo.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_modelo.insert(0, str(registro[1]))
        
        ttk.Label(frame_edicao, text="Ano:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_ano = ttk.Entry(frame_edicao, width=35)
        entry_ano.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_ano.insert(0, str(registro[2]))
        
        ttk.Label(frame_edicao, text="Placa:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_placa = ttk.Entry(frame_edicao, width=35)
        entry_placa.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_placa.insert(0, str(registro[3]))
        
        ttk.Label(frame_edicao, text="Serviço:").grid(row=4, column=0, sticky=tk.W, pady=5)
        combo_servico = ttk.Combobox(frame_edicao, width=32, state="readonly",
                                    values=self.app.get_tipos_servico())
        combo_servico.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=10)
        combo_servico.set(str(registro[4]))
        
        ttk.Label(frame_edicao, text="Descrição:").grid(row=5, column=0, sticky=tk.NW, pady=5)
        text_descricao = tk.Text(frame_edicao, width=37, height=4, font=("Arial", 10))
        text_descricao.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=10)
        text_descricao.insert("1.0", str(registro[5]))
        
        frame_edicao.columnconfigure(1, weight=1)
        
        # Frame de botões
        frame_botoes_edicao = ttk.Frame(frame_edicao)
        frame_botoes_edicao.grid(row=6, column=0, columnspan=2, pady=20)
        
        def salvar_edicao():
            marca = entry_marca.get().strip()
            modelo = entry_modelo.get().strip()
            ano = entry_ano.get().strip()
            placa = entry_placa.get().strip()
            servico = combo_servico.get()
            descricao = text_descricao.get("1.0", tk.END).strip()
            
            if not all([marca, modelo, ano, placa, servico]):
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
                return
            
            try:
                int(ano)
            except ValueError:
                messagebox.showerror("Erro", "O ano deve ser um número válido!")
                return
            
            if self.app.editar_registro(indice, marca, modelo, ano, placa, servico, descricao):
                messagebox.showinfo("Sucesso", "Registro editado com sucesso!")
                janela_edicao.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível editar o registro.")
        
        btn_salvar = ttk.Button(frame_botoes_edicao, text="Salvar", command=salvar_edicao)
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = ttk.Button(frame_botoes_edicao, text="Cancelar", command=janela_edicao.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=5)


def main():
    root = tk.Tk()
    interface = InterfaceOficina(root)
    root.mainloop()


if __name__ == "__main__":
    main()

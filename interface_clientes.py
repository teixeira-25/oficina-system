import tkinter as tk
from tkinter import ttk, messagebox
from clientes import GerenciadorClientes

class InterfaceClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Clientes - Oficina")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        self.gerenciador = GerenciadorClientes()
        self.cliente_selecionado = None
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        # Criar a interface
        self.criar_interface()
        self.atualizar_lista_clientes()
    
    def criar_interface(self):
        """Cria a interface principal"""
        
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # ===== LADO ESQUERDO - CLIENTES =====
        frame_clientes = ttk.LabelFrame(frame_principal, text="👥 Clientes", padding="10")
        frame_clientes.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 5), pady=0)
        
        # Campos para novo cliente
        ttk.Label(frame_clientes, text="Nome:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_nome_cliente = ttk.Entry(frame_clientes, width=40)
        self.entry_nome_cliente.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame_clientes, text="Telefone:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_telefone_cliente = ttk.Entry(frame_clientes, width=40)
        self.entry_telefone_cliente.pack(anchor=tk.W, pady=(0, 10))
        
        btn_novo_cliente = ttk.Button(frame_clientes, text="➕ Novo Cliente", 
                                      command=self.adicionar_cliente)
        btn_novo_cliente.pack(fill=tk.X, pady=(0, 15))
        
        # Lista de clientes
        ttk.Label(frame_clientes, text="Clientes Cadastrados:").pack(anchor=tk.W, pady=(10, 5))
        
        frame_tree = ttk.Frame(frame_clientes)
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_clientes = ttk.Treeview(frame_tree, columns=("Nome", "Telefone", "Carros"), 
                                          height=15, show="tree headings", yscrollcommand=scrollbar.set)
        self.tree_clientes.column("#0", width=0, stretch=tk.NO)
        self.tree_clientes.column("Nome", anchor=tk.W, width=150)
        self.tree_clientes.column("Telefone", anchor=tk.CENTER, width=100)
        self.tree_clientes.column("Carros", anchor=tk.CENTER, width=50)
        
        self.tree_clientes.heading("Nome", text="Nome")
        self.tree_clientes.heading("Telefone", text="Telefone")
        self.tree_clientes.heading("Carros", text="Carros")
        
        self.tree_clientes.bind("<<TreeviewSelect>>", self.selecionar_cliente)
        scrollbar.config(command=self.tree_clientes.yview)
        
        self.tree_clientes.pack(fill=tk.BOTH, expand=True)
        
        # Botões de cliente
        frame_btn_cliente = ttk.Frame(frame_clientes)
        frame_btn_cliente.pack(fill=tk.X, pady=(10, 0))
        
        btn_editar_cliente = ttk.Button(frame_btn_cliente, text="✏️ Editar", 
                                       command=self.editar_cliente)
        btn_editar_cliente.pack(side=tk.LEFT, padx=2)
        
        btn_deletar_cliente = ttk.Button(frame_btn_cliente, text="🗑️ Deletar", 
                                        command=self.deletar_cliente)
        btn_deletar_cliente.pack(side=tk.LEFT, padx=2)
        
        # ===== LADO DIREITO SUPERIOR - CARROS =====
        frame_carros = ttk.LabelFrame(frame_principal, text="🚗 Carros do Cliente", padding="10")
        frame_carros.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        
        ttk.Label(frame_carros, text="Marca:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_marca_carro = ttk.Entry(frame_carros, width=40)
        self.entry_marca_carro.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame_carros, text="Modelo:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_modelo_carro = ttk.Entry(frame_carros, width=40)
        self.entry_modelo_carro.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame_carros, text="Ano:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_ano_carro = ttk.Entry(frame_carros, width=40)
        self.entry_ano_carro.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame_carros, text="Placa:").pack(anchor=tk.W, pady=(0, 5))
        self.entry_placa_carro = ttk.Entry(frame_carros, width=40)
        self.entry_placa_carro.pack(anchor=tk.W, pady=(0, 10))
        
        btn_novo_carro = ttk.Button(frame_carros, text="➕ Adicionar Carro", 
                                    command=self.adicionar_carro)
        btn_novo_carro.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_carros, text="Carros Cadastrados:").pack(anchor=tk.W, pady=(10, 5))
        
        frame_tree_carros = ttk.Frame(frame_carros)
        frame_tree_carros.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar_carros = ttk.Scrollbar(frame_tree_carros, orient=tk.VERTICAL)
        scrollbar_carros.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_carros = ttk.Treeview(frame_tree_carros, columns=("Marca", "Modelo", "Ano", "Placa"), 
                                       height=8, show="tree headings", yscrollcommand=scrollbar_carros.set)
        self.tree_carros.column("#0", width=0, stretch=tk.NO)
        self.tree_carros.column("Marca", anchor=tk.W, width=100)
        self.tree_carros.column("Modelo", anchor=tk.W, width=100)
        self.tree_carros.column("Ano", anchor=tk.CENTER, width=50)
        self.tree_carros.column("Placa", anchor=tk.CENTER, width=80)
        
        self.tree_carros.heading("Marca", text="Marca")
        self.tree_carros.heading("Modelo", text="Modelo")
        self.tree_carros.heading("Ano", text="Ano")
        self.tree_carros.heading("Placa", text="Placa")
        
        self.tree_carros.bind("<<TreeviewSelect>>", self.selecionar_carro)
        scrollbar_carros.config(command=self.tree_carros.yview)
        
        self.tree_carros.pack(fill=tk.BOTH, expand=True)
        
        btn_deletar_carro = ttk.Button(frame_carros, text="🗑️ Deletar Carro", 
                                      command=self.deletar_carro)
        btn_deletar_carro.pack(fill=tk.X, pady=(10, 0))
        
        # ===== LADO DIREITO INFERIOR - SERVIÇOS =====
        frame_servicos = ttk.LabelFrame(frame_principal, text="🔧 Serviços", padding="10")
        frame_servicos.grid(row=1, column=1, sticky="nsew", padx=(5, 0), pady=(5, 0))
        
        ttk.Label(frame_servicos, text="Tipo de Serviço:").pack(anchor=tk.W, pady=(0, 5))
        self.combo_servico = ttk.Combobox(frame_servicos, width=38, state="readonly",
                                         values=self.gerenciador.get_tipos_servico())
        self.combo_servico.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame_servicos, text="Descrição (opcional):").pack(anchor=tk.W, pady=(0, 5))
        self.text_descricao_servico = tk.Text(frame_servicos, width=40, height=3, font=("Arial", 10))
        self.text_descricao_servico.pack(anchor=tk.W, pady=(0, 10))
        
        btn_novo_servico = ttk.Button(frame_servicos, text="➕ Adicionar Serviço", 
                                     command=self.adicionar_servico)
        btn_novo_servico.pack(fill=tk.X, pady=(0, 15))
        
        # Configurar grid weights
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(0, weight=1)
        frame_principal.rowconfigure(1, weight=1)
    
    def atualizar_lista_clientes(self):
        """Atualiza a lista de clientes"""
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        clientes = self.gerenciador.obter_clientes()
        
        for cliente in clientes:
            num_carros = len(cliente['carros'])
            self.tree_clientes.insert("", tk.END, values=(cliente['nome'], cliente['telefone'], num_carros), 
                                     iid=cliente['id'])
    
    def atualizar_lista_carros(self):
        """Atualiza a lista de carros do cliente selecionado"""
        self.tree_carros.delete(*self.tree_carros.get_children())
        
        if not self.cliente_selecionado:
            return
        
        carros = self.gerenciador.obter_carros_cliente(self.cliente_selecionado)
        
        for carro in carros:
            self.tree_carros.insert("", tk.END, 
                                   values=(carro['marca'], carro['modelo'], carro['ano'], carro['placa']),
                                   iid=carro['id'])
    
    def selecionar_cliente(self, event):
        """Callback quando seleciona um cliente"""
        selecionado = self.tree_clientes.selection()
        if selecionado:
            self.cliente_selecionado = selecionado[0]
            self.atualizar_lista_carros()
            self.limpar_campos_carro()
    
    def selecionar_carro(self, event):
        """Callback quando seleciona um carro"""
        pass  # Implementar se necessário
    
    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        nome = self.entry_nome_cliente.get().strip()
        telefone = self.entry_telefone_cliente.get().strip()
        
        if not nome or not telefone:
            messagebox.showwarning("Aviso", "Preencha nome e telefone!")
            return
        
        cliente = self.gerenciador.adicionar_cliente(nome, telefone)
        
        if cliente:
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' adicionado com sucesso!")
            self.entry_nome_cliente.delete(0, tk.END)
            self.entry_telefone_cliente.delete(0, tk.END)
            self.atualizar_lista_clientes()
        else:
            messagebox.showerror("Erro", "Erro ao adicionar cliente ou cliente já existe!")
    
    def editar_cliente(self):
        """Edita um cliente selecionado"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        cliente = self.gerenciador.obter_cliente(self.cliente_selecionado)
        
        # Criar janela de edição
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Cliente")
        janela_edicao.geometry("400x200")
        janela_edicao.resizable(False, False)
        
        frame = ttk.Frame(janela_edicao, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="✏️ Editar Cliente", font=("Arial", 12, "bold")).pack(pady=(0, 15))
        
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_nome = ttk.Entry(frame, width=30)
        entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_nome.insert(0, cliente['nome'])
        
        ttk.Label(frame, text="Telefone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_telefone = ttk.Entry(frame, width=30)
        entry_telefone.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=10)
        entry_telefone.insert(0, cliente['telefone'])
        
        frame.columnconfigure(1, weight=1)
        
        def salvar():
            nome = entry_nome.get().strip()
            telefone = entry_telefone.get().strip()
            
            if not nome or not telefone:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            if self.gerenciador.editar_cliente(self.cliente_selecionado, nome, telefone):
                messagebox.showinfo("Sucesso", "Cliente editado com sucesso!")
                janela_edicao.destroy()
                self.atualizar_lista_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao editar cliente!")
        
        frame_btn = ttk.Frame(frame)
        frame_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_btn, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn, text="Cancelar", command=janela_edicao.destroy).pack(side=tk.LEFT, padx=5)
    
    def deletar_cliente(self):
        """Deleta um cliente selecionado"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para deletar!")
            return
        
        if messagebox.askyesno("Confirmar", "Deletar este cliente e todos seus carros e serviços?"):
            if self.gerenciador.deletar_cliente(self.cliente_selecionado):
                messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
                self.cliente_selecionado = None
                self.atualizar_lista_clientes()
                self.atualizar_lista_carros()
                self.limpar_campos_carro()
            else:
                messagebox.showerror("Erro", "Erro ao deletar cliente!")
    
    def limpar_campos_carro(self):
        """Limpa campos de carro"""
        self.entry_marca_carro.delete(0, tk.END)
        self.entry_modelo_carro.delete(0, tk.END)
        self.entry_ano_carro.delete(0, tk.END)
        self.entry_placa_carro.delete(0, tk.END)
    
    def adicionar_carro(self):
        """Adiciona um carro ao cliente selecionado"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente primeiro!")
            return
        
        marca = self.entry_marca_carro.get().strip()
        modelo = self.entry_modelo_carro.get().strip()
        ano = self.entry_ano_carro.get().strip()
        placa = self.entry_placa_carro.get().strip()
        
        if not all([marca, modelo, ano, placa]):
            messagebox.showwarning("Aviso", "Preencha todos os campos do carro!")
            return
        
        try:
            int(ano)
        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser um número!")
            return
        
        carro = self.gerenciador.adicionar_carro(self.cliente_selecionado, marca, modelo, ano, placa)
        
        if carro:
            messagebox.showinfo("Sucesso", "Carro adicionado com sucesso!")
            self.limpar_campos_carro()
            self.atualizar_lista_carros()
            self.atualizar_lista_clientes()  # Atualizar contagem de carros
        else:
            messagebox.showerror("Erro", "Erro ao adicionar carro!")
    
    def deletar_carro(self):
        """Deleta um carro selecionado"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente primeiro!")
            return
        
        selecionado = self.tree_carros.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um carro para deletar!")
            return
        
        carro_id = selecionado[0]
        
        if messagebox.askyesno("Confirmar", "Deletar este carro e todos seus serviços?"):
            if self.gerenciador.deletar_carro(self.cliente_selecionado, carro_id):
                messagebox.showinfo("Sucesso", "Carro deletado com sucesso!")
                self.atualizar_lista_carros()
                self.atualizar_lista_clientes()
            else:
                messagebox.showerror("Erro", "Erro ao deletar carro!")
    
    def adicionar_servico(self):
        """Adiciona um serviço a um carro"""
        if not self.cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente primeiro!")
            return
        
        selecionado = self.tree_carros.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um carro para adicionar serviço!")
            return
        
        carro_id = selecionado[0]
        servico = self.combo_servico.get()
        descricao = self.text_descricao_servico.get("1.0", tk.END).strip()
        
        if not servico:
            messagebox.showwarning("Aviso", "Selecione um tipo de serviço!")
            return
        
        srv = self.gerenciador.adicionar_servico(self.cliente_selecionado, carro_id, servico, descricao)
        
        if srv:
            messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso!")
            self.combo_servico.set("")
            self.text_descricao_servico.delete("1.0", tk.END)
        else:
            messagebox.showerror("Erro", "Erro ao adicionar serviço!")


def main():
    root = tk.Tk()
    interface = InterfaceClientes(root)
    root.mainloop()


if __name__ == "__main__":
    main()

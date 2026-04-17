import tkinter as tk
from tkinter import ttk, messagebox
from clientes import GerenciadorClientes

class InterfaceOficina:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Oficina - Gerenciamento de Clientes")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        self.gerenciador = GerenciadorClientes()
        
        # Estado de navegação
        self.cliente_atual = None
        self.carro_atual = None
        self.pagina_atual = "clientes"
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        # Criar frames principais
        self.criar_frames()
        self.mostrar_pagina_clientes()
    
    def criar_frames(self):
        """Cria os frames para cada página"""
        # Frame de cabeçalho com botões de navegação
        self.frame_header = ttk.Frame(self.root, padding="10")
        self.frame_header.pack(fill=tk.X, side=tk.TOP)
        
        # Frame de conteúdo (será substituído conforme a página)
        self.frame_conteudo = ttk.Frame(self.root, padding="10")
        self.frame_conteudo.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
    
    def criar_header(self, titulo, mostrar_voltar=False):
        """Cria o header com título e botão voltar se necessário"""
        # Limpar header anterior
        for widget in self.frame_header.winfo_children():
            widget.destroy()
        
        # Título
        lbl_titulo = ttk.Label(self.frame_header, text=titulo, font=("Arial", 14, "bold"))
        lbl_titulo.pack(side=tk.LEFT, padx=10)
        
        # Botão voltar
        if mostrar_voltar:
            btn_voltar = ttk.Button(self.frame_header, text="← Voltar", command=self.voltar)
            btn_voltar.pack(side=tk.RIGHT, padx=10)
        
        # Separador
        ttk.Separator(self.frame_header, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 0))
    
    def limpar_conteudo(self):
        """Limpa o frame de conteúdo"""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
    
    def voltar(self):
        """Volta para a página anterior"""
        if self.pagina_atual == "servicos":
            self.mostrar_pagina_carros()
        elif self.pagina_atual == "carros":
            self.mostrar_pagina_clientes()
    
    # ===== PÁGINA 1: CLIENTES =====
    def mostrar_pagina_clientes(self):
        """Exibe a página de clientes"""
        self.pagina_atual = "clientes"
        self.cliente_atual = None
        self.carro_atual = None
        
        self.limpar_conteudo()
        self.criar_header("👥 Gerenciar Clientes")
        
        # Frame para adicionar novo cliente
        frame_novo = ttk.LabelFrame(self.frame_conteudo, text="Novo Cliente", padding="10")
        frame_novo.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        frame_campos = ttk.Frame(frame_novo)
        frame_campos.pack(fill=tk.X)
        
        ttk.Label(frame_campos, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        entry_nome = ttk.Entry(frame_campos, width=40)
        entry_nome.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Telefone:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        entry_telefone = ttk.Entry(frame_campos, width=40)
        entry_telefone.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        frame_campos.columnconfigure(1, weight=1)
        
        def adicionar():
            nome = entry_nome.get().strip()
            telefone = entry_telefone.get().strip()
            
            if not nome or not telefone:
                messagebox.showwarning("Aviso", "Preencha nome e telefone!")
                return
            
            cliente = self.gerenciador.adicionar_cliente(nome, telefone)
            if cliente:
                messagebox.showinfo("Sucesso", "Cliente adicionado!")
                entry_nome.delete(0, tk.END)
                entry_telefone.delete(0, tk.END)
                self.atualizar_lista_clientes(tree_clientes)
                entry_nome.focus()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar cliente!")
        
        btn_adicionar = ttk.Button(frame_novo, text="➕ Adicionar Cliente", command=adicionar)
        btn_adicionar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Frame para lista de clientes
        frame_lista = ttk.LabelFrame(self.frame_conteudo, text="Clientes Cadastrados", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Treeview
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_clientes = ttk.Treeview(frame_tree, columns=("Nome", "Telefone", "Carros"), 
                                    height=14, show="tree headings", yscrollcommand=scrollbar.set)
        tree_clientes.column("#0", width=0, stretch=tk.NO)
        tree_clientes.column("Nome", anchor=tk.W, width=300)
        tree_clientes.column("Telefone", anchor=tk.CENTER, width=150)
        tree_clientes.column("Carros", anchor=tk.CENTER, width=80)
        
        tree_clientes.heading("Nome", text="Nome")
        tree_clientes.heading("Telefone", text="Telefone")
        tree_clientes.heading("Carros", text="Carros")
        
        scrollbar.config(command=tree_clientes.yview)
        tree_clientes.pack(fill=tk.BOTH, expand=True)
        
        self.atualizar_lista_clientes(tree_clientes)
        
        # Frame de botões
        frame_botoes = ttk.Frame(frame_lista)
        frame_botoes.pack(fill=tk.X, pady=(10, 0))
        
        def editar_cliente():
            selecionado = tree_clientes.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente!")
                return
            
            cliente_id = selecionado[0]
            cliente = self.gerenciador.obter_cliente(cliente_id)
            
            # Janela de edição
            janela = tk.Toplevel(self.root)
            janela.title("Editar Cliente")
            janela.geometry("400x220")
            janela.resizable(False, False)
            
            frame = ttk.Frame(janela, padding="15")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="✏️ Editar Cliente", font=("Arial", 12, "bold")).pack(pady=(0, 15))
            
            # Frame para Nome
            frame_nome = ttk.Frame(frame)
            frame_nome.pack(fill=tk.X, pady=5)
            ttk.Label(frame_nome, text="Nome:", width=12).pack(side=tk.LEFT)
            entry_nome_ed = ttk.Entry(frame_nome)
            entry_nome_ed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entry_nome_ed.insert(0, cliente['nome'])
            
            # Frame para Telefone
            frame_tel = ttk.Frame(frame)
            frame_tel.pack(fill=tk.X, pady=5)
            ttk.Label(frame_tel, text="Telefone:", width=12).pack(side=tk.LEFT)
            entry_tel_ed = ttk.Entry(frame_tel)
            entry_tel_ed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entry_tel_ed.insert(0, cliente['telefone'])
            
            def salvar():
                nome = entry_nome_ed.get().strip()
                tel = entry_tel_ed.get().strip()
                
                if not nome or not tel:
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
                    return
                
                if self.gerenciador.editar_cliente(cliente_id, nome, tel):
                    messagebox.showinfo("Sucesso", "Cliente editado!")
                    janela.destroy()
                    self.atualizar_lista_clientes(tree_clientes)
                else:
                    messagebox.showerror("Erro", "Erro ao editar cliente!")
            
            frame_btn = ttk.Frame(frame)
            frame_btn.pack(fill=tk.X, pady=(20, 0))
            
            ttk.Button(frame_btn, text="✓ Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_btn, text="✕ Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=5)
        
        def deletar_cliente():
            selecionado = tree_clientes.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente!")
                return
            
            cliente_id = selecionado[0]
            cliente = self.gerenciador.obter_cliente(cliente_id)
            
            if messagebox.askyesno("Confirmar", f"Deletar '{cliente['nome']}' e todos seus carros/serviços?"):
                if self.gerenciador.deletar_cliente(cliente_id):
                    messagebox.showinfo("Sucesso", "Cliente deletado!")
                    self.atualizar_lista_clientes(tree_clientes)
                else:
                    messagebox.showerror("Erro", "Erro ao deletar!")
        
        def entrar_cliente():
            selecionado = tree_clientes.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente!")
                return
            
            self.cliente_atual = selecionado[0]
            self.mostrar_pagina_carros()
        
        ttk.Button(frame_botoes, text="✏️ Editar", command=editar_cliente).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes, text="🗑️ Deletar", command=deletar_cliente).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes, text="➡️ Entrar em Carros", command=entrar_cliente).pack(side=tk.LEFT, padx=2)
    
    def atualizar_lista_clientes(self, tree):
        """Atualiza a lista de clientes na treeview"""
        tree.delete(*tree.get_children())
        clientes = self.gerenciador.obter_clientes()
        
        for cliente in clientes:
            num_carros = len(cliente['carros'])
            tree.insert("", tk.END, values=(cliente['nome'], cliente['telefone'], num_carros), 
                       iid=cliente['id'])
    
    # ===== PÁGINA 2: CARROS =====
    def mostrar_pagina_carros(self):
        """Exibe a página de carros do cliente"""
        self.pagina_atual = "carros"
        self.carro_atual = None
        
        if not self.cliente_atual:
            self.mostrar_pagina_clientes()
            return
        
        cliente = self.gerenciador.obter_cliente(self.cliente_atual)
        
        self.limpar_conteudo()
        self.criar_header(f"🚗 Carros de {cliente['nome']}", mostrar_voltar=True)
        
        # Frame para adicionar novo carro
        frame_novo = ttk.LabelFrame(self.frame_conteudo, text="Novo Carro", padding="10")
        frame_novo.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        frame_campos = ttk.Frame(frame_novo)
        frame_campos.pack(fill=tk.X)
        
        ttk.Label(frame_campos, text="Marca:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        entry_marca = ttk.Entry(frame_campos, width=35)
        entry_marca.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Modelo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        entry_modelo = ttk.Entry(frame_campos, width=35)
        entry_modelo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Ano:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        entry_ano = ttk.Entry(frame_campos, width=35)
        entry_ano.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Placa:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        entry_placa = ttk.Entry(frame_campos, width=35)
        entry_placa.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        frame_campos.columnconfigure(1, weight=1)
        
        def adicionar_carro():
            marca = entry_marca.get().strip()
            modelo = entry_modelo.get().strip()
            ano = entry_ano.get().strip()
            placa = entry_placa.get().strip()
            
            if not all([marca, modelo, ano, placa]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            try:
                int(ano)
            except ValueError:
                messagebox.showerror("Erro", "Ano deve ser número!")
                return
            
            carro = self.gerenciador.adicionar_carro(self.cliente_atual, marca, modelo, ano, placa)
            if carro:
                messagebox.showinfo("Sucesso", f"{marca} {modelo} adicionado!")
                entry_marca.delete(0, tk.END)
                entry_modelo.delete(0, tk.END)
                entry_ano.delete(0, tk.END)
                entry_placa.delete(0, tk.END)
                self.atualizar_lista_carros(tree_carros)
                entry_marca.focus()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar carro!")
        
        btn_adicionar = ttk.Button(frame_novo, text="➕ Adicionar Carro", command=adicionar_carro)
        btn_adicionar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Frame para lista de carros
        frame_lista = ttk.LabelFrame(self.frame_conteudo, text="Carros Cadastrados", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=0, pady=(5, 0))
        
        # Treeview
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_carros = ttk.Treeview(frame_tree, columns=("Marca", "Modelo", "Ano", "Placa", "Serviços"), 
                                  height=12, show="tree headings", yscrollcommand=scrollbar.set)
        tree_carros.column("#0", width=0, stretch=tk.NO)
        tree_carros.column("Marca", anchor=tk.W, width=120)
        tree_carros.column("Modelo", anchor=tk.W, width=120)
        tree_carros.column("Ano", anchor=tk.CENTER, width=80)
        tree_carros.column("Placa", anchor=tk.CENTER, width=100)
        tree_carros.column("Serviços", anchor=tk.CENTER, width=80)
        
        tree_carros.heading("Marca", text="Marca")
        tree_carros.heading("Modelo", text="Modelo")
        tree_carros.heading("Ano", text="Ano")
        tree_carros.heading("Placa", text="Placa")
        tree_carros.heading("Serviços", text="Serviços")
        
        scrollbar.config(command=tree_carros.yview)
        tree_carros.pack(fill=tk.BOTH, expand=True)
        
        self.atualizar_lista_carros(tree_carros)
        
        # Frame de botões
        frame_botoes = ttk.Frame(frame_lista)
        frame_botoes.pack(fill=tk.X, pady=(10, 0))
        
        def editar_carro():
            selecionado = tree_carros.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um carro!")
                return
            
            carro_id = selecionado[0]
            carros = self.gerenciador.obter_carros_cliente(self.cliente_atual)
            carro = None
            for c in carros:
                if c['id'] == carro_id:
                    carro = c
                    break
            
            if not carro:
                return
            
            # Janela de edição
            janela = tk.Toplevel(self.root)
            janela.title("Editar Carro")
            janela.geometry("450x300")
            janela.resizable(False, False)
            
            frame = ttk.Frame(janela, padding="15")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="✏️ Editar Carro", font=("Arial", 12, "bold")).pack(pady=(0, 15))
            
            # Frame para Marca
            frame_marca = ttk.Frame(frame)
            frame_marca.pack(fill=tk.X, pady=5)
            ttk.Label(frame_marca, text="Marca:", width=12).pack(side=tk.LEFT)
            entry_marca_ed = ttk.Entry(frame_marca)
            entry_marca_ed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entry_marca_ed.insert(0, carro['marca'])
            
            # Frame para Modelo
            frame_modelo = ttk.Frame(frame)
            frame_modelo.pack(fill=tk.X, pady=5)
            ttk.Label(frame_modelo, text="Modelo:", width=12).pack(side=tk.LEFT)
            entry_modelo_ed = ttk.Entry(frame_modelo)
            entry_modelo_ed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entry_modelo_ed.insert(0, carro['modelo'])
            
            # Frame para Ano
            frame_ano = ttk.Frame(frame)
            frame_ano.pack(fill=tk.X, pady=5)
            ttk.Label(frame_ano, text="Ano:", width=12).pack(side=tk.LEFT)
            entry_ano_ed = ttk.Entry(frame_ano, width=10)
            entry_ano_ed.pack(side=tk.LEFT, padx=5)
            entry_ano_ed.insert(0, carro['ano'])
            
            # Frame para Placa
            frame_placa = ttk.Frame(frame)
            frame_placa.pack(fill=tk.X, pady=5)
            ttk.Label(frame_placa, text="Placa:", width=12).pack(side=tk.LEFT)
            entry_placa_ed = ttk.Entry(frame_placa, width=15)
            entry_placa_ed.pack(side=tk.LEFT, padx=5)
            entry_placa_ed.insert(0, carro['placa'])
            
            def salvar():
                marca = entry_marca_ed.get().strip()
                modelo = entry_modelo_ed.get().strip()
                ano = entry_ano_ed.get().strip()
                placa = entry_placa_ed.get().strip()
                
                if not all([marca, modelo, ano, placa]):
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
                    return
                
                try:
                    int(ano)
                except ValueError:
                    messagebox.showerror("Erro", "Ano deve ser número!")
                    return
                
                # Atualizar carro
                if self.gerenciador.editar_carro(self.cliente_atual, carro_id, marca, modelo, ano, placa):
                    messagebox.showinfo("Sucesso", "Carro editado!")
                    janela.destroy()
                    self.atualizar_lista_carros(tree_carros)
                else:
                    messagebox.showerror("Erro", "Erro ao editar!")
            
            frame_btn = ttk.Frame(frame)
            frame_btn.pack(fill=tk.X, pady=(20, 0))
            
            ttk.Button(frame_btn, text="✓ Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_btn, text="✕ Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=5)
        
        def deletar_carro():
            selecionado = tree_carros.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um carro!")
                return
            
            carro_id = selecionado[0]
            if messagebox.askyesno("Confirmar", "Deletar este carro e seus serviços?"):
                if self.gerenciador.deletar_carro(self.cliente_atual, carro_id):
                    messagebox.showinfo("Sucesso", "Carro deletado!")
                    self.atualizar_lista_carros(tree_carros)
                else:
                    messagebox.showerror("Erro", "Erro ao deletar!")
        
        def entrar_carro():
            selecionado = tree_carros.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um carro!")
                return
            
            self.carro_atual = selecionado[0]
            self.mostrar_pagina_servicos()
        
        ttk.Button(frame_botoes, text="✏️ Editar", command=editar_carro).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes, text="🗑️ Deletar", command=deletar_carro).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes, text="➡️ Ver Serviços", command=entrar_carro).pack(side=tk.LEFT, padx=2)
    
    def atualizar_lista_carros(self, tree):
        """Atualiza a lista de carros"""
        tree.delete(*tree.get_children())
        carros = self.gerenciador.obter_carros_cliente(self.cliente_atual)
        
        for carro in carros:
            num_servicos = len(carro['servicos'])
            tree.insert("", tk.END, 
                       values=(carro['marca'], carro['modelo'], carro['ano'], carro['placa'], num_servicos),
                       iid=carro['id'])
    
    def editar_carro(self, cliente_id, carro_id, marca, modelo, ano, placa):
        """Edita um carro - método faltante"""
        try:
            clientes = self.gerenciador._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            carro['marca'] = marca
                            carro['modelo'] = modelo
                            carro['ano'] = ano
                            carro['placa'] = placa
                            self.gerenciador._salvar_clientes(clientes)
                            return True
            
            return False
        except Exception as e:
            print(f"Erro ao editar carro: {e}")
            return False
    
    # Adicionar método ao gerenciador
    def _setup_gerenciador(self):
        """Adiciona método editar_carro ao gerenciador"""
        self.gerenciador.editar_carro = self.editar_carro.__get__(self.gerenciador, type(self.gerenciador))
    
    # ===== PÁGINA 3: SERVIÇOS =====
    def mostrar_pagina_servicos(self):
        """Exibe a página de serviços do carro"""
        self.pagina_atual = "servicos"
        
        if not self.cliente_atual or not self.carro_atual:
            self.mostrar_pagina_carros()
            return
        
        cliente = self.gerenciador.obter_cliente(self.cliente_atual)
        carros = self.gerenciador.obter_carros_cliente(self.cliente_atual)
        
        carro = None
        for c in carros:
            if c['id'] == self.carro_atual:
                carro = c
                break
        
        if not carro:
            self.mostrar_pagina_carros()
            return
        
        self.limpar_conteudo()
        self.criar_header(f"🔧 Serviços: {carro['marca']} {carro['modelo']} ({carro['placa']})", 
                         mostrar_voltar=True)
        
        # Frame para adicionar novo serviço
        frame_novo = ttk.LabelFrame(self.frame_conteudo, text="Novo Serviço", padding="10")
        frame_novo.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        frame_campos = ttk.Frame(frame_novo)
        frame_campos.pack(fill=tk.X)
        
        ttk.Label(frame_campos, text="Tipo de Serviço:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        combo_servico = ttk.Combobox(frame_campos, width=40, state="readonly",
                                    values=self.gerenciador.get_tipos_servico())
        combo_servico.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_campos, text="Descrição (opcional):").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        text_desc = tk.Text(frame_campos, width=40, height=3, font=("Arial", 10))
        text_desc.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        frame_campos.columnconfigure(1, weight=1)
        
        def adicionar_servico():
            servico = combo_servico.get()
            desc = text_desc.get("1.0", tk.END).strip()
            
            if not servico:
                messagebox.showwarning("Aviso", "Selecione um tipo de serviço!")
                return
            
            srv = self.gerenciador.adicionar_servico(self.cliente_atual, self.carro_atual, servico, desc)
            if srv:
                messagebox.showinfo("Sucesso", "Serviço adicionado!")
                combo_servico.set("")
                text_desc.delete("1.0", tk.END)
                self.atualizar_lista_servicos(tree_servicos)
                combo_servico.focus()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar serviço!")
        
        btn_adicionar = ttk.Button(frame_novo, text="➕ Adicionar Serviço", command=adicionar_servico)
        btn_adicionar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Frame para lista de serviços
        frame_lista = ttk.LabelFrame(self.frame_conteudo, text="Serviços Cadastrados", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Treeview
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_servicos = ttk.Treeview(frame_tree, columns=("Serviço", "Descrição", "Data"), 
                                    height=10, show="tree headings", yscrollcommand=scrollbar.set)
        tree_servicos.column("#0", width=0, stretch=tk.NO)
        tree_servicos.column("Serviço", anchor=tk.W, width=200)
        tree_servicos.column("Descrição", anchor=tk.W, width=350)
        tree_servicos.column("Data", anchor=tk.CENTER, width=120)
        
        tree_servicos.heading("Serviço", text="Serviço")
        tree_servicos.heading("Descrição", text="Descrição")
        tree_servicos.heading("Data", text="Data")
        
        scrollbar.config(command=tree_servicos.yview)
        tree_servicos.pack(fill=tk.BOTH, expand=True)
        
        self.atualizar_lista_servicos(tree_servicos)
        
        # Frame de botões
        frame_botoes = ttk.Frame(frame_lista)
        frame_botoes.pack(fill=tk.X, pady=(10, 0))
        
        def editar_servico():
            selecionado = tree_servicos.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um serviço!")
                return
            
            servico_id = selecionado[0]
            servicos = self.gerenciador.obter_servicos_carro(self.cliente_atual, self.carro_atual)
            servico_atual = None
            for s in servicos:
                if s['id'] == servico_id:
                    servico_atual = s
                    break
            
            if not servico_atual:
                messagebox.showerror("Erro", "Serviço não encontrado!")
                return
            
            # Criar janela modal para editar
            janela_edit = tk.Toplevel(self.root)
            janela_edit.title("Editar Serviço")
            janela_edit.geometry("500x300")
            janela_edit.resizable(False, False)
            
            ttk.Label(janela_edit, text="Tipo de Serviço:", font=("Arial", 10)).pack(padx=10, pady=(10, 0), anchor=tk.W)
            combo_servico = ttk.Combobox(janela_edit, width=50, state="readonly",
                                        values=self.gerenciador.get_tipos_servico())
            combo_servico.set(servico_atual['servico'])
            combo_servico.pack(padx=10, pady=(0, 10))
            
            ttk.Label(janela_edit, text="Descrição:", font=("Arial", 10)).pack(padx=10, pady=(0, 0), anchor=tk.W)
            text_desc = tk.Text(janela_edit, width=50, height=8, font=("Arial", 10))
            text_desc.pack(padx=10, pady=(0, 10))
            text_desc.insert("1.0", servico_atual['descricao'])
            
            def salvar_edicao():
                novo_servico = combo_servico.get()
                nova_desc = text_desc.get("1.0", tk.END).strip()
                
                if not novo_servico:
                    messagebox.showwarning("Aviso", "Selecione um tipo de serviço!")
                    return
                
                if self.gerenciador.editar_servico(self.cliente_atual, self.carro_atual, servico_id, novo_servico, nova_desc):
                    messagebox.showinfo("Sucesso", "Serviço atualizado!")
                    self.atualizar_lista_servicos(tree_servicos)
                    janela_edit.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar serviço!")
            
            frame_botoes_edit = ttk.Frame(janela_edit)
            frame_botoes_edit.pack(fill=tk.X, padx=10, pady=10)
            ttk.Button(frame_botoes_edit, text="✓ Salvar", command=salvar_edicao).pack(side=tk.LEFT, padx=2)
            ttk.Button(frame_botoes_edit, text="✕ Cancelar", command=janela_edit.destroy).pack(side=tk.LEFT, padx=2)
        
        def deletar_servico():
            selecionado = tree_servicos.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um serviço!")
                return
            
            servico_id = selecionado[0]
            if messagebox.askyesno("Confirmar", "Deletar este serviço?"):
                if self.gerenciador.deletar_servico(self.cliente_atual, self.carro_atual, servico_id):
                    messagebox.showinfo("Sucesso", "Serviço deletado!")
                    self.atualizar_lista_servicos(tree_servicos)
                else:
                    messagebox.showerror("Erro", "Erro ao deletar!")
        
        ttk.Button(frame_botoes, text="✎ Editar", command=editar_servico).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botoes, text="🗑️ Deletar", command=deletar_servico).pack(side=tk.LEFT, padx=2)
    
    def atualizar_lista_servicos(self, tree):
        """Atualiza a lista de serviços"""
        tree.delete(*tree.get_children())
        servicos = self.gerenciador.obter_servicos_carro(self.cliente_atual, self.carro_atual)
        
        for servico in servicos:
            tree.insert("", tk.END, 
                       values=(servico['servico'], servico['descricao'], servico['data']),
                       iid=servico['id'])


def main():
    root = tk.Tk()
    app = InterfaceOficina(root)
    # Adicionar método editar_carro ao gerenciador
    app._setup_gerenciador()
    app.gerenciador.editar_carro = app.editar_carro
    root.mainloop()


if __name__ == "__main__":
    main()

import json
import os
from datetime import datetime

class GerenciadorClientes:
    """Gerencia clientes e seus carros"""
    
    def __init__(self):
        self.arquivo_clientes = "clientes.json"
        self.tipos_servico = [
            "Troca de Óleo",
            "Troca de Filtro de Ar",
            "Balanceamento de Pneus",
            "Alinhamento",
            "Troca de Pneus",
            "Revisão Geral",
            "Reparo do Motor",
            "Reparo de Freios",
            "Ar Condicionado",
            "Elétrica",
            "Suspensão",
            "Outro"
        ]
        self.inicializar_arquivo()
    
    def inicializar_arquivo(self):
        """Inicializa o arquivo JSON se não existir"""
        if not os.path.exists(self.arquivo_clientes):
            try:
                with open(self.arquivo_clientes, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Erro ao criar arquivo JSON: {e}")
    
    def get_tipos_servico(self):
        """Retorna lista de tipos de serviço"""
        return self.tipos_servico
    
    def adicionar_cliente(self, nome, telefone):
        """
        Adiciona um novo cliente
        
        Args:
            nome (str): Nome do cliente
            telefone (str): Telefone do cliente
        
        Returns:
            dict: Cliente criado ou None se falhar
        """
        if not nome or not telefone:
            return None
        
        try:
            clientes = self._ler_clientes()
            
            # Verificar se cliente já existe
            for cliente in clientes:
                if cliente['nome'].lower() == nome.lower() and cliente['telefone'] == telefone:
                    return None  # Cliente já existe
            
            novo_cliente = {
                'id': self._gerar_id(),
                'nome': nome,
                'telefone': telefone,
                'carros': [],
                'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            clientes.append(novo_cliente)
            self._salvar_clientes(clientes)
            return novo_cliente
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            return None
    
    def obter_clientes(self):
        """Retorna lista de todos os clientes"""
        return self._ler_clientes()
    
    def obter_cliente(self, cliente_id):
        """Obtém um cliente específico pelo ID"""
        clientes = self._ler_clientes()
        for cliente in clientes:
            if cliente['id'] == cliente_id:
                return cliente
        return None
    
    def editar_cliente(self, cliente_id, nome, telefone):
        """Edita dados de um cliente"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    cliente['nome'] = nome
                    cliente['telefone'] = telefone
                    self._salvar_clientes(clientes)
                    return True
            
            return False
        except Exception as e:
            print(f"Erro ao editar cliente: {e}")
            return False
    
    def deletar_cliente(self, cliente_id):
        """Deleta um cliente e todos seus carros"""
        try:
            clientes = self._ler_clientes()
            clientes = [c for c in clientes if c['id'] != cliente_id]
            self._salvar_clientes(clientes)
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            return False
    
    def adicionar_carro(self, cliente_id, marca, modelo, ano, placa):
        """Adiciona um carro a um cliente"""
        if not all([cliente_id, marca, modelo, ano, placa]):
            return None
        
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    novo_carro = {
                        'id': self._gerar_id(),
                        'marca': marca,
                        'modelo': modelo,
                        'ano': ano,
                        'placa': placa,
                        'servicos': [],
                        'data_adicao': datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    cliente['carros'].append(novo_carro)
                    self._salvar_clientes(clientes)
                    return novo_carro
            
            return None
        except Exception as e:
            print(f"Erro ao adicionar carro: {e}")
            return None
    
    def obter_carros_cliente(self, cliente_id):
        """Obtém todos os carros de um cliente"""
        cliente = self.obter_cliente(cliente_id)
        return cliente['carros'] if cliente else []
    
    def deletar_carro(self, cliente_id, carro_id):
        """Deleta um carro de um cliente"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    cliente['carros'] = [c for c in cliente['carros'] if c['id'] != carro_id]
                    self._salvar_clientes(clientes)
                    return True
            
            return False
        except Exception as e:
            print(f"Erro ao deletar carro: {e}")
            return False
    
    def adicionar_servico(self, cliente_id, carro_id, servico, descricao=""):
        """Adiciona um serviço a um carro"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            novo_servico = {
                                'id': self._gerar_id(),
                                'servico': servico,
                                'descricao': descricao,
                                'data': datetime.now().strftime("%d/%m/%Y %H:%M")
                            }
                            carro['servicos'].append(novo_servico)
                            self._salvar_clientes(clientes)
                            return novo_servico
            
            return None
        except Exception as e:
            print(f"Erro ao adicionar serviço: {e}")
            return None
    
    def obter_servicos_carro(self, cliente_id, carro_id):
        """Obtém todos os serviços de um carro"""
        cliente = self.obter_cliente(cliente_id)
        if cliente:
            for carro in cliente['carros']:
                if carro['id'] == carro_id:
                    return carro['servicos']
        return []
    
    def editar_servico(self, cliente_id, carro_id, servico_id, servico, descricao=""):
        """Edita um serviço"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            for srv in carro['servicos']:
                                if srv['id'] == servico_id:
                                    srv['servico'] = servico
                                    srv['descricao'] = descricao
                                    self._salvar_clientes(clientes)
                                    return True
            
            return False
        except Exception as e:
            print(f"Erro ao editar serviço: {e}")
            return False
    
    def deletar_servico(self, cliente_id, carro_id, servico_id):
        """Deleta um serviço"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            carro['servicos'] = [s for s in carro['servicos'] if s['id'] != servico_id]
                            self._salvar_clientes(clientes)
                            return True
            
            return False
        except Exception as e:
            print(f"Erro ao deletar serviço: {e}")
            return False
    
    # Métodos privados
    def _ler_clientes(self):
        """Lê clientes do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_clientes):
                with open(self.arquivo_clientes, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao ler clientes: {e}")
        
        return []
    
    def _salvar_clientes(self, clientes):
        """Salva clientes no arquivo JSON"""
        try:
            with open(self.arquivo_clientes, 'w', encoding='utf-8') as f:
                json.dump(clientes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar clientes: {e}")
    
    def _gerar_id(self):
        """Gera um ID único"""
        import uuid
        return str(uuid.uuid4())[:8]

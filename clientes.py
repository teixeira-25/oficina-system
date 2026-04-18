import json
import os
from datetime import datetime
import pandas as pd
import uuid

try:
    import streamlit as st
    from streamlit_gsheets import GSheetsConnection
except ImportError:
    st = None

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
        self.conn = None
        self.sheet_url = st.secrets.get("connections", {}).get("gsheets", {}).get("spreadsheet", None) if st else None
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
        """Deleta um cliente e todos seus carros e serviços (exclusão em cascata)"""
        try:
            clientes = self._ler_clientes()
            tamanho_original = len(clientes)
            clientes = [c for c in clientes if c['id'] != cliente_id]
            
            if len(clientes) < tamanho_original:
                self._salvar_clientes(clientes)
                return True
            return False # Cliente não encontrado
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
    
    def editar_carro(self, cliente_id, carro_id, marca, modelo, ano, placa):
        """Edita um carro de um cliente"""
        try:
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            carro['marca'] = marca
                            carro['modelo'] = modelo
                            carro['ano'] = ano
                            carro['placa'] = placa
                            self._salvar_clientes(clientes)
                            return True
            
            return False
        except Exception as e:
            print(f"Erro ao editar carro: {e}")
            return False
    
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
    
    def adicionar_servico(self, cliente_id, carro_id, servico, descricao="", pecas=None):
        """Adiciona um serviço a um carro"""
        try:
            pecas_normalizadas = self._normalizar_pecas(pecas)
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            novo_servico = {
                                'id': self._gerar_id(),
                                'servico': servico,
                                'descricao': descricao,
                                'pecas': pecas_normalizadas,
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
    
    def editar_servico(self, cliente_id, carro_id, servico_id, servico, descricao="", pecas=None):
        """Edita um serviço"""
        try:
            pecas_normalizadas = self._normalizar_pecas(pecas)
            clientes = self._ler_clientes()
            
            for cliente in clientes:
                if cliente['id'] == cliente_id:
                    for carro in cliente['carros']:
                        if carro['id'] == carro_id:
                            for srv in carro['servicos']:
                                if srv['id'] == servico_id:
                                    srv['servico'] = servico
                                    srv['descricao'] = descricao
                                    srv['pecas'] = pecas_normalizadas
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
    
    def limpar_banco_dados(self):
        """Remove todos os dados do sistema (Local e Google Sheets)"""
        try:
            self._salvar_clientes([])
            return True
        except Exception as e:
            print(f"Erro ao limpar banco de dados: {e}")
            return False

    # Métodos privados
    def _ler_clientes(self):
        """Lê clientes do arquivo JSON"""
        if st and self.sheet_url:
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read(ttl=0)
                if df is not None and not df.empty:
                    clientes_dict = {}
                    for _, row in df.iterrows():
                        c_id = str(row.get('cliente_id', ''))
                        if not c_id or pd.isna(c_id): continue
                        
                        if c_id not in clientes_dict:
                            clientes_dict[c_id] = {
                                'id': c_id, 'nome': row.get('cliente_nome', ''),
                                'telefone': str(row.get('cliente_telefone', '')),
                                'carros': [], 'data_criacao': row.get('cliente_data_criacao', '')
                            }
                        
                        v_id = str(row.get('carro_id', ''))
                        if v_id and not pd.isna(v_id):
                            carro = next((c for c in clientes_dict[c_id]['carros'] if c['id'] == v_id), None)
                            if not carro:
                                carro = {
                                    'id': v_id, 'marca': row.get('carro_marca', ''),
                                    'modelo': row.get('carro_modelo', ''), 'ano': str(row.get('carro_ano', '')),
                                    'placa': row.get('carro_placa', ''), 'servicos': [],
                                    'data_adicao': row.get('carro_data_adicao', '')
                                }
                                clientes_dict[c_id]['carros'].append(carro)
                            
                            s_id = str(row.get('servico_id', ''))
                            if s_id and not pd.isna(s_id):
                                if not any(s['id'] == s_id for s in carro['servicos']):
                                    carro['servicos'].append({
                                        'id': s_id, 'servico': row.get('servico_tipo', ''),
                                        'descricao': row.get('servico_descricao', ''),
                                        'pecas': json.loads(row.get('servico_pecas_json', '[]')),
                                        'data': row.get('servico_data', '')
                                    })
                    return list(clientes_dict.values())
            except Exception as e:
                print(f"Erro ao ler do Google Sheets: {e}")

        try:
            if os.path.exists(self.arquivo_clientes):
                with open(self.arquivo_clientes, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao ler clientes: {e}")
        
        return []
    
    def _salvar_clientes(self, clientes):
        """Salva clientes no arquivo JSON"""
        if st and self.sheet_url:
            try:
                dados_planilha = []
                for c in clientes:
                    if not c['carros']:
                        dados_planilha.append({
                            'cliente_id': c['id'], 'cliente_nome': c['nome'], 'cliente_telefone': c['telefone'], 'cliente_data_criacao': c.get('data_criacao', ''),
                            'carro_id': '', 'carro_marca': '', 'carro_modelo': '', 'carro_ano': '', 'carro_placa': '', 'carro_data_adicao': '',
                            'servico_id': '', 'servico_tipo': '', 'servico_descricao': '', 'servico_data': '', 'servico_pecas_json': '[]'
                        })
                    for car in c['carros']:
                        if not car['servicos']:
                            dados_planilha.append({
                                'cliente_id': c['id'], 'cliente_nome': c['nome'], 'cliente_telefone': c['telefone'], 'cliente_data_criacao': c.get('data_criacao', ''),
                                'carro_id': car['id'], 'carro_marca': car['marca'], 'carro_modelo': car['modelo'], 'carro_ano': car['ano'], 'carro_placa': car['placa'], 'carro_data_adicao': car.get('data_adicao', ''),
                                'servico_id': '', 'servico_tipo': '', 'servico_descricao': '', 'servico_data': '', 'servico_pecas_json': '[]'
                            })
                        for srv in car['servicos']:
                            dados_planilha.append({
                                'cliente_id': c['id'], 'cliente_nome': c['nome'], 'cliente_telefone': c['telefone'], 'cliente_data_criacao': c.get('data_criacao', ''),
                                'carro_id': car['id'], 'carro_marca': car['marca'], 'carro_modelo': car['modelo'], 'carro_ano': car['ano'], 'carro_placa': car['placa'], 'carro_data_adicao': car.get('data_adicao', ''),
                                'servico_id': srv['id'], 'servico_tipo': srv['servico'], 'servico_descricao': srv.get('descricao', ''), 'servico_data': srv['data'],
                                'servico_pecas_json': json.dumps(srv.get('pecas', []), ensure_ascii=False)
                            })
                
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_final = pd.DataFrame(dados_planilha)
                conn.update(data=df_final)
            except Exception as e:
                print(f"Erro ao salvar no Google Sheets: {e}")

        try:
            with open(self.arquivo_clientes, 'w', encoding='utf-8') as f:
                json.dump(clientes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar clientes: {e}")
    
    def _gerar_id(self):
        """Gera um ID único"""
        return str(uuid.uuid4())[:8]

    def _normalizar_pecas(self, pecas):
        """Normaliza a lista de peças para persistência estável."""
        pecas_normalizadas = []
        if not pecas:
            return pecas_normalizadas

        for peca in pecas:
            nome = str(peca.get('nome', '')).strip()
            preco = peca.get('preco', 0)
            quantidade = peca.get('quantidade', 1)

            if not nome:
                continue

            try:
                preco_float = round(float(preco), 2)
            except (TypeError, ValueError):
                preco_float = 0.0

            try:
                quantidade_int = int(quantidade)
            except (TypeError, ValueError):
                quantidade_int = 1

            if preco_float < 0:
                preco_float = 0.0
            if quantidade_int <= 0:
                quantidade_int = 1

            pecas_normalizadas.append({
                'nome': nome,
                'preco': preco_float,
                'quantidade': quantidade_int,
                'total': round(preco_float * quantidade_int, 2),
            })

        return pecas_normalizadas
    
    # ==================== FUNÇÕES DE RELATÓRIO ====================
    
    def obter_todos_servicos(self):
        """
        Retorna lista de todos os serviços com informações do cliente e carro
        
        Returns:
            list: Lista de serviços com contexto
        """
        try:
            clientes = self._ler_clientes()
            todos_servicos = []
            
            for cliente in clientes:
                for carro in cliente['carros']:
                    for servico in carro['servicos']:
                        pecas = servico.get('pecas', [])
                        valor_pecas = round(sum(float(peca.get('total', peca.get('preco', 0)) or 0) for peca in pecas), 2)
                        todos_servicos.append({
                            'servico_id': servico['id'],
                            'servico_tipo': servico['servico'],
                            'descricao': servico.get('descricao', ''),
                            'pecas': pecas,
                            'total_pecas': len(pecas),
                            'valor_pecas': valor_pecas,
                            'data': servico['data'],
                            'cliente_nome': cliente['nome'],
                            'cliente_telefone': cliente['telefone'],
                            'cliente_id': cliente['id'],
                            'carro_marca': carro['marca'],
                            'carro_modelo': carro['modelo'],
                            'carro_placa': carro['placa'],
                            'carro_ano': carro['ano']
                        })
            
            # Ordenar por data decrescente
            todos_servicos.sort(key=lambda x: datetime.strptime(x['data'], "%d/%m/%Y %H:%M"), reverse=True)
            return todos_servicos
        except Exception as e:
            print(f"Erro ao obter todos os serviços: {e}")
            return []
    
    def obter_servicos_por_periodo(self, mes, ano):
        """
        Retorna serviços de um período específico
        
        Args:
            mes (int): Mês (1-12)
            ano (int): Ano
        
        Returns:
            list: Serviços do período
        """
        try:
            todos_servicos = self.obter_todos_servicos()
            servicos_periodo = []
            
            for servico in todos_servicos:
                data_obj = datetime.strptime(servico['data'], "%d/%m/%Y %H:%M")
                if data_obj.month == mes and data_obj.year == ano:
                    servicos_periodo.append(servico)
            
            return servicos_periodo
        except Exception as e:
            print(f"Erro ao obter serviços por período: {e}")
            return []
    
    def gerar_relatorio_mensal(self, mes, ano):
        """
        Gera relatório completo do mês
        
        Args:
            mes (int): Mês (1-12)
            ano (int): Ano
        
        Returns:
            dict: Estatísticas do mês
        """
        try:
            servicos = self.obter_servicos_por_periodo(mes, ano)
            
            # Contar por tipo de serviço
            contagem_tipos = {}
            for servico in servicos:
                tipo = servico['servico_tipo']
                contagem_tipos[tipo] = contagem_tipos.get(tipo, 0) + 1
            
            # Contar por cliente
            contagem_clientes = {}
            for servico in servicos:
                cliente = servico['cliente_nome']
                contagem_clientes[cliente] = contagem_clientes.get(cliente, 0) + 1
            
            return {
                'mes': mes,
                'ano': ano,
                'total_servicos': len(servicos),
                'tipos_servico': contagem_tipos,
                'clientes': contagem_clientes,
                'servicos': servicos
            }
        except Exception as e:
            print(f"Erro ao gerar relatório mensal: {e}")
            return None
    
    def obter_meses_com_dados(self):
        """
        Retorna lista de (mes, ano) que possuem serviços
        
        Returns:
            list: Lista de tuplas (mes, ano)
        """
        try:
            todos_servicos = self.obter_todos_servicos()
            periodos = set()
            
            for servico in todos_servicos:
                data_obj = datetime.strptime(servico['data'], "%d/%m/%Y %H:%M")
                periodos.add((data_obj.month, data_obj.year))
            
            # Ordenar decrescente (mais recente primeiro)
            periodos_lista = sorted(list(periodos), key=lambda x: (x[1], x[0]), reverse=True)
            return periodos_lista
        except Exception as e:
            print(f"Erro ao obter meses com dados: {e}")
            return []

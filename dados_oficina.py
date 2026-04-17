import csv
from datetime import datetime
import os

class OficinaApp:
    def __init__(self):
        """Inicializa a aplicação da oficina"""
        self.arquivo_csv = "registros.csv"
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
        """Inicializa o arquivo CSV se não existir"""
        if not os.path.exists(self.arquivo_csv):
            try:
                with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Marca", "Modelo", "Ano", "Placa", "Serviço", "Descrição", "Data"])
            except Exception as e:
                print(f"Erro ao criar arquivo CSV: {e}")
    
    def get_tipos_servico(self):
        """Retorna a lista de tipos de serviço"""
        return self.tipos_servico
    
    def adicionar_registro(self, marca, modelo, ano, placa, servico, descricao=""):
        """
        Adiciona um novo registro ao arquivo CSV
        
        Args:
            marca (str): Marca do carro
            modelo (str): Modelo do carro
            ano (str): Ano do carro
            placa (str): Placa do carro
            servico (str): Tipo de serviço
            descricao (str): Descrição adicional do serviço
        
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([marca, modelo, ano, placa, servico, descricao, data_atual])
            
            return True
        except Exception as e:
            print(f"Erro ao salvar registro: {e}")
            return False
    
    def obter_registros(self):
        """
        Obtém todos os registros do arquivo CSV
        
        Returns:
            list: Lista de tuplas com os registros
        """
        registros = []
        try:
            if os.path.exists(self.arquivo_csv):
                with open(self.arquivo_csv, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Pular cabeçalho
                    for row in reader:
                        if row:  # Pular linhas vazias
                            registros.append(tuple(row))
        except Exception as e:
            print(f"Erro ao ler registros: {e}")
        
        return registros
    
    def deletar_registro(self, indice):
        """
        Deleta um registro pelo índice
        
        Args:
            indice (int): Índice do registro a deletar
        
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        try:
            registros = self.obter_registros()
            if 0 <= indice < len(registros):
                registros.pop(indice)
                
                with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Marca", "Modelo", "Ano", "Placa", "Serviço", "Descrição", "Data"])
                    writer.writerows(registros)
                
                return True
        except Exception as e:
            print(f"Erro ao deletar registro: {e}")
        
        return False
    
    def editar_registro(self, indice, marca, modelo, ano, placa, servico, descricao=""):
        """
        Edita um registro existente
        
        Args:
            indice (int): Índice do registro a editar
            marca (str): Marca do carro
            modelo (str): Modelo do carro
            ano (str): Ano do carro
            placa (str): Placa do carro
            servico (str): Tipo de serviço
            descricao (str): Descrição adicional do serviço
        
        Returns:
            bool: True se editado com sucesso, False caso contrário
        """
        try:
            registros = self.obter_registros()
            if 0 <= indice < len(registros):
                # Manter a data original, apenas atualizar os dados
                data_original = registros[indice][6]
                novo_registro = [marca, modelo, ano, placa, servico, descricao, data_original]
                registros[indice] = tuple(novo_registro)
                
                with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Marca", "Modelo", "Ano", "Placa", "Serviço", "Descrição", "Data"])
                    writer.writerows(registros)
                
                return True
        except Exception as e:
            print(f"Erro ao editar registro: {e}")
        
        return False
    
    def obter_registros_por_placa(self, placa):
        """
        Obtém todos os registros de um carro específico
        
        Args:
            placa (str): Placa do carro
        
        Returns:
            list: Lista de tuplas com os registros
        """
        registros = self.obter_registros()
        return [r for r in registros if r[3] == placa]  # Placa está no índice 3

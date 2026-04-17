#!/usr/bin/env python3
"""
Teste rápido do sistema de clientes
"""

from clientes import GerenciadorClientes
import os

def test_sistema_clientes():
    print("=" * 60)
    print("TESTE - SISTEMA DE CLIENTES")
    print("=" * 60)
    
    # Limpar arquivo anterior
    if os.path.exists("clientes.json"):
        os.remove("clientes.json")
    
    gerenciador = GerenciadorClientes()
    
    # Teste 1: Adicionar cliente
    print("\n1️⃣ Adicionando clientes...")
    cliente1 = gerenciador.adicionar_cliente("João Silva", "11999999999")
    cliente2 = gerenciador.adicionar_cliente("Maria Santos", "21988888888")
    print(f"✅ Cliente 1: {cliente1['nome']}")
    print(f"✅ Cliente 2: {cliente2['nome']}")
    
    # Teste 2: Adicionar carros
    print("\n2️⃣ Adicionando carros...")
    carro1 = gerenciador.adicionar_carro(cliente1['id'], "Toyota", "Corolla", "2020", "ABC-1234")
    carro2 = gerenciador.adicionar_carro(cliente1['id'], "Honda", "Civic", "2019", "XYZ-5678")
    carro3 = gerenciador.adicionar_carro(cliente2['id'], "Ford", "Fiesta", "2021", "DEF-9012")
    print(f"✅ {cliente1['nome']} tem {len(gerenciador.obter_carros_cliente(cliente1['id']))} carros")
    print(f"✅ {cliente2['nome']} tem {len(gerenciador.obter_carros_cliente(cliente2['id']))} carro")
    
    # Teste 3: Adicionar serviços
    print("\n3️⃣ Adicionando serviços...")
    srv1 = gerenciador.adicionar_servico(cliente1['id'], carro1['id'], "Troca de Óleo", "Troca feita")
    srv2 = gerenciador.adicionar_servico(cliente1['id'], carro2['id'], "Alinhamento", "")
    print(f"✅ Serviço adicionado ao {carro1['marca']} {carro1['modelo']}: {srv1['servico']}")
    print(f"✅ Serviço adicionado ao {carro2['marca']} {carro2['modelo']}: {srv2['servico']}")
    
    # Teste 4: Validar estrutura
    print("\n4️⃣ Validando estrutura...")
    clientes = gerenciador.obter_clientes()
    print(f"Total de clientes: {len(clientes)}")
    for cliente in clientes:
        print(f"\n  👤 {cliente['nome']} ({cliente['telefone']})")
        print(f"     Carros: {len(cliente['carros'])}")
        for carro in cliente['carros']:
            print(f"       🚗 {carro['marca']} {carro['modelo']} - {carro['placa']}")
            print(f"          Serviços: {len(carro['servicos'])}")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    test_sistema_clientes()

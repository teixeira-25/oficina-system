#!/usr/bin/env python3
import json
import os
import csv
from clientes import GerenciadorClientes

def limpar_sistema():
    print("🧹 Iniciando limpeza completa do sistema...")

    gerenciador = GerenciadorClientes()

    # 1. Limpar via Gerenciador (Trata Google Sheets se estiver ativo)
    if gerenciador.sheet_url:
        print("🌐 Conexão com Google Sheets detectada.")
        confirmacao = input("Deseja apagar os dados também do Google Sheets? (S/N): ")
        if confirmacao.upper() == 'S':
            if gerenciador.limpar_banco_dados():
                print("✅ Dados removidos do Google Sheets.")
            else:
                print("❌ Falha ao limpar Google Sheets.")
    else:
        print("📝 Usando apenas armazenamento local.")

    # 2. Limpar clientes.json (Local)
    arquivo_clientes = "clientes.json"
    if os.path.exists(arquivo_clientes):
        os.remove(arquivo_clientes)
        print(f"✅ Arquivo local {arquivo_clientes} removido.")

    # 2. Limpar registros.csv (Base de dados legada/tkinter)
    arquivo_csv = "registros.csv"
    if os.path.exists(arquivo_csv):
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Marca", "Modelo", "Ano", "Placa", "Serviço", "Descrição", "Data"])
        print(f"✅ Arquivo {arquivo_csv} foi resetado (apenas cabeçalhos).")

if __name__ == "__main__":
    limpar_sistema()
    print("\n✨ O sistema agora está totalmente limpo e pronto para novos registros!")
#!/usr/bin/env python3
"""
Gera dados de teste para validar listagens extensas do sistema.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4


ARQUIVO_CLIENTES = Path("clientes.json")

TIPOS_SERVICO = [
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
    "Outro",
]

NOMES = [
    "João", "Maria", "Pedro", "Ana", "Carlos", "Fernanda", "Lucas", "Juliana",
    "Marcos", "Patrícia", "Bruno", "Camila", "Rafael", "Aline", "Gustavo", "Larissa",
    "Thiago", "Renata", "Felipe", "Bianca", "André", "Vanessa", "Rodrigo", "Tatiane",
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Costa", "Pereira", "Almeida",
    "Ferreira", "Rodrigues", "Gomes", "Martins", "Araújo", "Barbosa", "Rocha", "Dias",
]

MARCAS_MODELOS = {
    "Toyota": ["Corolla", "Hilux", "Yaris", "Etios"],
    "Honda": ["Civic", "HR-V", "Fit", "City"],
    "Volkswagen": ["Gol", "Polo", "T-Cross", "Virtus"],
    "Chevrolet": ["Onix", "Tracker", "Cruze", "S10"],
    "Fiat": ["Argo", "Mobi", "Toro", "Strada"],
    "Hyundai": ["HB20", "Creta", "i30", "Tucson"],
    "Ford": ["Ka", "Fiesta", "Ranger", "EcoSport"],
    "Renault": ["Kwid", "Sandero", "Logan", "Duster"],
}

DESCRICOES = [
    "Cliente solicitou verificacao geral.",
    "Ruido identificado durante teste rapido.",
    "Preventiva agendada para revisao completa.",
    "Peca substituida e sistema validado.",
    "Veiculo liberado apos checklist final.",
    "Ajuste realizado conforme orientacao do cliente.",
    "Retorno para acompanhamento em 15 dias.",
    "Servico executado sem observacoes adicionais.",
]


def gerar_id() -> str:
    return str(uuid4())[:8]


def gerar_nome(indice: int) -> str:
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)} Teste {indice:02d}"


def gerar_telefone(indice: int) -> str:
    return f"(85) 9{indice:04d}-{(indice * 37) % 10000:04d}"


def gerar_placa(indice_cliente: int, indice_carro: int) -> str:
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    prefixo = (
        letras[indice_cliente % 26]
        + letras[(indice_cliente + indice_carro + 3) % 26]
        + letras[(indice_cliente + indice_carro + 11) % 26]
    )
    return f"{prefixo}{indice_cliente % 10}{indice_carro % 10}{(indice_cliente + indice_carro) % 10}{(indice_cliente * 3 + indice_carro) % 10}"


def gerar_data(dias_atras: int) -> str:
    data = datetime.now() - timedelta(days=dias_atras, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return data.strftime("%d/%m/%Y %H:%M")


def gerar_servicos(indice_cliente: int, indice_carro: int) -> list[dict]:
    quantidade = random.randint(3, 8)
    servicos = []
    for indice_servico in range(quantidade):
        servicos.append(
            {
                "id": gerar_id(),
                "servico": random.choice(TIPOS_SERVICO),
                "descricao": random.choice(DESCRICOES),
                "data": gerar_data((indice_cliente * 5) + (indice_carro * 2) + indice_servico),
            }
        )
    servicos.sort(key=lambda item: datetime.strptime(item["data"], "%d/%m/%Y %H:%M"))
    return servicos


def gerar_carros(indice_cliente: int) -> list[dict]:
    quantidade = random.randint(2, 4)
    carros = []
    marcas = list(MARCAS_MODELOS.keys())
    for indice_carro in range(quantidade):
        marca = random.choice(marcas)
        modelo = random.choice(MARCAS_MODELOS[marca])
        carros.append(
            {
                "id": gerar_id(),
                "marca": marca,
                "modelo": modelo,
                "ano": str(random.randint(2012, 2025)),
                "placa": gerar_placa(indice_cliente, indice_carro),
                "servicos": gerar_servicos(indice_cliente, indice_carro),
                "data_adicao": gerar_data(indice_cliente + indice_carro),
            }
        )
    return carros


def gerar_clientes(total_clientes: int = 36) -> list[dict]:
    clientes = []
    for indice_cliente in range(1, total_clientes + 1):
        clientes.append(
            {
                "id": gerar_id(),
                "nome": gerar_nome(indice_cliente),
                "telefone": gerar_telefone(indice_cliente),
                "carros": gerar_carros(indice_cliente),
                "data_criacao": gerar_data(indice_cliente),
            }
        )
    return clientes


def main() -> None:
    random.seed(42)
    clientes = gerar_clientes()
    with ARQUIVO_CLIENTES.open("w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, ensure_ascii=False, indent=2)

    total_carros = sum(len(cliente["carros"]) for cliente in clientes)
    total_servicos = sum(len(carro["servicos"]) for cliente in clientes for carro in cliente["carros"])

    print(f"Carga criada em {ARQUIVO_CLIENTES}")
    print(f"Clientes: {len(clientes)}")
    print(f"Carros: {total_carros}")
    print(f"Serviços: {total_servicos}")


if __name__ == "__main__":
    main()

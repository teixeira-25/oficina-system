#!/usr/bin/env python3
"""
Script de teste para validar a funcionalidade de edição
"""

from dados_oficina import OficinaApp

def test_edit_functionality():
    print("=" * 60)
    print("TESTE DE FUNCIONALIDADE DE EDIÇÃO")
    print("=" * 60)
    
    app = OficinaApp()
    
    # Limpar dados antigos
    import os
    if os.path.exists("registros.csv"):
        os.remove("registros.csv")
    
    app.inicializar_arquivo()
    
    # Teste 1: Adicionar um registro
    print("\n1️⃣ Adicionando um registro de teste...")
    resultado = app.adicionar_registro(
        marca="Honda",
        modelo="Civic", 
        ano="2019",
        placa="XYZ-9876",
        servico="Troca de Óleo",
        descricao="Primeiro teste"
    )
    print(f"✅ Registro adicionado: {resultado}")
    
    # Teste 2: Obter registros
    print("\n2️⃣ Obtendo registros...")
    registros = app.obter_registros()
    print(f"Total de registros: {len(registros)}")
    for i, reg in enumerate(registros):
        print(f"  [{i}] {reg}")
    
    if not registros:
        print("❌ ERRO: Nenhum registro foi encontrado!")
        return False
    
    # Teste 3: Editar registro
    print("\n3️⃣ Editando o primeiro registro...")
    indice = 0
    novo_servico = "Troca de Filtro de Ar"
    novo_descricao = "Serviço após edição"
    
    registro_antes = registros[0]
    print(f"ANTES: {registro_antes}")
    
    resultado_edicao = app.editar_registro(
        indice=indice,
        marca=registro_antes[0],
        modelo=registro_antes[1],
        ano=registro_antes[2],
        placa=registro_antes[3],
        servico=novo_servico,
        descricao=novo_descricao
    )
    print(f"✅ Registro editado: {resultado_edicao}")
    
    # Teste 4: Verificar mudanças
    print("\n4️⃣ Verificando mudanças...")
    registros_atualizados = app.obter_registros()
    registro_depois = registros_atualizados[0]
    print(f"DEPOIS: {registro_depois}")
    
    # Validar mudanças
    if registro_depois[4] == novo_servico and "Serviço após edição" in registro_depois[5]:
        print("✅ Edição realizada com sucesso!")
        return True
    else:
        print("❌ ERRO: Edição não foi aplicada corretamente!")
        print(f"   Esperado serviço: {novo_servico}, Obtido: {registro_depois[4]}")
        return False

if __name__ == "__main__":
    try:
        sucesso = test_edit_functionality()
        if sucesso:
            print("\n" + "=" * 60)
            print("✅ TODOS OS TESTES PASSARAM!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ ALGUNS TESTES FALHARAM!")
            print("=" * 60)
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

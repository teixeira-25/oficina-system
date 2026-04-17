import streamlit as st
from clientes import GerenciadorClientes
import json

# Configuração da página
st.set_page_config(page_title="Sistema de Oficina", layout="wide", initial_sidebar_state="expanded")

# Inicializar gerenciador
@st.cache_resource
def get_gerenciador():
    return GerenciadorClientes()

gerenciador = get_gerenciador()

# Título e estilo
st.markdown("# 🔧 Sistema de Gerenciamento - Oficina")
st.markdown("---")

# Sidebar para navegação
pagina = st.sidebar.radio(
    "📌 Menu Principal",
    ["👥 Clientes", "🚗 Carros", "🛠️ Serviços", "📊 Relatórios"]
)

# ==================== PÁGINA DE CLIENTES ====================
if pagina == "👥 Clientes":
    st.header("Gerenciamento de Clientes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Cadastrar Novo Cliente")
        with st.form("form_cliente", clear_on_submit=True):
            nome = st.text_input("Nome do Cliente")
            telefone = st.text_input("Telefone")
            
            if st.form_submit_button("➕ Adicionar Cliente", use_container_width=True):
                if nome and telefone:
                    if gerenciador.adicionar_cliente(nome, telefone):
                        st.success("✅ Cliente adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar cliente!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
    
    with col2:
        st.subheader("Total de Clientes")
        clientes = gerenciador.obter_clientes()
        st.metric("Clientes Cadastrados", len(clientes))
    
    st.markdown("---")
    st.subheader("Clientes Cadastrados")
    
    clientes = gerenciador.obter_clientes()
    if clientes:
        for cliente in clientes:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                carros = gerenciador.obter_carros_cliente(cliente['id'])
                st.write(f"**{cliente['nome']}** | 📞 {cliente['telefone']} | 🚗 {len(carros)} carros")
            
            with col2:
                if st.button("✏️ Editar", key=f"edit_{cliente['id']}", use_container_width=True):
                    st.session_state[f"edit_{cliente['id']}"] = True
            
            with col3:
                if st.button("🗑️ Deletar", key=f"del_{cliente['id']}", use_container_width=True):
                    if gerenciador.deletar_cliente(cliente['id']):
                        st.success("✅ Cliente deletado!")
                        st.rerun()
            
            # Modal de edição
            if st.session_state.get(f"edit_{cliente['id']}", False):
                with st.form(f"edit_form_{cliente['id']}", clear_on_submit=True):
                    st.subheader("✏️ Editar Cliente")
                    nome_ed = st.text_input("Nome", value=cliente['nome'], key=f"nome_{cliente['id']}")
                    tel_ed = st.text_input("Telefone", value=cliente['telefone'], key=f"tel_{cliente['id']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("✓ Salvar", use_container_width=True):
                            if gerenciador.editar_cliente(cliente['id'], nome_ed, tel_ed):
                                st.success("✅ Cliente atualizado!")
                                st.session_state[f"edit_{cliente['id']}"] = False
                                st.rerun()
                    with col2:
                        if st.form_submit_button("✕ Cancelar", use_container_width=True):
                            st.session_state[f"edit_{cliente['id']}"] = False
                            st.rerun()
            
            st.divider()
    else:
        st.info("📌 Nenhum cliente cadastrado ainda.")


# ==================== PÁGINA DE CARROS ====================
elif pagina == "🚗 Carros":
    st.header("Gerenciamento de Carros")
    
    clientes = gerenciador.obter_clientes()
    
    if not clientes:
        st.warning("⚠️ Cadastre um cliente primeiro!")
    else:
        cliente_selecionado = st.selectbox(
            "Selecione um cliente",
            clientes,
            format_func=lambda c: f"{c['nome']} ({c['telefone']})"
        )
        
        st.subheader(f"Carros de {cliente_selecionado['nome']}")
        
        with st.form("form_carro", clear_on_submit=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                marca = st.text_input("Marca")
            with col2:
                modelo = st.text_input("Modelo")
            with col3:
                ano = st.text_input("Ano")
            with col4:
                placa = st.text_input("Placa")
            
            if st.form_submit_button("➕ Adicionar Carro", use_container_width=True):
                if all([marca, modelo, ano, placa]):
                    try:
                        int(ano)
                        if gerenciador.adicionar_carro(cliente_selecionado['id'], marca, modelo, ano, placa):
                            st.success("✅ Carro adicionado!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar!")
                    except ValueError:
                        st.error("❌ Ano deve ser um número!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
        
        st.markdown("---")
        
        carros = gerenciador.obter_carros_cliente(cliente_selecionado['id'])
        if carros:
            for carro in carros:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    servicos = gerenciador.obter_servicos_carro(cliente_selecionado['id'], carro['id'])
                    st.write(f"**{carro['marca']} {carro['modelo']}** ({carro['placa']}) | Ano: {carro['ano']} | Serviços: {len(servicos)}")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_carro_{carro['id']}", use_container_width=True):
                        st.session_state[f"edit_carro_{carro['id']}"] = True
                
                with col3:
                    if st.button("📋 Serviços", key=f"srv_{carro['id']}", use_container_width=True):
                        st.session_state[f"view_srv_{carro['id']}"] = True
                
                with col4:
                    if st.button("🗑️ Deletar", key=f"del_carro_{carro['id']}", use_container_width=True):
                        if gerenciador.deletar_carro(cliente_selecionado['id'], carro['id']):
                            st.success("✅ Carro deletado!")
                            st.rerun()
                
                st.divider()
        else:
            st.info("📌 Nenhum carro cadastrado para este cliente.")


# ==================== PÁGINA DE SERVIÇOS ====================
elif pagina == "🛠️ Serviços":
    st.header("Gerenciamento de Serviços")
    
    clientes = gerenciador.obter_clientes()
    
    if not clientes:
        st.warning("⚠️ Cadastre um cliente primeiro!")
    else:
        cliente_selecionado = st.selectbox(
            "Selecione um cliente",
            clientes,
            format_func=lambda c: f"{c['nome']} ({c['telefone']})",
            key="srv_cliente"
        )
        
        carros = gerenciador.obter_carros_cliente(cliente_selecionado['id'])
        
        if not carros:
            st.warning("⚠️ Cadastre um carro primeiro!")
        else:
            carro_selecionado = st.selectbox(
                "Selecione um carro",
                carros,
                format_func=lambda c: f"{c['marca']} {c['modelo']} ({c['placa']})",
                key="srv_carro"
            )
            
            st.subheader(f"Serviços: {carro_selecionado['marca']} {carro_selecionado['modelo']}")
            
            with st.form("form_servico", clear_on_submit=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    servico = st.selectbox(
                        "Tipo de Serviço",
                        gerenciador.get_tipos_servico(),
                        key="tipo_srv"
                    )
                with col2:
                    descricao = st.text_area("Descrição (opcional)")
                
                if st.form_submit_button("➕ Adicionar Serviço", use_container_width=True):
                    if servico:
                        if gerenciador.adicionar_servico(cliente_selecionado['id'], carro_selecionado['id'], servico, descricao):
                            st.success("✅ Serviço adicionado!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar!")
                    else:
                        st.warning("⚠️ Selecione um tipo de serviço!")
            
            st.markdown("---")
            
            servicos = gerenciador.obter_servicos_carro(cliente_selecionado['id'], carro_selecionado['id'])
            if servicos:
                for srv in servicos:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{srv['servico']}** | 📅 {srv['data']}")
                        if srv['descricao']:
                            st.caption(srv['descricao'])
                    
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_srv_{srv['id']}", use_container_width=True):
                            st.session_state[f"edit_srv_{srv['id']}"] = True
                    
                    with col3:
                        if st.button("🗑️ Deletar", key=f"del_srv_{srv['id']}", use_container_width=True):
                            if gerenciador.deletar_servico(cliente_selecionado['id'], carro_selecionado['id'], srv['id']):
                                st.success("✅ Serviço deletado!")
                                st.rerun()
                    
                    st.divider()
            else:
                st.info("📌 Nenhum serviço cadastrado para este carro.")


# ==================== PÁGINA DE RELATÓRIOS ====================
elif pagina == "📊 Relatórios":
    st.header("Relatórios")
    
    clientes = gerenciador.obter_clientes()
    total_clientes = len(clientes)
    total_carros = sum(len(gerenciador.obter_carros_cliente(c['id'])) for c in clientes)
    total_servicos = sum(
        len(gerenciador.obter_servicos_carro(c['id'], car['id']))
        for c in clientes
        for car in gerenciador.obter_carros_cliente(c['id'])
    )
    
    st.subheader("Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Clientes", total_clientes)
    col2.metric("🚗 Carros", total_carros)
    col3.metric("🛠️ Serviços", total_servicos)
    
    st.markdown("---")
    
    st.subheader("Detalhamento por Cliente")
    for cliente in clientes:
        with st.expander(f"👤 {cliente['nome']}"):
            carros = gerenciador.obter_carros_cliente(cliente['id'])
            st.write(f"**Telefone:** {cliente['telefone']}")
            st.write(f"**Total de Carros:** {len(carros)}")
            
            for carro in carros:
                servicos = gerenciador.obter_servicos_carro(cliente['id'], carro['id'])
                st.write(f"  • {carro['marca']} {carro['modelo']} ({carro['placa']}) - {len(servicos)} serviços")


# Footer
st.markdown("---")
st.markdown("🔧 Sistema de Gerenciamento de Oficina | Desenvolvido com ❤️ por Gabriel")

import streamlit as st
from clientes import GerenciadorClientes

# Configuração da página
st.set_page_config(page_title="Sistema de Oficina", layout="wide", initial_sidebar_state="collapsed")

# Inicializar gerenciador
@st.cache_resource
def get_gerenciador():
    return GerenciadorClientes()

gerenciador = get_gerenciador()

# Inicializar estado de navegação
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "clientes"
if "cliente_atual" not in st.session_state:
    st.session_state.cliente_atual = None
if "carro_atual" not in st.session_state:
    st.session_state.carro_atual = None

# Função para voltar
def voltar():
    if st.session_state.pagina_atual == "servicos":
        st.session_state.pagina_atual = "carros"
    elif st.session_state.pagina_atual == "carros":
        st.session_state.pagina_atual = "clientes"
        st.session_state.cliente_atual = None

# ==================== PÁGINA 1: CLIENTES ====================
if st.session_state.pagina_atual == "clientes":
    st.markdown("# 👥 Gerenciar Clientes")
    st.divider()
    
    col_form, col_list = st.columns([1, 1])
    
    # COLUNA ESQUERDA: FORMULÁRIO
    with col_form:
        st.subheader("➕ Novo Cliente")
        nome = st.text_input("Nome do Cliente", key="novo_nome", placeholder="Ex: João Silva")
        telefone = st.text_input("Telefone", key="novo_tel", placeholder="Ex: (11) 9999-9999")
        
        if st.button("✓ Adicionar", use_container_width=True, type="primary"):
            if nome and telefone:
                if gerenciador.adicionar_cliente(nome, telefone):
                    st.success("✅ Cliente adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar!")
            else:
                st.warning("⚠️ Preencha todos os campos!")
    
    # COLUNA DIREITA: LISTAGEM
    with col_list:
        st.subheader("📋 Clientes")
        clientes = gerenciador.obter_clientes()
        
        if not clientes:
            st.info("📌 Nenhum cliente cadastrado ainda.")
        else:
            for cliente in clientes:
                carros = gerenciador.obter_carros_cliente(cliente['id'])
                
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{cliente['nome']}**")
                        st.caption(f"📞 {cliente['telefone']} | 🚗 {len(carros)} carros")
                    
                    with col2:
                        if st.button("✓ Entrar", key=f"enter_{cliente['id']}", use_container_width=True):
                            st.session_state.cliente_atual = cliente['id']
                            st.session_state.pagina_atual = "carros"
                            st.rerun()
                    
                    with col3:
                        if st.button("✏️ Editar", key=f"edit_{cliente['id']}", use_container_width=True):
                            st.session_state[f"edit_{cliente['id']}"] = True
                    
                    with col4:
                        if st.button("🗑️ Deletar", key=f"del_{cliente['id']}", use_container_width=True):
                            if gerenciador.deletar_cliente(cliente['id']):
                                st.success("✅ Deletado!")
                                st.rerun()
                
                # Modal de edição
                if st.session_state.get(f"edit_{cliente['id']}", False):
                    with st.expander("✏️ Editar Cliente", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            nome_ed = st.text_input("Nome", value=cliente['nome'], key=f"nome_ed_{cliente['id']}")
                        with col2:
                            tel_ed = st.text_input("Telefone", value=cliente['telefone'], key=f"tel_ed_{cliente['id']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✓ Salvar", key=f"save_{cliente['id']}", use_container_width=True):
                                if gerenciador.editar_cliente(cliente['id'], nome_ed, tel_ed):
                                    st.success("✅ Atualizado!")
                                    st.session_state[f"edit_{cliente['id']}"] = False
                                    st.rerun()
                        with col2:
                            if st.button("✕ Cancelar", key=f"cancel_{cliente['id']}", use_container_width=True):
                                st.session_state[f"edit_{cliente['id']}"] = False
                                st.rerun()


# ==================== PÁGINA 2: CARROS ====================
elif st.session_state.pagina_atual == "carros":
    cliente = gerenciador.obter_cliente(st.session_state.cliente_atual)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.markdown(f"# 🚗 Carros de {cliente['nome']}")
    with col2:
        if st.button("← Voltar", use_container_width=True):
            voltar()
            st.rerun()
    st.divider()
    
    col_form, col_list = st.columns([1, 1])
    
    # COLUNA ESQUERDA: FORMULÁRIO
    with col_form:
        st.subheader("➕ Novo Carro")
        marca = st.text_input("Marca", key="novo_marca", placeholder="Ex: Toyota")
        modelo = st.text_input("Modelo", key="novo_modelo", placeholder="Ex: Corolla")
        ano = st.text_input("Ano", key="novo_ano", placeholder="Ex: 2022")
        placa = st.text_input("Placa", key="novo_placa", placeholder="Ex: ABC-1234")
        
        if st.button("✓ Adicionar", use_container_width=True, type="primary"):
            if all([marca, modelo, ano, placa]):
                try:
                    int(ano)
                    if gerenciador.adicionar_carro(st.session_state.cliente_atual, marca, modelo, ano, placa):
                        st.success("✅ Carro adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar!")
                except ValueError:
                    st.error("❌ Ano deve ser número!")
            else:
                st.warning("⚠️ Preencha todos os campos!")
    
    # COLUNA DIREITA: LISTAGEM
    with col_list:
        st.subheader("📋 Carros")
        carros = gerenciador.obter_carros_cliente(st.session_state.cliente_atual)
        
        if not carros:
            st.info("📌 Nenhum carro cadastrado.")
        else:
            for carro in carros:
                servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, carro['id'])
                
                with st.container(border=True):
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{carro['marca']} {carro['modelo']}**")
                        st.caption(f"Placa: {carro['placa']} | Ano: {carro['ano']} | 🛠️ {len(servicos)}")
                    
                    with col2:
                        if st.button("✓ Serviços", key=f"srv_{carro['id']}", use_container_width=True):
                            st.session_state.carro_atual = carro['id']
                            st.session_state.pagina_atual = "servicos"
                            st.rerun()
                    
                    with col3:
                        if st.button("✏️", key=f"edit_car_{carro['id']}", use_container_width=True):
                            st.session_state[f"edit_car_{carro['id']}"] = True
                    
                    with col4:
                        if st.button("🗑️", key=f"del_car_{carro['id']}", use_container_width=True):
                            if gerenciador.deletar_carro(st.session_state.cliente_atual, carro['id']):
                                st.success("✅ Deletado!")
                                st.rerun()
                
                # Modal de edição
                if st.session_state.get(f"edit_car_{carro['id']}", False):
                    with st.expander("✏️ Editar Carro", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            marca_ed = st.text_input("Marca", value=carro['marca'], key=f"marca_ed_{carro['id']}")
                            ano_ed = st.text_input("Ano", value=carro['ano'], key=f"ano_ed_{carro['id']}")
                        with col2:
                            modelo_ed = st.text_input("Modelo", value=carro['modelo'], key=f"modelo_ed_{carro['id']}")
                            placa_ed = st.text_input("Placa", value=carro['placa'], key=f"placa_ed_{carro['id']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✓ Salvar", key=f"save_car_{carro['id']}", use_container_width=True):
                                if all([marca_ed, modelo_ed, ano_ed, placa_ed]):
                                    try:
                                        int(ano_ed)
                                        if gerenciador.editar_carro(st.session_state.cliente_atual, carro['id'], marca_ed, modelo_ed, ano_ed, placa_ed):
                                            st.success("✅ Atualizado!")
                                            st.session_state[f"edit_car_{carro['id']}"] = False
                                            st.rerun()
                                    except ValueError:
                                        st.error("❌ Ano deve ser número!")
                        with col2:
                            if st.button("✕ Cancelar", key=f"cancel_car_{carro['id']}", use_container_width=True):
                                st.session_state[f"edit_car_{carro['id']}"] = False
                                st.rerun()


# ==================== PÁGINA 3: SERVIÇOS ====================
elif st.session_state.pagina_atual == "servicos":
    cliente = gerenciador.obter_cliente(st.session_state.cliente_atual)
    carros = gerenciador.obter_carros_cliente(st.session_state.cliente_atual)
    
    carro = None
    for c in carros:
        if c['id'] == st.session_state.carro_atual:
            carro = c
            break
    
    if not carro:
        st.error("❌ Carro não encontrado!")
    else:
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"# 🔧 Serviços: {carro['marca']} {carro['modelo']} ({carro['placa']})")
        with col2:
            if st.button("← Voltar", use_container_width=True):
                voltar()
                st.rerun()
        st.divider()
        
        col_form, col_list = st.columns([1, 1])
        
        # COLUNA ESQUERDA: FORMULÁRIO
        with col_form:
            st.subheader("➕ Novo Serviço")
            servico = st.selectbox("Tipo de Serviço", gerenciador.get_tipos_servico(), key="novo_srv")
            descricao = st.text_area("Descrição (opcional)", key="nova_desc", placeholder="Detalhes do serviço...")
            
            if st.button("✓ Adicionar", use_container_width=True, type="primary"):
                if servico:
                    if gerenciador.adicionar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, servico, descricao):
                        st.success("✅ Serviço adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar!")
                else:
                    st.warning("⚠️ Selecione um tipo!")
        
        # COLUNA DIREITA: LISTAGEM
        with col_list:
            st.subheader("📋 Serviços")
            servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, st.session_state.carro_atual)
            
            if not servicos:
                st.info("📌 Nenhum serviço cadastrado.")
            else:
                for srv in servicos:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{srv['servico']}**")
                            st.caption(f"📅 {srv['data']}")
                            if srv['descricao']:
                                st.caption(f"📝 {srv['descricao']}")
                        
                        with col2:
                            if st.button("✏️ Editar", key=f"edit_srv_{srv['id']}", use_container_width=True):
                                st.session_state[f"edit_srv_{srv['id']}"] = True
                        
                        with col3:
                            if st.button("🗑️ Deletar", key=f"del_srv_{srv['id']}", use_container_width=True):
                                if gerenciador.deletar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, srv['id']):
                                    st.success("✅ Deletado!")
                                    st.rerun()
                    
                    # Modal de edição
                    if st.session_state.get(f"edit_srv_{srv['id']}", False):
                        with st.expander("✏️ Editar Serviço", expanded=True):
                            tipo_ed = st.selectbox("Tipo", gerenciador.get_tipos_servico(), 
                                                  value=srv['servico'], key=f"tipo_ed_{srv['id']}")
                            desc_ed = st.text_area("Descrição", value=srv['descricao'], key=f"desc_ed_{srv['id']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✓ Salvar", key=f"save_srv_{srv['id']}", use_container_width=True):
                                    if gerenciador.editar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, srv['id'], tipo_ed, desc_ed):
                                        st.success("✅ Atualizado!")
                                        st.session_state[f"edit_srv_{srv['id']}"] = False
                                        st.rerun()
                            with col2:
                                if st.button("✕ Cancelar", key=f"cancel_srv_{srv['id']}", use_container_width=True):
                                    st.session_state[f"edit_srv_{srv['id']}"] = False
                                    st.rerun()

# Footer
st.markdown("---")
st.markdown("🔧 Sistema de Gerenciamento de Oficina | Desenvolvido com ❤️")

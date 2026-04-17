import streamlit as st
from clientes import GerenciadorClientes

# Configuração da página
st.set_page_config(page_title="Sistema de Oficina", layout="wide", initial_sidebar_state="collapsed")

# CSS Customizado para Design Profissional
st.markdown("""
<style>
    /* Cores Profissionais */
    :root {
        --primary-color: #1e40af;
        --primary-light: #3b82f6;
        --danger-color: #dc2626;
        --success-color: #16a34a;
        --warning-color: #f59e0b;
        --neutral-light: #f9fafb;
        --neutral-border: #e5e7eb;
        --text-primary: #111827;
        --text-secondary: #6b7280;
    }
    
    /* Elementos Principais */
    .main {
        padding: 2rem;
        background-color: #f9fafb;
    }
    
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    h1 {
        font-size: 1.875rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid var(--primary-color);
        padding-bottom: 0.75rem;
    }
    
    /* Cards */
    .stContainer {
        border: 1px solid var(--neutral-border);
        border-radius: 0.5rem;
        padding: 1rem;
        background: white;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stContainer:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-color: var(--primary-light);
    }
    
    /* Botões */
    .stButton>button {
        border-radius: 0.375rem;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid var(--neutral-border);
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 0.375rem;
        border: 1px solid var(--neutral-border);
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 0.375rem;
        border-left: 4px solid;
    }
    
    .stAlert[data-baseweb="notification"][data-state="information"] {
        border-left-color: var(--primary-light);
    }
    
    .stAlert[data-baseweb="notification"][data-state="success"] {
        border-left-color: var(--success-color);
    }
    
    .stAlert[data-baseweb="notification"][data-state="error"] {
        border-left-color: var(--danger-color);
    }
    
    .stAlert[data-baseweb="notification"][data-state="warning"] {
        border-left-color: var(--warning-color);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 0.375rem;
        background-color: var(--neutral-light);
        border: 1px solid var(--neutral-border);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f3f4f6;
    }
    
    /* Scroll Container */
    .scroll-container {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 0.5rem;
        border-right: 1px solid var(--neutral-border);
    }
    
    .scroll-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .scroll-container::-webkit-scrollbar-track {
        background: var(--neutral-light);
        border-radius: 10px;
    }
    
    .scroll-container::-webkit-scrollbar-thumb {
        background: var(--neutral-border);
        border-radius: 10px;
    }
    
    .scroll-container::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light);
    }
</style>
""", unsafe_allow_html=True)

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
    st.markdown("## 👥 Gerenciamento de Clientes")
    st.markdown("---")
    
    col_form, col_list = st.columns([1, 1], gap="large")
    
    # COLUNA ESQUERDA: FORMULÁRIO
    with col_form:
        st.markdown("### ➕ Adicionar Cliente")
        with st.form("form_novo_cliente", clear_on_submit=True):
            nome = st.text_input("Nome completo", placeholder="João Silva Santos")
            telefone = st.text_input("Telefone", placeholder="(11) 98765-4321")
            
            submitted = st.form_submit_button("✓ Cadastrar Cliente", use_container_width=True, type="primary")
            
            if submitted:
                if nome and telefone:
                    if gerenciador.adicionar_cliente(nome, telefone):
                        st.success("✅ Cliente cadastrado com sucesso!", icon="✅")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar cliente", icon="❌")
                else:
                    st.warning("⚠️ Preencha todos os campos", icon="⚠️")
    
    # COLUNA DIREITA: LISTAGEM
    with col_list:
        st.markdown("### 📋 Clientes Cadastrados")
        clientes = gerenciador.obter_clientes()
        
        if not clientes:
            st.info("📌 Nenhum cliente cadastrado. Comece adicionando um novo cliente!", icon="ℹ️")
        else:
            # Search Bar
            search_cliente = st.text_input("🔍 Buscar cliente", placeholder="Nome ou telefone...", key="search_cli")
            
            # Filtrar clientes
            clientes_filtrados = [
                c for c in clientes 
                if search_cliente.lower() in c['nome'].lower() or search_cliente.lower() in c['telefone']
            ]
            
            st.markdown(f"**Total:** {len(clientes_filtrados)}/{len(clientes)} cliente(s)")
            st.divider()
            
            # ScrollContainer com altura fixa
            with st.container(border=False):
                st.markdown("""<div class="scroll-container" style="max-height: 600px; overflow-y: auto;">""", unsafe_allow_html=True)
                
                for idx, cliente in enumerate(clientes_filtrados):
                    carros = gerenciador.obter_carros_cliente(cliente['id'])
                    
                    with st.container(border=True):
                        col_info, col_actions = st.columns([2.5, 1.5])
                        
                        with col_info:
                            st.markdown(f"**{cliente['nome']}**", help=f"ID: {cliente['id']}")
                            st.markdown(f"📞 {cliente['telefone']} • 🚗 {len(carros)} carro(s)")
                        
                        with col_actions:
                            col_e, col_d, col_s = st.columns(3)
                            with col_e:
                                if st.button("✓", key=f"enter_{cliente['id']}", use_container_width=True, help="Ver carros deste cliente"):
                                    st.session_state.cliente_atual = cliente['id']
                                    st.session_state.pagina_atual = "carros"
                                    st.rerun()
                            with col_d:
                                if st.button("✏️", key=f"edit_{cliente['id']}", use_container_width=True, help="Editar"):
                                    st.session_state[f"edit_{cliente['id']}"] = True
                                    st.rerun()
                            with col_s:
                                if st.button("🗑️", key=f"del_{cliente['id']}", use_container_width=True, help="Deletar"):
                                    if gerenciador.deletar_cliente(cliente['id']):
                                        st.success("✅ Cliente removido", icon="✅")
                                        st.rerun()
                                    else:
                                        st.error("Erro ao deletar", icon="❌")
                        
                        # Modal de edição
                        if st.session_state.get(f"edit_{cliente['id']}", False):
                            st.divider()
                            st.markdown("**✏️ Editar Cliente**")
                            col_ed1, col_ed2 = st.columns(2)
                            with col_ed1:
                                nome_ed = st.text_input("Nome", value=cliente['nome'], key=f"nome_ed_{cliente['id']}")
                            with col_ed2:
                                tel_ed = st.text_input("Telefone", value=cliente['telefone'], key=f"tel_ed_{cliente['id']}")
                            
                            col_s1, col_s2 = st.columns(2)
                            with col_s1:
                                if st.button("✓ Salvar", key=f"save_{cliente['id']}", use_container_width=True, type="primary"):
                                    if nome_ed and tel_ed:
                                        if gerenciador.editar_cliente(cliente['id'], nome_ed, tel_ed):
                                            st.success("✅ Atualizado", icon="✅")
                                            st.session_state[f"edit_{cliente['id']}"] = False
                                            st.rerun()
                                    else:
                                        st.warning("⚠️ Preencha os campos")
                            with col_s2:
                                if st.button("✕ Cancelar", key=f"cancel_{cliente['id']}", use_container_width=True):
                                    st.session_state[f"edit_{cliente['id']}"] = False
                                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)


# ==================== PÁGINA 2: CARROS ====================
elif st.session_state.pagina_atual == "carros":
    cliente = gerenciador.obter_cliente(st.session_state.cliente_atual)
    
    col_header, col_back = st.columns([10, 1])
    with col_header:
        st.markdown(f"## 🚗 Carros de {cliente['nome']}")
    with col_back:
        if st.button("← Voltar", use_container_width=True, help="Voltar para clientes"):
            voltar()
            st.rerun()
    st.markdown("---")
    
    col_form, col_list = st.columns([1, 1], gap="large")
    
    # COLUNA ESQUERDA: FORMULÁRIO
    with col_form:
        st.markdown("### ➕ Adicionar Carro")
        with st.form("form_novo_carro", clear_on_submit=True):
            marca = st.text_input("Marca", key="novo_marca", placeholder="Toyota, BMW, etc")
            modelo = st.text_input("Modelo", key="novo_modelo", placeholder="Corolla, X5, etc")
            ano = st.text_input("Ano", key="novo_ano", placeholder="2022")
            placa = st.text_input("Placa", key="novo_placa", placeholder="ABC-1234")
            
            submitted = st.form_submit_button("✓ Cadastrar Carro", use_container_width=True, type="primary")
            
            if submitted:
                if all([marca, modelo, ano, placa]):
                    try:
                        int(ano)
                        if gerenciador.adicionar_carro(st.session_state.cliente_atual, marca, modelo, ano, placa):
                            st.success("✅ Carro cadastrado!", icon="✅")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao cadastrar", icon="❌")
                    except ValueError:
                        st.error("❌ Ano deve ser numérico", icon="❌")
                else:
                    st.warning("⚠️ Preencha todos os campos", icon="⚠️")
    
    # COLUNA DIREITA: LISTAGEM
    with col_list:
        st.markdown("### 📋 Carros Cadastrados")
        carros = gerenciador.obter_carros_cliente(st.session_state.cliente_atual)
        
        if not carros:
            st.info("📌 Nenhum carro cadastrado. Adicione o primeiro carro!", icon="ℹ️")
        else:
            # Search Bar
            search_carro = st.text_input("🔍 Buscar carro", placeholder="Marca, modelo ou placa...", key="search_car")
            
            # Filtrar carros
            carros_filtrados = [
                c for c in carros 
                if search_carro.lower() in c['marca'].lower() or 
                   search_carro.lower() in c['modelo'].lower() or 
                   search_carro.lower() in c['placa'].lower()
            ]
            
            st.markdown(f"**Total:** {len(carros_filtrados)}/{len(carros)} carro(s)")
            st.divider()
            
            # ScrollContainer com altura fixa
            with st.container(border=False):
                st.markdown("""<div class="scroll-container" style="max-height: 600px; overflow-y: auto;">""", unsafe_allow_html=True)
                
                for carro in carros_filtrados:
                    servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, carro['id'])
                
                    with st.container(border=True):
                        col_info, col_actions = st.columns([2.5, 1.5])
                    
                    with col_info:
                        st.markdown(f"**{carro['marca']} {carro['modelo']}**", help=f"ID: {carro['id']}")
                        st.markdown(f"📋 Placa: {carro['placa']} • 📅 Ano: {carro['ano']} • 🛠️ {len(servicos)} serviço(s)")
                    
                    with col_actions:
                        col_s, col_e, col_d = st.columns(3)
                        with col_s:
                            if st.button("✓", key=f"srv_{carro['id']}", use_container_width=True, help="Ver serviços"):
                                st.session_state.carro_atual = carro['id']
                                st.session_state.pagina_atual = "servicos"
                                st.rerun()
                        with col_e:
                            if st.button("✏️", key=f"edit_car_{carro['id']}", use_container_width=True, help="Editar"):
                                st.session_state[f"edit_car_{carro['id']}"] = True
                                st.rerun()
                        with col_d:
                            if st.button("🗑️", key=f"del_car_{carro['id']}", use_container_width=True, help="Deletar"):
                                if gerenciador.deletar_carro(st.session_state.cliente_atual, carro['id']):
                                    st.success("✅ Carro removido", icon="✅")
                                    st.rerun()
                    
                    # Modal de edição
                    if st.session_state.get(f"edit_car_{carro['id']}", False):
                        st.divider()
                        st.markdown("**✏️ Editar Carro**")
                        col_ed1, col_ed2 = st.columns(2)
                        with col_ed1:
                            marca_ed = st.text_input("Marca", value=carro['marca'], key=f"marca_ed_{carro['id']}")
                            ano_ed = st.text_input("Ano", value=carro['ano'], key=f"ano_ed_{carro['id']}")
                        with col_ed2:
                            modelo_ed = st.text_input("Modelo", value=carro['modelo'], key=f"modelo_ed_{carro['id']}")
                            placa_ed = st.text_input("Placa", value=carro['placa'], key=f"placa_ed_{carro['id']}")
                        
                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            if st.button("✓ Salvar", key=f"save_car_{carro['id']}", use_container_width=True, type="primary"):
                                if all([marca_ed, modelo_ed, ano_ed, placa_ed]):
                                    try:
                                        int(ano_ed)
                                        if gerenciador.editar_carro(st.session_state.cliente_atual, carro['id'], marca_ed, modelo_ed, ano_ed, placa_ed):
                                            st.success("✅ Atualizado", icon="✅")
                                            st.session_state[f"edit_car_{carro['id']}"] = False
                                            st.rerun()
                                    except ValueError:
                                        st.error("❌ Ano deve ser número", icon="❌")
                                else:
                                    st.warning("⚠️ Preencha os campos")
                        with col_s2:
                            if st.button("✕ Cancelar", key=f"cancel_car_{carro['id']}", use_container_width=True):
                                st.session_state[f"edit_car_{carro['id']}"] = False
                                st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)


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
        col_header, col_back = st.columns([10, 1])
        with col_header:
            st.markdown(f"## 🔧 Serviços: {carro['marca']} {carro['modelo']} ({carro['placa']})")
        with col_back:
            if st.button("← Voltar", use_container_width=True, help="Voltar para carros"):
                voltar()
                st.rerun()
        st.markdown("---")
        
        col_form, col_list = st.columns([1, 1], gap="large")
        
        # COLUNA ESQUERDA: FORMULÁRIO
        with col_form:
            st.markdown("### ➕ Adicionar Serviço")
            with st.form("form_novo_servico", clear_on_submit=True):
                servico = st.selectbox("Tipo de Serviço", gerenciador.get_tipos_servico(), key="novo_srv")
                descricao = st.text_area("Descrição (opcional)", key="nova_desc", placeholder="Detalhes do serviço realizado...", height=100)
                
                submitted = st.form_submit_button("✓ Cadastrar Serviço", use_container_width=True, type="primary")
                
                if submitted:
                    if servico:
                        if gerenciador.adicionar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, servico, descricao):
                            st.success("✅ Serviço cadastrado!", icon="✅")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao cadastrar", icon="❌")
                    else:
                        st.warning("⚠️ Selecione um tipo de serviço", icon="⚠️")
        
        # COLUNA DIREITA: LISTAGEM
        with col_list:
            st.markdown("### 📋 Serviços Cadastrados")
            servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, st.session_state.carro_atual)
            
            if not servicos:
                st.info("📌 Nenhum serviço cadastrado. Registre o primeiro serviço!", icon="ℹ️")
            else:
                # Search Bar
                search_servico = st.text_input("🔍 Buscar serviço", placeholder="Tipo de serviço...", key="search_srv")
                
                # Filtrar serviços
                servicos_filtrados = [
                    s for s in servicos 
                    if search_servico.lower() in s['servico'].lower()
                ]
                
                st.markdown(f"**Total:** {len(servicos_filtrados)}/{len(servicos)} serviço(s)")
                st.divider()
                
                # ScrollContainer com altura fixa
                with st.container(border=False):
                    st.markdown("""<div class="scroll-container" style="max-height: 600px; overflow-y: auto;">""", unsafe_allow_html=True)
                    
                    for srv in servicos_filtrados:
                        with st.container(border=True):
                            col_info, col_actions = st.columns([2.5, 1.5])
                            
                            with col_info:
                                st.markdown(f"**{srv['servico']}**", help=f"ID: {srv['id']}")
                                st.markdown(f"📅 {srv['data']}")
                                if srv['descricao']:
                                    st.markdown(f"📝 *{srv['descricao']}*")
                            
                            with col_actions:
                                col_e, col_d = st.columns(2)
                                with col_e:
                                    if st.button("✏️", key=f"edit_srv_{srv['id']}", use_container_width=True, help="Editar"):
                                        st.session_state[f"edit_srv_{srv['id']}"] = True
                                        st.rerun()
                                with col_d:
                                    if st.button("🗑️", key=f"del_srv_{srv['id']}", use_container_width=True, help="Deletar"):
                                        if gerenciador.deletar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, srv['id']):
                                            st.success("✅ Serviço removido", icon="✅")
                                            st.rerun()
                        
                        # Modal de edição
                        if st.session_state.get(f"edit_srv_{srv['id']}", False):
                            st.divider()
                            st.markdown("**✏️ Editar Serviço**")
                            col_ed1, col_ed2 = st.columns([1, 2])
                            with col_ed1:
                                tipo_ed = st.selectbox("Tipo", gerenciador.get_tipos_servico(), 
                                                      value=srv['servico'], key=f"tipo_ed_{srv['id']}")
                            with col_ed2:
                                desc_ed = st.text_area("Descrição", value=srv['descricao'], key=f"desc_ed_{srv['id']}", height=80)
                            
                            col_s1, col_s2 = st.columns(2)
                            with col_s1:
                                if st.button("✓ Salvar", key=f"save_srv_{srv['id']}", use_container_width=True, type="primary"):
                                    if gerenciador.editar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, srv['id'], tipo_ed, desc_ed):
                                        st.success("✅ Atualizado", icon="✅")
                                        st.session_state[f"edit_srv_{srv['id']}"] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao atualizar", icon="❌")
                            with col_s2:
                                if st.button("✕ Cancelar", key=f"cancel_srv_{srv['id']}", use_container_width=True):
                                    st.session_state[f"edit_srv_{srv['id']}"] = False
                                    st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.875rem; margin-top: 2rem;'>
    <p>🔧 <strong>Sistema de Gerenciamento de Oficina</strong> | Desenvolvido com ❤️</p>
    <p style='margin-top: 0.5rem;'><em>Versão Web • 2026</em></p>
</div>
""", unsafe_allow_html=True)

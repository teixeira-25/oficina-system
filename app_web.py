import streamlit as st
from datetime import datetime
import hashlib
from clientes import GerenciadorClientes

try:
    from fpdf import FPDF
except ImportError:
    st.error("Erro: A biblioteca 'fpdf2' não foi encontrada. Instale-a com: pip install fpdf2")
    st.stop()

# Configuração da página
st.set_page_config(page_title="Sistema de Oficina", layout="wide", initial_sidebar_state="collapsed")

# CSS Customizado para Design Profissional
st.markdown("""
<style>
    /* Cores Red Car */
    :root {
        --primary-color: #ef4444;
        --primary-hover: #dc2626;
        --bg-main: #f3f4f6;
        --bg-card: #ffffff;
        --border-color: #e5e7eb;
        --text-main: #111827;
        --text-muted: #6b7280;
    }
    
    /* Elementos Principais */
    .main {
        background-color: var(--bg-main);
        padding-top: 3rem;
    }
    
    h1, h2, h3 {
        color: var(--text-main);
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    h1 {
        font-size: 1.25rem;
    }

    /* Esconder o header padrão do Streamlit para o nosso fixo brilhar */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Cards */
    .stContainer {
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        background: var(--bg-card);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stContainer:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Botões */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.4rem 0.8rem;
        transition: all 0.15s ease-in-out;
    }
    
    /* Botão Primário (Red) */
    .stButton>button[kind="primary"] {
        background-color: var(--primary-color);
        border: none;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: var(--primary-hover);
    }

    /* Divider */
    hr {
        margin: 1rem 0;
        border: none;
        border-top: 1px solid var(--border-color);
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 0.5rem 0.75rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
    }
    
    /* Scroll Container */
    .scroll-container {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 0.5rem;
        border-right: 1px solid var(--neutral-border);
    }
    
    /* Top Header */
    .top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(8px);
        color: var(--text-main);
        border-bottom: 1px solid var(--border-color);
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar gerenciador
@st.cache_resource
def get_gerenciador():
    return GerenciadorClientes()

gerenciador = get_gerenciador()
ALTURA_LISTA_MAXIMA = 620
ALTURA_LISTA_MINIMA = 140
ALTURA_ITEM_LISTA = 120

def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    # Tenta restaurar a sessão a partir da URL (Hash seguro do usuário+senha)
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        try:
            expected_token = hashlib.sha256((st.secrets["auth"]["username"] + st.secrets["auth"]["password"]).encode()).hexdigest()
            if st.query_params.get("session") == expected_token:
                st.session_state["authenticated"] = True
        except (KeyError, AttributeError):
            pass

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #ef4444; font-size: 2.5rem;'>🚗 RED CAR</h1>
            <p style='color: #6b7280;'>Acesso restrito ao sistema de gerenciamento</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        col_l, col_r = st.columns([1, 1])
        with col_l:
            user = st.text_input("Usuário", placeholder="Digite seu usuário")
        with col_r:
            pw = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        if st.button("Entrar no Sistema", use_container_width=True, type="primary"):
            try:
                if user == st.secrets["auth"]["username"] and pw == st.secrets["auth"]["password"]:
                    st.session_state["authenticated"] = True
                    # Persistir login na URL para permanência após refresh
                    st.query_params["session"] = hashlib.sha256((user + pw).encode()).hexdigest()
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
            except KeyError:
                st.error("❌ Erro de Configuração: A seção [auth] não foi encontrada nos Secrets do Streamlit Cloud.")
    return False

# Bloqueia a execução se não estiver autenticado
if not check_password():
    st.stop()

# Inicializar estado de navegação
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = st.query_params.get("p", "dashboard")
if "cliente_atual" not in st.session_state:
    st.session_state.cliente_atual = st.query_params.get("c")
if "carro_atual" not in st.session_state:
    st.session_state.carro_atual = st.query_params.get("v")
if "edit_servico_id" not in st.session_state:
    st.session_state.edit_servico_id = None

# Sincronizar URL com o estado atual para suportar Refresh sem perda de contexto
st.query_params["p"] = st.session_state.pagina_atual
if st.session_state.cliente_atual: st.query_params["c"] = st.session_state.cliente_atual
else: st.query_params.pop("c", None)
if st.session_state.carro_atual: st.query_params["v"] = st.session_state.carro_atual
else: st.query_params.pop("v", None)

# Função para voltar à dashboard
def voltar_dashboard():
    st.session_state.pagina_atual = "dashboard"
    st.rerun()

# Função para voltar
def voltar():
    if st.session_state.pagina_atual == "servicos":
        st.session_state.pagina_atual = "carros"
    elif st.session_state.pagina_atual == "carros":
        st.session_state.pagina_atual = "clientes"
        st.session_state.cliente_atual = None
    st.session_state.edit_servico_id = None

# Função para obter hora atual
def obter_hora_digital():
    return datetime.now().strftime("%H:%M:%S")


def calcular_altura_lista(total_itens):
    """Ajusta a altura da lista sem deixar grandes blocos vazios."""
    if total_itens <= 0:
        return ALTURA_LISTA_MINIMA
    return min(ALTURA_LISTA_MAXIMA, max(ALTURA_LISTA_MINIMA, total_itens * ALTURA_ITEM_LISTA))


def formatar_moeda(valor):
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data
def gerar_pdf_servico(cliente_nome, cliente_tel, carro_info, servico_info):
    """Gera o buffer de bytes de um PDF com os detalhes do serviço."""
    pdf = FPDF()
    pdf.add_page()

    # --- CABEÇALHO ---
    pdf.set_fill_color(220, 38, 38)  # Cor Vermelha Red Car
    pdf.rect(10, 10, 190, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 20)
    pdf.cell(0, 12, "RED CAR", ln=True, align="C")
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, "Proprietário: Osvaldo Teixeira | CNPJ: 88.888.888/0001-55", ln=True, align="C")
    pdf.set_font("helvetica", "", 9)
    pdf.cell(0, 5, "Rua Dr. Irineu Pinheiro, 558 - Pimenta, Crato - CE", ln=True, align="C")
    pdf.ln(13)

    # Número da OS e Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(95, 10, "ORDEM DE SERVIÇO", border="B")
    pdf.cell(95, 10, f"DATA: {servico_info['data']}", border="B", ln=True, align="R")
    pdf.ln(5)

    # --- DADOS DO CLIENTE E VEÍCULO ---
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, " INFORMAÇÕES GERAIS", ln=True, fill=True)
    pdf.set_font("helvetica", "", 10)

    col_width = 95
    pdf.set_font("helvetica", "B", 10); pdf.cell(25, 7, "Cliente:"); pdf.set_font("helvetica", "", 10); pdf.cell(col_width - 25, 7, cliente_nome)
    pdf.set_font("helvetica", "B", 10); pdf.cell(25, 7, "Veículo:"); pdf.set_font("helvetica", "", 10); pdf.cell(col_width - 25, 7, f"{carro_info['marca']} {carro_info['modelo']}", ln=True)

    pdf.set_font("helvetica", "B", 10); pdf.cell(25, 7, "Telefone:"); pdf.set_font("helvetica", "", 10); pdf.cell(col_width - 25, 7, cliente_tel)
    pdf.set_font("helvetica", "B", 10); pdf.cell(25, 7, "Placa/Ano:"); pdf.set_font("helvetica", "", 10); pdf.cell(col_width - 25, 7, f"{carro_info['placa']} / {carro_info['ano']}", ln=True)
    pdf.ln(5)

    # --- DESCRIÇÃO DO SERVIÇO ---
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, f" SERVIÇO: {servico_info['servico'].upper()}", ln=True, fill=True)
    pdf.set_font("helvetica", "", 10)
    pdf.ln(2)
    desc = servico_info.get('descricao', 'Nenhum detalhe adicional informado.')
    pdf.multi_cell(0, 6, desc)
    pdf.ln(5)

    # --- TABELA DE PEÇAS ---
    pecas = servico_info.get('pecas', [])
    if pecas:
        pdf.set_fill_color(220, 38, 38)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(100, 8, " Descrição da Peça / Material", 1, 0, "L", fill=True)
        pdf.cell(20, 8, "Qtd", 1, 0, "C", fill=True)
        pdf.cell(35, 8, "V. Unitário", 1, 0, "R", fill=True)
        pdf.cell(35, 8, "Total", 1, 1, "R", fill=True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", "", 10)
        for p in pecas:
            pdf.cell(100, 8, f" {p['nome']}", 1)
            pdf.cell(20, 8, str(p['quantidade']), 1, 0, "C")
            pdf.cell(35, 8, f"R$ {float(p['preco']):.2f} ", 1, 0, "R")
            pdf.cell(35, 8, f"R$ {float(p['total']):.2f} ", 1, 1, "R")

    # --- TOTAL ---
    pdf.ln(2)
    valor_total = sum(float(p.get('total', 0)) for p in pecas)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_fill_color(220, 38, 38)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(155, 10, "VALOR TOTAL DO SERVIÇO ", 0, 0, "R", fill=True)
    pdf.cell(35, 10, f"R$ {valor_total:.2f} ", 0, 1, "R", fill=True)

    pdf.ln(10)
    pdf.set_font("helvetica", "I", 8); pdf.cell(0, 10, "Documento gerado pelo Sistema Red Car.", align="C")
    return bytes(pdf.output())

def gerar_pdf_relatorio_consolidado(servicos, titulo_periodo):
    """Gera um PDF consolidado com todos os serviços do período."""
    pdf = FPDF()
    pdf.add_page()

    # --- CABEÇALHO ---
    pdf.set_fill_color(220, 38, 38)
    pdf.rect(10, 10, 190, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 20)
    pdf.cell(0, 12, "RED CAR", ln=True, align="C")
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, "Proprietário: Osvaldo Teixeira | CNPJ: 88.888.888/0001-55", ln=True, align="C")
    pdf.set_font("helvetica", "", 9)
    pdf.cell(0, 5, "Rua Dr. Irineu Pinheiro, 558 - Pimenta, Crato - CE", ln=True, align="C")
    pdf.ln(13)

    # Título do Relatório
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"RELATÓRIO DE SERVIÇOS - {titulo_periodo}", ln=True, align="C", border="B")
    pdf.ln(5)

    # Resumo Estatístico
    total_receita = sum(s.get('valor_pecas', 0) for s in servicos)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(95, 8, f"Total de Serviços: {len(servicos)}")
    pdf.cell(95, 8, f"Receita Total Estimada: {formatar_moeda(total_receita)}", ln=True, align="R")
    pdf.ln(5)

    # Tabela de Serviços
    pdf.set_fill_color(220, 38, 38)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(20, 8, " Data", 1, 0, "L", fill=True)
    pdf.cell(45, 8, " Cliente", 1, 0, "L", fill=True)
    pdf.cell(45, 8, " Veículo", 1, 0, "L", fill=True)
    pdf.cell(50, 8, " Serviço", 1, 0, "L", fill=True)
    pdf.cell(30, 8, " Valor", 1, 1, "R", fill=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "", 7)
    
    for s in servicos:
        cliente = (s['cliente_nome'][:25] + '..') if len(s['cliente_nome']) > 25 else s['cliente_nome']
        veiculo = f"{s['carro_marca']} {s['carro_modelo']} ({s['carro_placa']})"
        veiculo = (veiculo[:25] + '..') if len(veiculo) > 25 else veiculo
        servico = (s['servico_tipo'][:30] + '..') if len(s['servico_tipo']) > 30 else s['servico_tipo']
        
        pdf.cell(20, 7, s['data'].split(' ')[0], 1)
        pdf.cell(45, 7, f" {cliente}", 1)
        pdf.cell(45, 7, f" {veiculo}", 1)
        pdf.cell(50, 7, f" {servico}", 1)
        pdf.cell(30, 7, f"{formatar_moeda(s['valor_pecas'])} ", 1, 1, "R")

    pdf.ln(10)
    pdf.set_font("helvetica", "I", 8)
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", align="R")
    
    return bytes(pdf.output())

@st.dialog("Exportar Relatório Consolidado", width="large")
def modal_exportar_relatorio():
    st.markdown("Escolha o tipo de relatório e o período desejado para exportação.")
    
    tipo = st.radio("Tipo de Relatório", ["Diário", "Mensal", "Anual"], horizontal=True)
    
    servicos_filtrados = []
    titulo_periodo = ""
    todos = gerenciador.obter_todos_servicos()
    
    if tipo == "Diário":
        data_sel = st.date_input("Selecione a Data", value=datetime.now())
        data_str = data_sel.strftime("%d/%m/%Y")
        titulo_periodo = f"DIÁRIO ({data_str})"
        servicos_filtrados = [s for s in todos if s['data'].startswith(data_str)]
        
    elif tipo == "Mensal":
        col_m, col_a = st.columns(2)
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_sel = col_m.selectbox("Mês", meses, index=datetime.now().month - 1)
        ano_sel = col_a.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)
        mes_num = meses.index(mes_sel) + 1
        titulo_periodo = f"MENSAL ({mes_sel}/{ano_sel})"
        servicos_filtrados = [s for s in todos if datetime.strptime(s['data'], "%d/%m/%Y %H:%M").month == mes_num and datetime.strptime(s['data'], "%d/%m/%Y %H:%M").year == ano_sel]
        
    elif tipo == "Anual":
        ano_sel = st.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)
        titulo_periodo = f"ANUAL ({ano_sel})"
        servicos_filtrados = [s for s in todos if datetime.strptime(s['data'], "%d/%m/%Y %H:%M").year == ano_sel]

    st.divider()
    
    if not servicos_filtrados:
        st.warning(f"Nenhum serviço encontrado para o período {titulo_periodo}.")
    else:
        st.success(f"Foram encontrados {len(servicos_filtrados)} serviços para o período {titulo_periodo}.")
        pdf_bytes = gerar_pdf_relatorio_consolidado(servicos_filtrados, titulo_periodo)
        
        st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=pdf_bytes,
            file_name=f"Relatorio_{tipo}_{titulo_periodo.replace('/', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    
    if st.button("Fechar", use_container_width=True):
        st.session_state.pop("abrir_modal_exportar", None)
        st.rerun()

def normalizar_pecas_editor(pecas_df):
    pecas = []
    if hasattr(pecas_df, "to_dict"):
        registros = pecas_df.to_dict("records")
    else:
        registros = pecas_df

    for registro in registros:
        nome = str(registro.get("Peca", "")).strip()
        preco = registro.get("Valor Unitario", 0)
        quantidade = registro.get("Quantidade", 1)

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

        pecas.append({
            "nome": nome,
            "preco": preco_float,
            "quantidade": quantidade_int,
            "total": round(preco_float * quantidade_int, 2),
        })

    return pecas


def preparar_pecas_editor(pecas):
    return [
        {
            "Peca": peca.get("nome", ""),
            "Quantidade": int(peca.get("quantidade", 1) or 1),
            "Valor Unitario": float(peca.get("preco", 0) or 0),
            "Total": float(peca.get("total", (peca.get("quantidade", 1) or 1) * (peca.get("preco", 0) or 0)) or 0),
        }
        for peca in (pecas or [])
    ] or [{"Peca": "", "Quantidade": 1, "Valor Unitario": 0.0, "Total": 0.0}]


def existe_linha_vazia(registros):
    return any(not str(registro.get("Peca", "")).strip() for registro in registros)


@st.dialog("Serviço", width="large")
def modal_servico(modo, cliente_id, carro_id, servico_atual=None):
    tipos_servico = gerenciador.get_tipos_servico()
    titulo = "Criar Serviço" if modo == "criar" else "Editar Serviço"
    st.markdown(f"### {titulo}")

    tipo_inicial = ""
    descricao_inicial = ""
    pecas_iniciais = []

    if servico_atual:
        tipo_inicial = servico_atual.get("servico", "")
        descricao_inicial = servico_atual.get("descricao", "")
        pecas_iniciais = servico_atual.get("pecas", [])

    editor_state_key = f"editor_pecas_state_{modo}_{servico_atual['id'] if servico_atual else 'novo'}"

    if editor_state_key not in st.session_state:
        st.session_state[editor_state_key] = preparar_pecas_editor(pecas_iniciais)

    indice_tipo = tipos_servico.index(tipo_inicial) if tipo_inicial in tipos_servico else 0

    tipo_servico = st.selectbox("Tipo de Serviço", tipos_servico, index=indice_tipo)
    st.markdown("#### Peças")
    registros_atuais = st.session_state[editor_state_key]
    header_nome, header_qtd, header_unit, header_total, header_remove = st.columns([3.5, 1.2, 1.5, 1.4, 0.8])
    header_nome.markdown("**Peça**")
    header_qtd.markdown("**Quantidade**")
    header_unit.markdown("**Valor Unitário**")
    header_total.markdown("**Valor Total**")

    for indice, registro in enumerate(registros_atuais):
        col_nome, col_qtd, col_unit, col_total, col_remove = st.columns([3.5, 1.2, 1.5, 1.4, 0.8])

        nome = col_nome.text_input("Peça", value=registro["Peca"], key=f"peca_nome_{editor_state_key}_{indice}", label_visibility="collapsed", placeholder="Nome da peça")
        quantidade = col_qtd.number_input("Quantidade", min_value=1, step=1, value=int(registro["Quantidade"] or 1), key=f"peca_qtd_{editor_state_key}_{indice}", label_visibility="collapsed")
        valor_unitario = col_unit.number_input("Valor Unitário", min_value=0.0, step=0.01, value=float(registro["Valor Unitario"] or 0.0), key=f"peca_valor_{editor_state_key}_{indice}", label_visibility="collapsed")
        total = round(quantidade * valor_unitario, 2)
        col_total.markdown("<div style='height: 0.2rem;'></div>", unsafe_allow_html=True)
        col_total.markdown(f"<div style='font-weight: 600; padding-top: 0.00rem;'>{formatar_moeda(total)}</div>", unsafe_allow_html=True)

        registros_atuais[indice] = {
            "Peca": nome,
            "Quantidade": quantidade,
            "Valor Unitario": valor_unitario,
            "Total": total,
        }

        pode_remover = len(registros_atuais) > 1 or str(nome).strip()
        if col_remove.button("✕", key=f"remover_peca_{editor_state_key}_{indice}", use_container_width=True, disabled=not pode_remover):
            registros_atuais.pop(indice)
            if not registros_atuais:
                registros_atuais.append({"Peca": "", "Quantidade": 1, "Valor Unitario": 0.0, "Total": 0.0})
            st.session_state[editor_state_key] = registros_atuais
            st.rerun()

    st.session_state[editor_state_key] = registros_atuais

    if st.button("＋ Adicionar item", use_container_width=True, disabled=existe_linha_vazia(registros_atuais)):
        registros_atuais = st.session_state[editor_state_key]
        registros_atuais.append({"Peca": "", "Quantidade": 1, "Valor Unitario": 0.0, "Total": 0.0})
        st.session_state[editor_state_key] = registros_atuais
        st.rerun()

    pecas = normalizar_pecas_editor(registros_atuais)
    valor_total_pecas = sum(float(peca.get("total", 0) or 0) for peca in pecas)

    if pecas:
        st.markdown(f"**Total das peças:** {formatar_moeda(valor_total_pecas)}")
        st.dataframe(
            preparar_pecas_editor(pecas),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Peca": "Peça",
                "Quantidade": "Quantidade",
                "Valor Unitario": st.column_config.NumberColumn("Valor Unitário", format="R$ %.2f"),
                "Total": st.column_config.NumberColumn("Total", format="R$ %.2f"),
            },
        )

    descricao = st.text_area("Descrição", value=descricao_inicial, placeholder="Detalhes do serviço realizado...", height=140)

    col_salvar, col_cancelar = st.columns(2)
    salvar = col_salvar.button("✓ Salvar", use_container_width=True, type="primary")
    cancelar = col_cancelar.button("✕ Cancelar", use_container_width=True)

    if cancelar:
        if servico_atual:
            st.session_state.edit_servico_id = None
        else:
            st.session_state.pop("abrir_modal_novo_servico", None)
        st.session_state.pop(editor_state_key, None)
        st.rerun()

    if salvar:
        if modo == "criar":
            resultado = gerenciador.adicionar_servico(
                cliente_id=cliente_id,
                carro_id=carro_id,
                servico=tipo_servico,
                descricao=descricao,
                pecas=pecas,
            )
        else:
            resultado = gerenciador.editar_servico(
                cliente_id=cliente_id,
                carro_id=carro_id,
                servico_id=servico_atual["id"],
                servico=tipo_servico,
                descricao=descricao,
                pecas=pecas,
            )

        if resultado:
            if servico_atual:
                st.session_state.edit_servico_id = None
            else:
                st.session_state.pop("abrir_modal_novo_servico", None)
            st.session_state.pop(editor_state_key, None)
            st.success("✅ Serviço salvo com sucesso!", icon="✅")
            st.rerun()
        st.error("❌ Erro ao salvar serviço", icon="❌")

# ==================== PÁGINA 0: DASHBOARD ====================
if st.session_state.pagina_atual == "dashboard":
    import streamlit.components.v1 as components
    
    # Criar header fixo no topo com nome da oficina e relógio
    header_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * { margin: 0; padding: 0; }
            body {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.5rem 2rem;
                background-color: white;
                color: #111827;
                border-bottom: 1px solid #e5e7eb;
                z-index: 9999;
                font-family: Arial, sans-serif;
                height: 60px;
                box-sizing: border-box;
            }
            .header-logo {
                font-size: 1.25rem;
                font-weight: bold;
                color: #ef4444;
            }
            .header-clock {
                font-size: 1.25rem;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <div class="header-logo">RED CAR</div>
        <div class="header-clock" id="clock">00:00:00</div>
        
        <script>
            function updateClock() {
                const now = new Date();
                const hours = String(now.getHours()).padStart(2, '0');
                const minutes = String(now.getMinutes()).padStart(2, '0');
                const seconds = String(now.getSeconds()).padStart(2, '0');
                document.getElementById('clock').textContent = hours + ':' + minutes + ':' + seconds;
            }
            updateClock();
            setInterval(updateClock, 1000);
        </script>
    </body>
    </html>
    """
    
    # Renderizar o header
    components.html(header_html, height=68)
    
    st.markdown("### Menu Principal")

    if st.button("👥 Registro de Clientes", key="btn_clientes_dash", use_container_width=True, type="primary"):
        st.session_state.pagina_atual = "clientes"
        st.session_state.cliente_atual = None
        st.session_state.carro_atual = None
        st.rerun()

    if st.button("🕐 Histórico de Serviços", key="btn_historico_dash", use_container_width=True):
        st.session_state.pagina_atual = "historico"
        st.rerun()

    if st.button("📊 Relatórios Mensais", key="btn_relatorios_dash", use_container_width=True):
        st.session_state.pagina_atual = "relatorios"
        st.rerun()

    if st.button("⚙️ Configurações", key="btn_config_dash", use_container_width=True):
        st.session_state.pagina_atual = "configuracoes"
        st.rerun()

    st.divider()
    if st.button("🚪 Sair do Sistema", key="btn_logout_dash", use_container_width=True):
        st.session_state["authenticated"] = False
        st.query_params.clear()
        st.rerun()

# ==================== BARRA DE NAVEGAÇÃO (Para outras páginas) ====================
elif st.session_state.pagina_atual != "dashboard":
    col_nav_home, col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([0.5, 1, 1, 1, 1])
    
    with col_nav_home:
        if st.button("🏠", use_container_width=True, help="Voltar ao menu principal"):
            voltar_dashboard()
    
    with col_nav1:
        if st.button("👥 Clientes", use_container_width=True, type="primary" if st.session_state.pagina_atual == "clientes" else "secondary"):
            st.session_state.pagina_atual = "clientes"
            st.session_state.cliente_atual = None
            st.session_state.carro_atual = None
            st.session_state.edit_servico_id = None
            st.rerun()

    with col_nav2:
        if st.button("🕐 Histórico", use_container_width=True, type="primary" if st.session_state.pagina_atual == "historico" else "secondary"):
            st.session_state.pagina_atual = "historico"
            st.rerun()

    with col_nav3:
        if st.button("📊 Relatórios", use_container_width=True, type="primary" if st.session_state.pagina_atual == "relatorios" else "secondary"):
            st.session_state.pagina_atual = "relatorios"
            st.rerun()

    with col_nav4:
        if st.button("⚙️ Configurações", use_container_width=True, type="secondary"):
            st.session_state.pagina_atual = "configuracoes"
            st.rerun()
    
    st.divider()

# ==================== PÁGINA 1: CLIENTES ====================
if st.session_state.pagina_atual == "clientes":
    st.markdown("## 👥 Gerenciamento de Clientes")
    st.markdown("---")

    st.markdown("### 📋 Clientes Cadastrados")
    clientes = gerenciador.obter_clientes()

    if not clientes:
        st.info("📌 Nenhum cliente cadastrado. Comece adicionando um novo cliente!", icon="ℹ️")
    else:
        search_cliente = st.text_input("🔍 Buscar cliente", placeholder="Nome ou telefone...", key="search_cli")

        clientes_filtrados = [
            c for c in clientes
            if search_cliente.lower() in c['nome'].lower() or search_cliente.lower() in c['telefone']
        ]

        st.markdown(f"**Total:** {len(clientes_filtrados)}/{len(clientes)} cliente(s)")
        st.divider()

        if not clientes_filtrados:
            st.info("📌 Nenhum cliente encontrado com o filtro informado.", icon="ℹ️")
        else:
            with st.container(height=calcular_altura_lista(len(clientes_filtrados)), border=False):
                for cliente in clientes_filtrados:
                    carros = gerenciador.obter_carros_cliente(cliente['id'])

                    with st.container(border=True):
                        col_info, col_actions = st.columns([4, 2])

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
                                if st.button("✏️", key=f"btn_edit_cli_{cliente['id']}", use_container_width=True, help="Editar"):
                                    st.session_state[f"edit_{cliente['id']}"] = True
                                    st.rerun()
                            with col_s:
                                if st.button("🗑️", key=f"btn_del_cli_{cliente['id']}", use_container_width=True, help="Deletar"):
                                    if gerenciador.deletar_cliente(cliente['id']):
                                        st.success("✅ Cliente removido", icon="✅")
                                        st.rerun()
                                    else:
                                        st.error("Erro ao deletar", icon="❌")

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

    st.divider()
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
    
    st.markdown("### 📋 Carros Cadastrados")
    carros = gerenciador.obter_carros_cliente(st.session_state.cliente_atual)

    if not carros:
        st.info("📌 Nenhum carro cadastrado. Adicione o primeiro carro!", icon="ℹ️")
    else:
        search_carro = st.text_input("🔍 Buscar carro", placeholder="Marca, modelo ou placa...", key="search_car")

        carros_filtrados = [
            c for c in carros
            if search_carro.lower() in c['marca'].lower()
            or search_carro.lower() in c['modelo'].lower()
            or search_carro.lower() in c['placa'].lower()
        ]

        st.markdown(f"**Total:** {len(carros_filtrados)}/{len(carros)} carro(s)")
        st.divider()

        if not carros_filtrados:
            st.info("📌 Nenhum carro encontrado com o filtro informado.", icon="ℹ️")
        else:
            with st.container(height=calcular_altura_lista(len(carros_filtrados)), border=False):
                for carro in carros_filtrados:
                    servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, carro['id'])

                    with st.container(border=True):
                        col_info, col_actions = st.columns([4, 2])

                        with col_info:
                            st.markdown(f"**{carro['marca']} {carro['modelo']}**", help=f"ID: {carro['id']}")
                            st.markdown(f"📋 Placa: {carro['placa']} • 📅 Ano: {carro['ano']} • 🛠️ {len(servicos)} serviço(s)")

                        with col_actions:
                            col_s, col_e, col_d = st.columns(3)
                            with col_s:
                                if st.button("✓", key=f"btn_srv_{carro['id']}", use_container_width=True, help="Ver serviços"):
                                    st.session_state.carro_atual = carro['id']
                                    st.session_state.pagina_atual = "servicos"
                                    st.session_state.edit_servico_id = None
                                    st.rerun()
                            with col_e:
                                if st.button("✏️", key=f"btn_edit_car_{carro['id']}", use_container_width=True, help="Editar"):
                                    st.session_state[f"edit_car_{carro['id']}"] = True
                                    st.rerun()
                            with col_d:
                                if st.button("🗑️", key=f"btn_del_car_{carro['id']}", use_container_width=True, help="Deletar"):
                                    if gerenciador.deletar_carro(st.session_state.cliente_atual, carro['id']):
                                        st.success("✅ Carro removido", icon="✅")
                                        st.rerun()

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

    st.divider()
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

        if st.session_state.get("abrir_modal_novo_servico"):
            modal_servico("criar", st.session_state.cliente_atual, st.session_state.carro_atual)
        
        st.markdown("### 📋 Serviços Cadastrados")
        servicos = gerenciador.obter_servicos_carro(st.session_state.cliente_atual, st.session_state.carro_atual)

        if not servicos:
            st.info("📌 Nenhum serviço cadastrado. Registre o primeiro serviço!", icon="ℹ️")
        else:
            search_servico = st.text_input("🔍 Buscar serviço", placeholder="Tipo de serviço...", key="search_srv")

            servicos_filtrados = [
                s for s in servicos
                if search_servico.lower() in s['servico'].lower()
            ]

            st.markdown(f"**Total:** {len(servicos_filtrados)}/{len(servicos)} serviço(s)")
            st.divider()

            if not servicos_filtrados:
                st.info("📌 Nenhum serviço encontrado com o filtro informado.", icon="ℹ️")
            else:
                with st.container(height=calcular_altura_lista(len(servicos_filtrados)), border=False):
                    for srv in servicos_filtrados:
                        with st.container(border=True):
                            col_info, col_actions = st.columns([4, 2])

                            with col_info:
                                st.markdown(f"**{srv['servico']}**", help=f"ID: {srv['id']}")
                                st.markdown(f"📅 {srv['data']}")
                                pecas = srv.get('pecas', [])
                                if pecas:
                                    total_itens = sum(int(peca.get('quantidade', 1) or 1) for peca in pecas)
                                    valor_pecas = sum(float(peca.get('total', peca.get('preco', 0)) or 0) for peca in pecas)
                                    st.markdown(f"🔩 {total_itens} item(ns) • {formatar_moeda(valor_pecas)}")
                                if srv['descricao']:
                                    st.markdown(f"📝 *{srv['descricao']}*")

                            with col_actions:
                                col_e, col_d, col_p = st.columns(3)
                                with col_e:
                                    if st.button("✏️", key=f"btn_edit_srv_{srv['id']}", use_container_width=True, help="Editar"):
                                        st.session_state.edit_servico_id = srv['id']
                                        st.rerun()
                                with col_d:
                                    if st.button("🗑️", key=f"btn_del_srv_{srv['id']}", use_container_width=True, help="Deletar"):
                                        if gerenciador.deletar_servico(st.session_state.cliente_atual, st.session_state.carro_atual, srv['id']):
                                            st.success("✅ Serviço removido", icon="✅")
                                            st.rerun()
                                with col_p:
                                    carro_pdf = {'marca': carro['marca'], 'modelo': carro['modelo'], 'placa': carro['placa'], 'ano': carro['ano']}
                                    srv_pdf = {'id': srv['id'], 'servico': srv['servico'], 'data': srv['data'], 'descricao': srv['descricao'], 'pecas': srv.get('pecas', [])}
                                    pdf_b = gerar_pdf_servico(cliente['nome'], cliente['telefone'], carro_pdf, srv_pdf)
                                    st.download_button("📄", data=pdf_b, file_name=f"OS_{srv['id']}.pdf", mime="application/pdf", key=f"pdf_srv_{srv['id']}", help="Baixar PDF")

                        if st.session_state.edit_servico_id == srv['id']:
                            modal_servico("editar", st.session_state.cliente_atual, st.session_state.carro_atual, srv)

        st.divider()
        st.markdown("### ➕ Adicionar Serviço")
        if st.button("➕ Criar Serviço", use_container_width=True, type="primary"):
            st.session_state["abrir_modal_novo_servico"] = True
            st.rerun()

# ==================== PÁGINA 4: HISTÓRICO DE SERVIÇOS ====================
elif st.session_state.pagina_atual == "historico":
    st.markdown("## 🕐 Histórico de Serviços")
    st.markdown("---")
    
    # Search e filtros
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_historico = st.text_input("🔍 Buscar por cliente, carro ou serviço", placeholder="Digite para filtrar...", key="search_hist")
    
    with col_filter:
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + gerenciador.get_tipos_servico(), key="filter_tipo_hist")
    
    # Obter todos os serviços
    todos_servicos = gerenciador.obter_todos_servicos()
    
    # Aplicar filtros
    servicos_filtrados = []
    for srv in todos_servicos:
        match_search = (search_historico.lower() in srv['cliente_nome'].lower() or
                       search_historico.lower() in srv['carro_marca'].lower() or
                       search_historico.lower() in srv['carro_modelo'].lower() or
                       search_historico.lower() in srv['carro_placa'].lower() or
                       search_historico.lower() in srv['servico_tipo'].lower())
        
        match_tipo = filtro_tipo == "Todos" or srv['servico_tipo'] == filtro_tipo
        
        if match_search and match_tipo:
            servicos_filtrados.append(srv)
    
    st.markdown(f"**Total de serviços:** {len(servicos_filtrados)}")
    st.divider()
    
    if not servicos_filtrados:
        st.info("📌 Nenhum serviço encontrado com os filtros aplicados.", icon="ℹ️")
    else:
        with st.container(height=calcular_altura_lista(len(servicos_filtrados)), border=False):
            for srv in servicos_filtrados:
                with st.container(border=True):
                    col_info, col_details = st.columns([2, 1])
                    
                    with col_info:
                        st.markdown(f"**{srv['servico_tipo']}**")
                        st.markdown(f"👤 {srv['cliente_nome']} • 🚗 {srv['carro_marca']} {srv['carro_modelo']} ({srv['carro_placa']})")
                        st.markdown(f"📅 {srv['data']}")
                        if srv.get('total_pecas', 0):
                            quantidade_total = sum(int(peca.get('quantidade', 1) or 1) for peca in srv.get('pecas', []))
                            st.markdown(f"🔩 {quantidade_total} item(ns) • {formatar_moeda(srv.get('valor_pecas', 0))}")
                        if srv['descricao']:
                            st.markdown(f"📝 *{srv['descricao']}*")
                    
                    with col_details:
                        st.markdown(f"<div style='text-align: right; color: #6b7280; font-size: 0.875rem;'><strong>Ano:</strong> {srv['carro_ano']}</div>", unsafe_allow_html=True)
                        carro_pdf = {'marca': srv['carro_marca'], 'modelo': srv['carro_modelo'], 'placa': srv['carro_placa'], 'ano': srv['carro_ano']}
                        srv_pdf = {'id': srv['servico_id'], 'servico': srv['servico_tipo'], 'data': srv['data'], 'descricao': srv['descricao'], 'pecas': srv.get('pecas', [])}
                        pdf_b = gerar_pdf_servico(srv['cliente_nome'], srv['cliente_telefone'], carro_pdf, srv_pdf)
                        st.download_button("📄 Baixar PDF", data=pdf_b, file_name=f"OS_{srv['servico_id']}.pdf", mime="application/pdf", key=f"pdf_hist_{srv['servico_id']}", use_container_width=True)

# ==================== PÁGINA 5: RELATÓRIOS MENSAIS ====================
elif st.session_state.pagina_atual == "relatorios":
    st.markdown("## 📊 Relatórios Mensais")
    st.markdown("---")
    
    # Obter meses com dados
    periodos = gerenciador.obter_meses_com_dados()
    
    if not periodos:
        st.info("📌 Nenhum serviço registrado no sistema ainda.", icon="ℹ️")
    else:
        # Seletor de período
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Criar opções de mês/ano
            opcoes_periodo = [f"{mes:02d}/{ano}" for mes, ano in periodos]
            periodo_selecionado = st.selectbox("Selecione o período", opcoes_periodo, key="periodo_rel")
            mes, ano = map(int, periodo_selecionado.split('/'))
        
        with col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("📥 Exportar Relatório", use_container_width=True):
                st.session_state["abrir_modal_exportar"] = True
                st.rerun()

        if st.session_state.get("abrir_modal_exportar"):
            modal_exportar_relatorio()
        
        st.divider()
        
        # Gerar relatório
        relatorio = gerenciador.gerar_relatorio_mensal(mes, ano)
        
        if relatorio:
            # Estatísticas gerais
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            
            with col_stats1:
                st.metric("Total de Serviços", relatorio['total_servicos'])
            
            with col_stats2:
                st.metric("Tipos de Serviço", len(relatorio['tipos_servico']))
            
            with col_stats3:
                st.metric("Clientes Atendidos", len(relatorio['clientes']))
            
            st.divider()
            
            # Gráficos
            col_graph1, col_graph2 = st.columns(2)
            
            with col_graph1:
                st.markdown("### 📈 Top Serviços")
                if relatorio['tipos_servico']:
                    import pandas as pd
                    df_tipos = pd.DataFrame(list(relatorio['tipos_servico'].items()), columns=['Tipo', 'Quantidade'])
                    df_tipos = df_tipos.sort_values('Quantidade', ascending=False)
                    st.bar_chart(df_tipos.set_index('Tipo'))
                else:
                    st.info("Sem dados", icon="ℹ️")
            
            with col_graph2:
                st.markdown("### 👥 Top Clientes")
                if relatorio['clientes']:
                    import pandas as pd
                    df_clientes = pd.DataFrame(list(relatorio['clientes'].items()), columns=['Cliente', 'Quantidade'])
                    df_clientes = df_clientes.sort_values('Quantidade', ascending=False).head(5)
                    st.bar_chart(df_clientes.set_index('Cliente'))
                else:
                    st.info("Sem dados", icon="ℹ️")
            
            st.divider()
            
            # Listagem detalhada
            st.markdown("### 📋 Serviços do Período")

            if not relatorio['servicos']:
                st.info("📌 Nenhum serviço encontrado para o período selecionado.", icon="ℹ️")
            else:
                with st.container(height=calcular_altura_lista(len(relatorio['servicos'])), border=False):
                    for srv in relatorio['servicos']:
                        with st.container(border=True):
                            col_srv_info, col_srv_details = st.columns([2.5, 1.5])
                            
                            with col_srv_info:
                                st.markdown(f"**{srv['servico_tipo']}**")
                                st.markdown(f"👤 {srv['cliente_nome']}")
                                st.markdown(f"🚗 {srv['carro_marca']} {srv['carro_modelo']} - Placa: {srv['carro_placa']}")
                                if srv.get('total_pecas', 0):
                                    quantidade_total = sum(int(peca.get('quantidade', 1) or 1) for peca in srv.get('pecas', []))
                                    st.markdown(f"🔩 {quantidade_total} item(ns) • {formatar_moeda(srv.get('valor_pecas', 0))}")
                                if srv['descricao']:
                                    st.markdown(f"📝 *{srv['descricao']}*")
                            
                            with col_srv_details:
                                st.markdown(f"<div style='text-align: right;'><strong>📅</strong><br/>{srv['data']}</div>", unsafe_allow_html=True)
                                carro_pdf = {'marca': srv['carro_marca'], 'modelo': srv['carro_modelo'], 'placa': srv['carro_placa'], 'ano': srv['carro_ano']}
                                srv_pdf = {'id': srv['servico_id'], 'servico': srv['servico_tipo'], 'data': srv['data'], 'descricao': srv['descricao'], 'pecas': srv.get('pecas', [])}
                                pdf_b = gerar_pdf_servico(srv['cliente_nome'], srv['cliente_telefone'], carro_pdf, srv_pdf)
                                st.download_button("📄 PDF", data=pdf_b, file_name=f"OS_REL_{srv['servico_id']}.pdf", mime="application/pdf", key=f"pdf_rel_{srv['servico_id']}", use_container_width=True)

# ==================== PÁGINA 6: CONFIGURAÇÕES ====================
elif st.session_state.pagina_atual == "configuracoes":
    st.markdown("## ⚙️ Configurações")
    st.markdown("---")
    
    with st.expander("📋 Tipos de Serviço Disponíveis", expanded=False):
        tipos = gerenciador.get_tipos_servico()
        for i, tipo in enumerate(tipos, 1):
            st.write(f"{i}. {tipo}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 0.875rem; margin-top: 2rem;'>
    <p><strong style='color: #dc2626;'>🚗 RED CAR</strong> • Sistema de Gerenciamento | Desenvolvido por Gabriel Teixeira</p>
    <p style='margin-top: 0.5rem;'><em>Versão Web • 2026</em></p>
</div>
""", unsafe_allow_html=True)

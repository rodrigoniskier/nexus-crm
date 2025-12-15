import streamlit as st
import pandas as pd
import plotly.express as px
import database as db

# --- Configuração da Página ---
st.set_page_config(
    page_title="Nexus CRM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o banco de dados
db.init_db()

# --- CSS: Tema "Modern Corporate Light" ---
st.markdown("""
<style>
    /* Importando Fonte Moderna (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Fundo Geral e Fonte Base */
    .stApp {
        background-color: #F9FAFB; /* Cinza muito claro/Branco Gelo */
        color: #1F2937; /* Cinza Escuro para texto (melhor contraste que preto puro) */
        font-family: 'Inter', sans-serif;
    }

    /* Títulos (Azul Profundo) */
    h1, h2, h3 {
        color: #1E3A8A !important; /* Azul Marinho */
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Subtítulos e Descrições */
    p, label {
        color: #4B5563; /* Cinza médio */
    }

    /* --- COMPONENTES --- */

    /* Botão Primário (Laranja para Ação) */
    .stButton>button {
        background-color: #F97316; /* Laranja Vibrante */
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #EA580C; /* Laranja mais escuro */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Botão Secundário/Delete (Vermelho discreto) */
    button[kind="primary"] {
        background-color: #EF4444 !important;
        color: white !important;
    }

    /* Cartões de Métricas (Branco com Borda Azul/Verde) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB; /* Borda cinza suave */
        border-left: 5px solid #3B82F6; /* Azul no canto */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        color: #111827 !important; /* Quase preto */
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 0.9rem;
    }

    /* Inputs e Selects (Fundo Branco) */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>div, 
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #FFFFFF;
        color: #1F2937;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
    }

    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    /* Ajuste da Tabela */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        background-color: white;
    }
    
    /* Remover menu padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL: Formulário ---
with st.sidebar:
    st.markdown("### ADD NEW RECORD")
    st.markdown("Enter details below to register a new deal.")
    
    with st.form("new_deal_form", clear_on_submit=True):
        company = st.text_input("COMPANY NAME")
        contact = st.text_input("CONTACT PERSON")
        email = st.text_input("EMAIL ADDRESS")
        phone = st.text_input("PHONE / WHATSAPP")
        status = st.selectbox("CURRENT STAGE", ["Lead", "Negotiation", "Proposal Sent", "Active", "Closed Won", "Lost"])
        value = st.number_input("DEAL VALUE ($)", min_value=0.0, step=100.0, format="%.2f")
        notes = st.text_area("NOTES / REQUIREMENTS")
        
        # Botão de submissão
        submitted = st.form_submit_button("SAVE DEAL")
        
        if submitted and company:
            db.add_deal(company, contact, email, phone, status, value, notes)
            st.success("RECORD SAVED SUCCESSFULLY")
            st.rerun()

# --- ÁREA PRINCIPAL ---

# Cabeçalho
st.title("NEXUS CRM")
st.markdown("**FREELANCE BUSINESS MANAGEMENT SYSTEM**")

# A DESCRIÇÃO SOLICITADA
st.markdown("""
<div style="background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 15px; border-radius: 4px; margin-bottom: 25px;">
    <p style="margin:0; color: #1E40AF; font-size: 0.95rem;">
    <strong>System Overview:</strong> This portal is a centralized Customer Relationship Management (CRM) tool designed to track client interactions, 
    manage deal pipelines, and analyze revenue streams in real-time. It uses a persistent SQL database to ensure secure data storage and retrieval.
    </p>
</div>
""", unsafe_allow_html=True)

# Carregar Dados
df = db.view_all_deals()

if not df.empty:
    # --- KPIs (Indicadores) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_pipeline = df['value'].sum()
    active_count = df[df['status'] == 'Active'].shape[0]
    avg_deal = df['value'].mean()
    # Tratamento para evitar divisão por zero
    win_rate = (len(df[df['status']=='Closed Won']) / len(df) * 100) if len(df) > 0 else 0
    
    # Customização de cores nas métricas via lógica simples
    col1.metric("TOTAL PIPELINE", f"${total_pipeline:,.2f}")
    col2.metric("ACTIVE CLIENTS", active_count)
    col3.metric("AVG DEAL SIZE", f"${avg_deal:,.2f}")
    col4.metric("WIN RATE", f"{win_rate:.1f}%")
    
    st.markdown("---")
    
    # --- GRÁFICOS ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("REVENUE DISTRIBUTION")
        # Gráfico de Barras (Azul e Verde)
        # Usamos uma paleta de azuis/verdes profissionais
        color_map = {
            "Closed Won": "#10B981", # Verde
            "Active": "#3B82F6", # Azul
            "Negotiation": "#F59E0B", # Laranja
            "Lead": "#9CA3AF", # Cinza
            "Lost": "#EF4444" # Vermelho
        }
        
        fig_bar = px.bar(df, x='status', y='value', color='status', 
                         title="", template="plotly_white",
                         color_discrete_map=color_map)
        
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "Inter, sans-serif", 'color': '#1F2937'},
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.subheader("DEAL COMPOSITION")
        # Gráfico de Rosca
        fig_pie = px.pie(df, names='status', values='value', hole=0.5, template="plotly_white",
                         color='status', color_discrete_map=color_map)
        fig_pie.update_layout(
            showlegend=False, 
            paper_bgcolor="rgba(0,0,0,0)",
            font={'family': "Inter, sans-serif", 'color': '#1F2937'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABELA DE REGISTROS ---
    st.markdown("---")
    st.subheader("CLIENT DATABASE RECORDS")
    
    # Filtro
    all_status = list(df['status'].unique())
    filter_status = st.multiselect("FILTER VIEW BY STAGE", all_status)
    
    if filter_status:
        df_view = df[df['status'].isin(filter_status)]
    else:
        df_view = df
        
    st.dataframe(
        df_view, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "value": st.column_config.NumberColumn("Value", format="$%.2f")
        }
    )
    
    # --- GERENCIAMENTO (Update/Delete) ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("MANAGE SELECTED RECORD"):
        st.markdown("Select a Deal ID below to update its status or remove it from the database.")
        
        col_select, col_action = st.columns([1, 2])
        
        with col_select:
            deal_id_to_edit = st.selectbox("SELECT DEAL ID", df['id'])
            # Feedback visual do item selecionado
            if not df.empty and deal_id_to_edit:
                selected_row = df[df['id'] == deal_id_to_edit].iloc[0]
                st.info(f"SELECTED: {selected_row['company_name']} | Current: {selected_row['status']}")
            
        with col_action:
            c_a, c_b = st.columns(2)
            with c_a:
                new_status_val = st.selectbox("UPDATE STAGE", ["Lead", "Negotiation", "Active", "Closed Won", "Lost"])
                if st.button("UPDATE STATUS"):
                    db.update_status(deal_id_to_edit, new_status_val)
                    st.rerun()
            with c_b:
                st.write("") 
                st.write("")
                # Botão de deletar (usará o estilo vermelho definido no CSS)
                if st.button("DELETE RECORD", type="primary"):
                    db.delete_deal(deal_id_to_edit)
                    st.rerun()

else:
    # Estado Zero
    st.info("DATABASE EMPTY. PLEASE INITIALIZE BY ADDING RECORDS VIA SIDEBAR.")
    
# Rodapé
st.markdown("---")
st.markdown('<div style="text-align: center; color: #9CA3AF; font-size: 0.8rem;">Nexus CRM v1.2 | Engineered by <strong>Rodrigo Niskier</strong></div>', unsafe_allow_html=True)
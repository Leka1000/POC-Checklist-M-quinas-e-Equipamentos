import streamlit as st
import pandas as pd
from datetime import date
import os

# Configuração da página
st.set_page_config(
    page_title="Check List Mensal de Equipamentos",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛠️ SISTEMA DE CHECK LIST MENSAL")
st.markdown("---")

# --- SELEÇÃO DO EQUIPAMENTO ---
st.subheader("🚜 Seleção do Equipamento")
equipamento_selecionado = st.selectbox(
    "Escolha o equipamento para inspeção:",
    [
        "Caminhão Basculante",
        "Caminhão Carroceria - Cabine Complementar",
        "Bobcat"
    ]
)

st.markdown("---")

# --- CABEÇALHO DO DOCUMENTO ---
st.subheader("📋 Informações Gerais")
col1, col2, col3 = st.columns(3)

with col1:
    local_servico = st.text_input("Local do Serviço:", value="OBRA LIVIO")
    
    tipo_selecao_id = st.radio("Como deseja informar o equipamento?", ["Escolher Prefixo", "Digitar Personalizado"])
    if tipo_selecao_id == "Escolher Prefixo":
        id_equipamento = st.selectbox("Identificação do Equipamento / Placa / Frota:", ["BOB001", "CB001", "CC001"])
    else:
        id_equipamento = st.text_input("Digite a Identificação do Equipamento / Placa / Frota:")

with col2:
    data_inspecao = st.date_input("Data da Inspeção:", value=date.today())
    revisao = st.text_input("Revisão:", value="00")

with col3:
    periodicidade = st.text_input("Periodicidade da Inspeção:", value="Mensal")
    cor_liberacao = st.selectbox(
        "Cor correspondente à liberação:",
        ["Verde", "Amarelo", "Brancoo", "Azul", "Outra"]
    )

st.markdown("---")

# --- DEFINIÇÃO DOS ITENS POR EQUIPAMENTO EM ORDEM NUMÉRICA CORRETA ---
if equipamento_selecionado == "Caminhão Basculante":

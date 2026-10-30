import streamlit as st
import pandas as pd
from datetime import date
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage

# Configuração da página
st.set_page_config(
    page_title="Check List Mensal de Equipamentos",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛠️ SISTEMA DE CHECK LIST MENSAL")
st.markdown("---")

# --- MÓDULO DE CONSULTA E FILTRAGEM POR PERÍODO (BARRA LATERAL) ---
st.sidebar.subheader("🔍 Consultar Histórico")
modo_consulta = st.sidebar.checkbox("Ativar modo de busca por período")

if modo_consulta:
    st.subheader("📊 Painel de Consulta e Extração por Período")
    caminho_consolidado = os.path.join("historico_geral", "Relatorio_Consolidado_Checklists.xlsx")
    
    if os.path.exists(caminho_consolidado):
        df_historico = pd.read_excel(caminho_consolidado)
        df_historico["Data"] = pd.to_datetime(df_historico["Data"]).dt.date
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            data_inicio = st.date_input("Data Inicial:", value=date.today().replace(day=1))
        with col_f2:
            data_fim = st.date_input("Data Final:", value=date.today())
        with col_f3:
            equip_filtro = st.selectbox("Filtrar Equipamento:", ["Todos"] + list(df_historico["Equipamento"].unique()))
            
        df_filtrado = df_historico[(df_historico["Data"] >= data_inicio) & (df_historico["Data"] <= data_fim)]
        
        if equip_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Equipamento"] == equip_filtro]
            
        st.markdown(f"**Total de registros encontrados no período:** {len(df_filtrado)}")
        st.dataframe(df_filtrado, use_container_width=True)
        
        output_filtro = io.BytesIO()
        with pd.ExcelWriter(output_filtro, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, sheet_name="Filtro_Periodo", index=False)
        excel_filtrado_bytes = output_filtro.getvalue()
        
        st.download_button(
            label="📥 Baixar Extração do Período (Excel)",
            data=excel_filtrado_bytes,
            file_name=f"Relatorio_Filtrado_{data_inicio}_a_{data_fim}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Ainda não há registros consolidados salvos para consulta. Preencha e salve alguns checklists para iniciar o histórico.")
    
    st.markdown("---")

else:
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
            ["Verde", "Amarelo", "Vermelho", "Azul", "Outra"]
        )

    st.markdown("---")

    # --- BASE DE DADOS DOS ITENS DE INSPEÇÃO ---
    CHECKLISTS = {
        "Caminhão Basculante":

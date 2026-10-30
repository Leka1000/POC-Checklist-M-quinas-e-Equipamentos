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
        "Caminhão Basculante": [
            "1. CRLV-e, documentos de operação, inspeções e exigências aplicáveis foram conferidos?",
            "2. Manual, identificação do modelo, modificações e plano de manutenção estão atualizados?",
            "3. Análise de risco e condições de descarga são verificadas antes de cada basculamento?",
            "4. Histórico de manutenção preventiva e corretiva está atualizado, com OS encerradas e evidências?",
            "5. As recomendações do fabricante por quilometragem/tempo estão atendidas e rastreadas?",
            "6. Identificação do veículo, placas, faixas e sinalização foram conferidas quanto à integridade?",
            "7. Os calços são compatíveis com pneus, massa, solo e procedimento de imobilização?",
            "8. Pneus, sulcos, pressão, aros, fixações e reapertos foram avaliados conforme fabricante?",
            "9. Circuitos, suportes, iluminação, relés e lanternas foram inspecionados?",
            "10. Buzina e alarme de ré foram submetidos a teste funcional controlado?",
            "11. Câmera, monitor, fiação, fixação e imagem foram inspecionados e testados?",
            "12. O sensor de presença foi testado em procedimento controlado e teve calibração/posicionamento conferidos?",
            "13. Giroflex, fixações e alimentação elétrica foram avaliados?",
            "14. Estrobo, fixações e alimentação elétrica foram avaliados?",
            "15. Registros, aferição/regularidade do registrador de velocidade foram conferidos?",
            "16. Comandos e dispositivos para prevenir descida involuntária foram testados?",
            "17. Indicadores e intertravamentos de basculamento foram testados?",
            "18. Dispositivos de advertência de marcha à ré tiveram resultado de ensaio controlado registrado?",
            "19. Indicador de caçamba elevada e limitações de basculamento foram testados, quando equipados?",
            "20. Chassi, longarinas, suportes, fixações e soldas estão íntegros, sem reparos irregulares?",
            "21. Foram identificadas e tratadas fugas nos sistemas de combustível, lubrificação, ar e arrefecimento?",
            "22. Extintores e demais meios de emergência foram inspecionados, incluindo fixações e manutenção?",
            "23. Equipamentos de emergência, estepe e ferramentas estão completos e adequados, quando exigidos?",
            "24. Retrovisores, regulagens, fechaduras, vedações e vidros foram avaliados detalhadamente?",
            "25. Estrutura da caçamba, soldas, dobradiças, batentes e travas foram examinados?",
            "26. Pinos, buchas, retenções, suportes e folgas foram inspecionados?",
            "27. Sistema hidráulico de basculamento, vedação, mangueiras e cilindros foi inspecionado?",
            "28. Escora/trava mecânica para caçamba elevada foi examinada, conforme fabricante?",
            "29. Cobertura, acionamentos e fixações foram conferidos?",
            "30. Suspensão, molas, amortecedores, buchas, suportes, terminais de direção, barras e articulações foram avaliados?",
            "31. Linhas e reservatórios pneumáticos/hidráulicos de freio estão íntegros, com drenagem e ensaios previstos?",
            "32. Fixação de cabine ao chassi e respectivos suportes/coxins estão íntegros?",
            "33. Sistema de exaustão, suportes e proteção contra aquecimento indevido estão íntegros?",
            "34. Bateria, chicotes, terminais e proteções elétricas estão íntegros, sem improvisações?",
            "35. Bujões, reservatórios e tampas estão íntegros e identificados, sem vestígios de vazamento?",
            "36. Há evidência de torque/reaperto de fixadores críticos quando previsto em manutenção?",
            "37. A caçamba elevada possui suporte/escora de manutenção estrutural e funcional, com uso restrito?",
            "38. Cinto, ancoragem, fecho e retrator foram inspecionados?",
            "39. Bancos, suportes, pedais, ergonomia e interferências nos comandos foram avaliados?",
            "40. Sistema de limpador, esguichos, braços e palhetas foram testados?",
            "41. Fixação e ancoragem dos cintos e bancos foram avaliadas e documentadas?",
            "42. Falhas, sensores, mensagens do painel e histórico diagnóstico foram verificados?",
            "43. Sistema de freios, componentes, indicadores e ensaios previstos foram conferidos?",
            "44. Freio de estacionamento, acionamento e condição de retenção foram inspecionados?",
            "45. Direção, articulações, transmissão e folgas foram avaliadas?",
            "46. Testes instrumentados ou procedimentos específicos do sistema de frenagem foram realizados quando requeridos?",
            "47. Calços em condições de uso e quantidade suficiente?"
        ],
        "Caminhão Carroceria - Cabine Complementar":

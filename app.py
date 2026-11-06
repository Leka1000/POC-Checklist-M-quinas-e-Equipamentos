from datetime import date
import io
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuração da página
st.set_page_config(
    page_title="Check List Mensal de Equipamentos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SALVAR A IMAGEM DO LOGÓTIPO ENVIADA PARA USO NO APP E NO EXCEL ---
PASTA_DESTINO = "historico_geral"
os.makedirs(PASTA_DESTINO, exist_ok=True)
caminho_logo = os.path.join(PASTA_DESTINO, "logo_ellenco.png")

img_logo_bytes = image_cadfa6
with open(caminho_logo, "wb") as f:
    f.write(img_logo_bytes)

with st.sidebar:
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, use_column_width=True)
    st.markdown("---")
    st.markdown("### Navegação e Filtros")

st.title("🛠️ SISTEMA DE CHECK LIST MENSAL")
st.markdown("---")

# --- SELEÇÃO DO EQUIPAMENTO ---
st.subheader("🚜 Seleção do Equipamento")
equipamento_selecionado = st.selectbox(
    "Escolha o equipamento para inspeção:",
    ["Caminhão Basculante", "Caminhão Carroceria - Cabine Complementar", "Bobcat"],
)

st.markdown("---")

# --- CABEÇALHO DO DOCUMENTO ---
st.subheader("📋 Informações Gerais")
col1, col2, col3 = st.columns(3)

with col1:
    local_servico = st.text_input("Local do Serviço:", value="OBRA LIVIO")

    tipo_selecao_id = st.radio(
        "Como deseja informar o equipamento?",
        ["Escolher Prefixo", "Digitar Personalizado"],
    )
    if tipo_selecao_id == "Escolher Prefixo":
        id_equipamento = st.selectbox(
            "Identificação do Equipamento / Placa / Frota:",
            ["BOB001", "CB001", "CC001"],
        )
    else:
        id_equipamento = st.text_input(
            "Digite a Identificação do Equipamento / Placa / Frota:"
        )

with col2:
    data_inspecao = st.date_input("Data da Inspeção:", value=date.today())
    revisao = st.text_input("Revisão:", value="00")

with col3:
    periodicidade = st.text_input("Periodicidade da Inspeção:", value="Mensal")
    cor_liberacao = st.selectbox(
        "Cor correspondente à liberação:",
        ["Verde", "Amarelo", "Vermelho", "Azul", "Outra"],
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
        "17. Indicadores e inter

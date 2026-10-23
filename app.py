import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Checklist de Pavimentação e Frota",
    page_icon="🚜",
    layout="wide"
)

# --- SIDEBAR: CONFIGURAÇÕES E CREDENCIAIS DO MICROSOFT FOUNDRY ---
st.sidebar.header("🔐 Configurações Microsoft Foundry")
minha_chave = st.sidebar.text_input("Chave de API (minha_chave)", type="password")
meu_endpoint = st.sidebar.text_input("Endpoint (meu_endpoint)")
meu_modelo = st.sidebar.text_input("Modelo (meu_modelo)", value="gpt-4o")

st.sidebar.divider()

# --- SIDEBAR: DADOS DA INSPEÇÃO ---
st.sidebar.header("📋 Dados da Inspeção")
data_inspecao = st.sidebar.date_input("Data", datetime.today())
operador = st.sidebar.text_input("Nome do Operador / Responsável")
obra_trecho = st.sidebar.text_input("Obra / Trecho")

# Seleção do Equipamento (Lista Completa)
equipamento = st.sidebar.selectbox(
    "Selecione o Equipamento",
    [
        "Vibroacabadora de Asfalto",
        "Rolo Compactador Tandem (Chapa)",
        "Rolo Compactador Pneumático",
        "Caminhão Espargidor (Lama/Pintura)",
        "Fresadora de Asfalto",
        "Mini Carregadeira (Com Vassoura)",
        "Equipamento de Terraplenagem (Escavadeira / Pá / Motoniveladora)",
        "Caminhão Basculante",
        "Caminhão Pipa",
        "Ônibus / Transporte de Passageiros"
    ]
)

st.sidebar.divider()

# --- TÍTULO E CABEÇALHO ---
st.title("🚜 Checklist de Inspeção - Equipamentos de Pavimentação e Frota")
st.markdown("Preencha a verificação diária dos equipamentos antes do início das operações.")

# --- DICIONÁRIO DE ITENS DE VERIFICAÇÃO ---
ITENS_CHECKLIST = {
    "Gerais (Todos os Equipamentos)": [
        "Nível do óleo do motor e fluido hidráulico",
        "Nível de combustível e ABLue/ARLA (se aplicável)",
        "Sistema de freios (serviço e estacionamento)",
        "Luzes de sinalização, faróis e giroflex",
        "Alarme de ré e buzina",
        "Extintor de incêndio (validade e pressão)",
        "Vazamentos visíveis (óleo, água, combustível)"
    ],
    "Vibroacabadora de Asfalto": [
        "Estado da mesa compactadora / aquecimento",
        "Condição dos caracóis / roscas transportadoras",
        "Esteiras de alimentação e correntes",
        "Sensor de nivelamento (móvel/laser/ponto fixo)",
        "Sistemas hidráulicos de abertura da mesa"
    ],
    "Rolo Compactador Tandem (Chapa)": [
        "Sistema de aspersão de água nos cilindros",
        "Raspadores dos cilindros (limpeza/desgaste)",
        "Sistema de vibração (amplitude e frequência)",
        "Articulação central e trava de segurança"
    ],
    "Rolo Compactador Pneumático": [
        "Calibragem e estado de conservação dos pneus",
        "Sistema de aspersão de saia / aditivo antiaderente",
        "Sistema de calibragem rápida (se houver)",
        "Raspadores de pneu"
    ],
    "Caminhão Espargidor (Lama/Pintura)": [
        "Condição da barra espargidora e bicos injetores",
        "Funcionamento do maçarico / sistema de aquecimento",
        "Bomba de produto e caneta de pintura manual",
        "Tacômetro / caneta de controle de dosagem"
    ],
    "Fresadora de Asfalto": [
        "Estado das ferramentas de corte (dentes/bits)",
        "Correia transportadora e cinto de descarga",
        "Sistema de aspersão de água para controle de poeira",
        "Sapatas laterais e sensores de profundidade"
    ],
    "Mini Carregadeira (Com Vassoura)": [
        "Cerdas da vassoura recolhedora/varredoura",
        "Engates rápidos do sistema hidráulico",
        "Caixa de recolhimento e basculamento"
    ],
    "Equipamento de Terraplenagem (Escavadeira / Pá / Motoniveladora)": [
        "Estado da caçamba / lâmina e dentes / cantos de corte",
        "Pinos, buchas e pistões hidráulicos (folgas/vazamentos)",
        "Condição das esteiras / pneus e roletes",
        "Articulações, escarificador e trava da lâmina"
    ],
    "Caminhão Basculante": [
        "Trava de segurança da caçamba e tampa traseira",
        "Pistão hidráulico de basculamento (sem vazamentos)",
        "Estado de conservação e calibragem dos pneus",
        "Lona de cobertura da carga e ganchos de amarração"
    ],
    "Caminhão Pipa": [
        "Bomba de água, tomada de força e cardan",
        "Mangote de sucção, barra irrigadora e rabo de pavão",
        "Canhão de água / carretel de mangueira",
        "Estanqueidade do tanque e válvulas de abertura"
    ],
    "Ônibus / Transporte de Passageiros": [
        "Funcionamento das portas e travas de segurança",
        "Condição dos cintos de segurança de todos os assentos",
        "Martelos de emergência e saídas de socorro sinalizadas",
        "Estado dos pneus, estepe, macaco e chave de roda"
    ]
}

# --- FUNÇÃO PARA ENVIAR E-MAIL VIA SMTP ---
def enviar_email(dados_gerais, df_respostas, destinatario="alessandra.nascimento@ellenco.com.br"):
    try:
        remetente = st.secrets["email"]["usuario"]
        senha = st.secrets["email"]["senha"]
        servidor_smtp = st.secrets["email"]["smtp_server"]
        porta = st.secrets["email"]["porta"]

        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = f"Checklist {dados_gerais['Equipamento']} - Prefixo: {dados_gerais['Prefixo/Placa']} ({dados_gerais['Data']})"

        corpo_html = f"""
        <h2>📋 Registro de Checklist de Pavimentação e Frota</h2>
        <p><b>Data:</b> {dados_gerais['Data']}</p>
        <p><b>Operador:</b> {dados_gerais['Operador']}</p>
        <p><b>Obra/Trecho:</b> {dados_gerais['Obra']}</p>
        <p><b>Equipamento:</b> {dados_gerais['Equipamento']}</p>
        <p><b>Prefixo/Placa:</b> {dados_gerais['Prefixo/Placa']}</p>
        <p><b>Horímetro/Quilometragem:</b> {dados_gerais['Horimetro']}</p>

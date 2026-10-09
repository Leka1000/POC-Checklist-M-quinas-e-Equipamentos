# Inicio do projeto
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Checklist de Pavimentação",
    page_icon="🚜",
    layout="wide"
)

# Título e Cabeçalho
st.title("🚜 Checklist de Inspeção - Equipamentos de Pavimentação")
st.markdown("Preencha a verificação diária dos equipamentos antes do início das operações.")

# Sidebar - Informações Gerais
st.sidebar.header("📋 Dados da Inspeção")
data_inspecao = st.sidebar.date_input("Data", datetime.today())
operador = st.sidebar.text_input("Nome do Operador / Responsável")
obra_trecho = st.sidebar.text_input("Obra / Trecho")

# Seleção do Equipamento
equipamento = st.sidebar.selectbox(
    "Selecione o Equipamento",
    [
        "Vibroacabadora de Asfalto",
        "Rolo Compactador Tandem (Chapa)",
        "Rolo Compactador Pneumático",
        "Caminhão Espargidor (Lama/Pintura)",
        "Fresadora de Asfalto",
        "Mini Carregadeira (Com Vassoura)"
    ]
)

st.sidebar.divider()

# Dicionário com itens de verificação por equipamento
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
        "Calibragem e estado de conservação dos pneu",
        "Sistema de aspersão de saia / aditivo antiaderente",
        "SISTEMA DE CALIBRAGEM RÁPIDA (se houver)",
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
    ]
}

# Formulário Principal
with st.form("form_checklist"):
    st.subheader(f"Verificação: {equipamento}")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        horimetro = st.number_input("Horímetro Atual", min_value=0.0, step=0.1)
    with col_info2:
        placa_prefixo = st.text_input("Placa / Prefixo do Equipamento")
    
    st.markdown("---")
    
    respostas = {}
    
    # Renderiza itens gerais
    st.markdown("### 🔍 Itens Gerais de Segurança e Mecânica")
    for item in ITENS_CHECKLIST["Gerais (Todos os Equipamentos)"]:
        respostas[item] = st.radio(
            item,
            ["Conforme", "Não Conforme", "Não Aplicável"],
            horizontal=True,
            key=f"geral_{item}"
        )
    
    # Renderiza itens específicos do equipamento selecionado
    if equipamento in ITENS_CHECKLIST:
        st.markdown(f"### ⚙️ Itens Específicos: {equipamento}")
        for item in ITENS_CHECKLIST[equipamento]:
            respostas[item] = st.radio(
                item,
                ["Conforme", "Não Conforme", "Não Aplicável"],
                horizontal=True,
                key=f"esp_{item}"
            )

    st.markdown("---")
    observacoes = st.text_area("Observações / Anomalias Encontradas")
    foto = st.file_uploader("Anexar foto de eventual anomalia (opcional)", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("💾 Salvar Registro de Inspeção")

# Processamento do formulário
if submitted:
    if not operador or not obra_trecho or not placa_prefixo:
        st.error("⚠️ Por favor, preencha o Nome do Operador, Obra/Trecho e Prefixo do Equipamento na barra lateral.")
    else:
        st.success("✅ Checklist registrado com sucesso!")
        
        # Consolidação dos Dados
        dados_gerais = {
            "Data": data_inspecao.strftime("%d/%m/%Y"),
            "Operador": operador,
            "Obra": obra_trecho,
            "Equipamento": equipamento,
            "Prefixo/Placa": placa_prefixo,
            "Horímetro": horimetro,
            "Observações": observacoes
        }
        
        df_respostas = pd.DataFrame(
            list(respostas.items()), 
            columns=["Item Verificado", "Status"]
        )
        
        # Resumo na Tela
        st.markdown("### 📄 Resumo da Inspeção")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.json(dados_gerais)
        
        with col_res2:
            st.dataframe(df_respostas, use_container_width=True)
            
            # Alerta visual para Não Conformidades
            nao_conformes = df_respostas[df_respostas["Status"] == "Não Conforme"]
            if not nao_conformes.empty:
                st.warning(f"⚠️ Atenção: Foram encontrados {len(nao_conformes)} item(ns) NÃO CONFORME(S)!")
        
        # Download dos dados em CSV
        csv = df_respostas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Checklist (CSV)",
            data=csv,
            file_name=f"checklist_{placa_prefixo}_{data_inspecao}.csv",
            mime="text/csv"
        )
        import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- FUNÇÃO PARA ENVIAR E-MAIL VIA SMTP ---
def enviar_email(dados_gerais, df_respostas, destinatario="alessandra.nascimento@ellenco.com.br"):
    try:
        # Configurações do servidor SMTP (usando os secrets do Streamlit)
        remetente = st.secrets["email"]["usuario"]
        senha = st.secrets["email"]["senha"]
        servidor_smtp = st.secrets["email"]["smtp_server"]
        porta = st.secrets["email"]["porta"]

        # Criação da mensagem
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = f"Checklist {dados_gerais['Equipamento']} - Prefixo: {dados_gerais['Prefixo/Placa']} ({dados_gerais['Data']})"

        # Corpo do E-mail em HTML
        corpo_html = f"""
        <h2>📋 Registro de Checklist de Pavimentação</h2>
        <p><b>Data:</b> {dados_gerais['Data']}</p>
        <p><b>Operador:</b> {dados_gerais['Operador']}</p>
        <p><b>Obra/Trecho:</b> {dados_gerais['Obra']}</p>
        <p><b>Equipamento:</b> {dados_gerais['Equipamento']}</p>
        <p><b>Prefixo/Placa:</b> {dados_gerais['Prefixo/Placa']}</p>
        <p><b>Horímetro:</b> {dados_gerais['Horímetro']}</p>
        <p><b>Observações:</b> {dados_gerais['Observações']}</p>
        <hr>
        <h3>Itens Verificados</h3>
        {df_respostas.to_html(index=False, border=1)}
        """
        
        msg.attach(MIMEText(corpo_html, "html"))

        # Conexão e envio
        with smtplib.SMTP(servidor_smtp, porta) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            
        return True, "E-mail enviado com sucesso!"
    except Exception as e:
        return False, f"Falha ao enviar e-mail: {str(e)}"

# --- PROCESSAMENTO DO FORMULÁRIO ---
# Adicione ou substitua dentro do bloco 'if submitted:'
if submitted:
    if not operador or not obra_trecho or not placa_prefixo:
        st.error("⚠️ Por favor, preencha o Nome do Operador, Obra/Trecho e Prefixo do Equipamento na barra lateral.")
    else:
        dados_gerais = {
            "Data": data_inspecao.strftime("%d/%m/%Y"),
            "Operador": operador,
            "Obra": obra_trecho,
            "Equipamento": equipamento,
            "Prefixo/Placa": placa_prefixo,
            "Horímetro": horimetro,
            "Observações": observacoes
        }
        
        df_respostas = pd.DataFrame(
            list(respostas.items()), 
            columns=["Item Verificado", "Status"]
        )

        # Tenta enviar o e-mail
        with st.spinner("Enviando formulário por e-mail..."):
            sucesso, mensagem = enviar_email(dados_gerais, df_respostas, "alessandra.nascimento@ellenco.com.br")

        if sucesso:
            st.success(f"✅ Checklist registrado e enviado para **alessandra.nascimento@ellenco.com.br**!")
        else:
            st.warning(f"⚠️ Registro salvo localmente, mas não foi possível enviar o e-mail: {mensagem}")

        # Resumo na Tela
        st.markdown("### 📄 Resumo da Inspeção")
        st.dataframe(df_respostas, use_container_width=True)
        

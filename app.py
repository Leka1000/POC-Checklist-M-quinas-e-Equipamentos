import streamlit as st
import pandas as pd
from datetime import date

# Configuração da página
st.set_page_config(
    page_title="Check List Mensal - Caminhão Basculante",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚛 CHECK LIST MENSAL - CAMINHÃO BASCULANTE")
st.markdown("---")

# --- CABEÇALHO DO DOCUMENTO ---
st.subheader("📋 Informações Gerais")
col1, col2, col3 = st.columns(3)

with col1:
    local_servico = st.text_input("Local do Serviço:")
    id_equipamento = st.text_input("Identificação do Equipamento:")
    data_inspecao = st.date_input("Data da Inspeção:", value=date.today())

with col2:
    codigo_doc = st.text_input("Código:", value="CL-CB-001")
    doc_ref = st.text_input("Doc. Referenciado:")
    revisao = st.text_input("Revisão:", value="00")

with col3:
    periodicidade = st.text_input("Periodicidade da Inspeção:", value="Mensal")
    cor_liberacao = st.selectbox(
        "Cor correspondente à liberação:",
        ["Verde", "Amarelo", "Vermelho", "Azul", "Outra"]
    )

st.markdown("---")

# --- LISTA DE ITENS DO CHECKLIST ---
itens_checklist = [
    # Documentação e Gestão
    "1. CRLV-e, documentos de operação, inspeções e exigências aplicáveis foram conferidos?",
    "2. Manual, identificação do modelo, modificações e plano de manutenção estão atualizados?",
    "4. Análise de risco e condições de descarga são verificadas antes de cada basculamento?",
    "5. Histórico de manutenção preventiva e corretiva está atualizado, com OS encerradas e evidências?",
    "6. As recomendações do fabricante por quilometragem/tempo estão atendidas e rastreadas?",
    
    # Estrutura e Mecânica Externa
    "7. Identificação do veículo, placas, faixas e sinalização foram conferidas quanto à integridade?",
    "8. Os calços são compatíveis com pneus, massa, solo e procedimento de imobilização?",
    "9. Pneus, sulcos, pressão, aros, fixações e reapertos foram avaliados conforme fabricante?",
    "11. Chassi, longarinas, suportes, fixações e soldas estão íntegros, sem reparos irregulares?",
    "12. Foram identificadas e tratadas fugas nos sistemas de combustível, lubrificação, ar e arrefecimento?",
    "13. Extintores e demais meios de emergência foram inspecionados, incluindo fixações e manutenção?",
    "14. Equipamentos de emergência, estepe e ferramentas estão completos e adequados, quando exigidos?",
    "15. Retrovisores, regulagens, fechaduras, vedações e vidros foram avaliados detalhadamente?",
    
    # Sistema Basculante e Caçamba
    "16. Estrutura da caçamba, soldas, dobradiças, batentes e travas foram examinados?",
    "17. Pinos, buchas, retenções, suportes e folgas foram inspecionados?",
    "18. Sistema hidráulico de basculamento, vedação, mangueiras e cilindros foi inspecionado?",
    "19. Escora/trava mecânica para caçamba elevada foi examinada, conforme fabricante?",
    "20. Cobertura, acionamentos e fixações foram conferidos?",
    "29. A caçamba elevada possui suporte/escora de manutenção estrutural e funcional, com uso restrito?",
    
    # Suspensão, Direção e Transmissão
    "21/22. Suspensão, molas, amortecedores, buchas, suportes, terminais de direção, barras e articulações foram avaliados?",
    "23. Linhas e reservatórios pneumáticos/hidráulicos de freio estão íntegros, com drenagem e ensaios previstos?",
    "24. Fixação de cabine ao chassi e respectivos suportes/coxins estão íntegros?",
    "25. Sistema de exaustão, suportes e proteção contra aquecimento indevido estão íntegros?",
    "26. Bateria, chicotes, terminais e proteções elétricas estão íntegros, sem improvisações?",
    "27. Bujões, reservatórios e tampas estão íntegros e identificados, sem vestígios de vazamento?",
    "28. Há evidência de torque/reaperto de fixadores críticos quando previsto em manutenção?",
    
    # Cabine, Ergonomia e Segurança Interna
    "30. Cinto, ancoragem, fecho e retrator foram inspecionados?",
    "31. Bancos, suportes, pedais, ergonomia e interferências nos comandos foram avaliados?",
    "32. Sistema de limpador, esguichos, braços e palhetas foram testados?",
    "33. Fixação e ancoragem dos cintos e bancos foram avaliadas e documentadas?",
    "34. Falhas, sensores, mensagens do painel e histórico diagnóstico foram verificados?",
    
    # Elétrica, Iluminação e Dispositivos de Segurança
    "10 (E). Circuitos, suportes, iluminação, relés e lanternas foram inspecionados?",
    "11 (E). Buzina e alarme de ré foram submetidos a teste funcional controlado?",
    "12 (E). Câmera, monitor, fiação, fixação e imagem foram inspecionados e testados?",
    "13 (E). O sensor de presença foi testado em procedimento controlado e teve calibração/posicionamento conferidos?",
    "14 (E). Giroflex, fixações e alimentação elétrica foram avaliados?",
    "15 (E). Estrobo, fixações e alimentação elétrica foram avaliados?",
    "16 (E). Registros, aferição/regularidade do registrador de velocidade foram conferidos?",
    "17 (E). Comandos e dispositivos para prevenir descida involuntária foram testados?",
    "18 (E). Indicadores e intertravamentos de basculamento foram testados?",
    "19 (E). Dispositivos de advertência de marcha à ré tiveram resultado de ensaio controlado registrado?",
    "20 (E). Indicador de caçamba elevada e limitações de basculamento foram testados, quando equipados?",
    
    # Freios e Testes Finais
    "21 (F). Sistema de freios, componentes, indicadores e ensaios previstos foram conferidos?",
    "22 (F). Freio de estacionamento, acionamento e condição de retenção foram inspecionados?",
    "23 (F). Direção, articulações, transmissão e folgas foram avaliadas?",
    "24 (F). Testes instrumentados ou procedimentos específicos do sistema de frenagem foram realizados quando requeridos?",
    "25 (F). Calços em condições de uso e quantidade suficiente?"
]

opcoes_status = ["ATENDE", "ATENDE PARCIAL", "NÃO ATENDE", "NÃO SE APLICA"]

respostas = []

st.subheader("📝 Itens de Inspeção")

# Formulário interativo
with st.form("form_checklist"):
    for idx, item in enumerate(itens_checklist):
        st.markdown(f"**{item}**")
        col_opt, col_obs = st.columns([2, 3])
        
        with col_opt:
            status = st.radio(
                "Status",
                opcoes_status,
                key=f"status_{idx}",
                horizontal=True,
                label_visibility="collapsed"
            )
        
        with col_obs:
            obs = st.text_input(
                "Observações",
                key=f"obs_{idx}",
                placeholder="Observações adicionais..."
            )
        
        respostas.append({
            "Nº / Descrição": item,
            "Status": status,
            "Observações": obs
        })
        st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    st.subheader("📌 Recomendações e Assinaturas")
    recomendacoes = st.text_area("RECOMENDAÇÕES E OBSERVAÇÕES GERAIIS:")
    
    col_resp1, col_resp2 = st.columns(2)
    with col_resp1:
        resp_inspecao = st.text_input("Responsável pela Inspeção:")
    with col_resp2:
        resp_equipamento = st.text_input("Responsável pelo Equipamento:")

    submitted = st.form_submit_button("💾 Salvar / Gerar Relatório")

# --- EXPORTAÇÃO DOS DADOS ---
if submitted:
    df_respostas = pd.DataFrame(respostas)
    
    st.success("Check List preenchido com sucesso!")
    
    st.subheader("📊 Resumo das Respostas")
    st.dataframe(df_respostas, use_container_width=True)
    
    # Download em CSV
    csv = df_respostas.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Check List preenchido (CSV)",
        data=csv,
        file_name=f"checklist_caminhao_{id_equipamento}_{data_inspecao}.csv",
        mime='text/csv',
    )

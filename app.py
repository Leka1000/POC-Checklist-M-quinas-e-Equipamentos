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
    local_servico = st.text_input("Local do Serviço:")
    id_equipamento = st.text_input("Identificação do Equipamento / Placa / Frota:")
    data_inspecao = st.date_input("Data da Inspeção:", value=date.today())

with col2:
    codigo_doc = st.text_input("Código do Documento:", value="CL-EQ-001")
    doc_ref = st.text_input("Doc. Referenciado:")
    revisao = st.text_input("Revisão:", value="00")

with col3:
    periodicidade = st.text_input("Periodicidade da Inspeção:", value="Mensal")
    cor_liberacao = st.selectbox(
        "Cor correspondente à liberação:",
        ["Verde", "Amarelo", "Branco", "Azul", "Outra"]
    )

st.markdown("---")

# --- DEFINIÇÃO DOS ITENS POR EQUIPAMENTO ---
if equipamento_selecionado == "Caminhão Basculante":
    itens_checklist = [
        "1. CRLV-e, documentos de operação, inspeções e exigências aplicáveis foram conferidos?",
        "2. Manual, identificação do modelo, modificações e plano de manutenção estão atualizados?",
        "4. Análise de risco e condições de descarga são verificadas antes de cada basculamento?",
        "5. Histórico de manutenção preventiva e corretiva está atualizado, com OS encerradas e evidências?",
        "6. As recomendações do fabricante por quilometragem/tempo estão atendidas e rastreadas?",
        "7. Identificação do veículo, placas, faixas e sinalização foram conferidas quanto à integridade?",
        "8. Os calços são compatíveis com pneus, massa, solo e procedimento de imobilização?",
        "9. Pneus, sulcos, pressão, aros, fixações e reapertos foram avaliados conforme fabricante?",
        "11. Chassi, longarinas, suportes, fixações e soldas estão íntegros, sem reparos irregulares?",
        "12. Foram identificadas e tratadas fugas nos sistemas de combustível, lubrificação, ar e arrefecimento?",
        "13. Extintores e demais meios de emergência foram inspecionados, incluindo fixações e manutenção?",
        "14. Equipamentos de emergência, estepe e ferramentas estão completos e adequados, quando exigidos?",
        "15. Retrovisores, regulagens, fechaduras, vedações e vidros foram avaliados detalhadamente?",
        "16. Estrutura da caçamba, soldas, dobradiças, batentes e travas foram examinados?",
        "17. Pinos, buchas, retenções, suportes e folgas foram inspecionados?",
        "18. Sistema hidráulico de basculamento, vedação, mangueiras e cilindros foi inspecionado?",
        "19. Escora/trava mecânica para caçamba elevada foi examinada, conforme fabricante?",
        "20. Cobertura, acionamentos e fixações foram conferidos?",
        "21/22. Suspensão, molas, amortecedores, buchas, suportes, terminais de direção, barras e articulações foram avaliados?",
        "23. Linhas e reservatórios pneumáticos/hidráulicos de freio estão íntegros, com drenagem e ensaios previstos?",
        "24. Fixação de cabine ao chassi e respectivos suportes/coxins estão íntegros?",
        "25. Sistema de exaustão, suportes e proteção contra aquecimento indevido estão íntegros?",
        "26. Bateria, chicotes, terminais e proteções elétricas estão íntegros, sem improvisações?",
        "27. Bujões, reservatórios e tampas estão íntegros e identificados, sem vestígios de vazamento?",
        "28. Há evidência de torque/reaperto de fixadores críticos quando previsto em manutenção?",
        "29. A caçamba elevada possui suporte/escora de manutenção estrutural e funcional, com uso restrito?",
        "30. Cinto, ancoragem, fecho e retrator foram inspecionados?",
        "31. Bancos, suportes, pedais, ergonomia e interferências nos comandos foram avaliados?",
        "32. Sistema de limpador, esguichos, braços e palhetas foram testados?",
        "33. Fixação e ancoragem dos cintos e bancos foram avaliadas e documentadas?",
        "34. Falhas, sensores, mensagens do painel e histórico diagnóstico foram verificados?",
        "10 (Elétrica). Circuitos, suportes, iluminação, relés e lanternas foram inspecionados?",
        "11 (Elétrica). Buzina e alarme de ré foram submetidos a teste funcional controlado?",
        "12 (Elétrica). Câmera, monitor, fiação, fixação e imagem foram inspecionados e testados?",
        "13 (Elétrica). O sensor de presença foi testado em procedimento controlado e teve calibração/posicionamento conferidos?",
        "14 (Elétrica). Giroflex, fixações e alimentação elétrica foram avaliados?",
        "15 (Elétrica). Estrobo, fixações e alimentação elétrica foram avaliados?",
        "16 (Elétrica). Registros, aferição/regularidade do registrador de velocidade foram conferidos?",
        "17 (Elétrica). Comandos e dispositivos para prevenir descida involuntária foram testados?",
        "18 (Elétrica). Indicadores e intertravamentos de basculamento foram testados?",
        "19 (Elétrica). Dispositivos de advertência de marcha à ré tiveram resultado de ensaio controlado registrado?",
        "20 (Elétrica). Indicador de caçamba elevada e limitações de basculamento foram testados, quando equipados?",
        "21 (Freios). Sistema de freios, componentes, indicadores e ensaios previstos foram conferidos?",
        "22 (Freios). Freio de estacionamento, acionamento e condição de retenção foram inspecionados?",
        "23 (Freios). Direção, articulações, transmissão e folgas foram avaliadas?",
        "24 (Freios). Testes instrumentados ou procedimentos específicos do sistema de frenagem foram realizados quando requeridos?",
        "25 (Freios). Calços em condições de uso e quantidade suficiente?"
    ]

elif equipamento_selecionado == "Caminhão Carroceria - Cabine Complementar":
    itens_checklist = [
        "1. CRLV-e, documentos de operação, inspeções e exigências aplicáveis foram conferidos?",
        "2. Manual, identificação do modelo, modificações e plano de manutenção estão atualizados?",
        "4. Lotação e condições do projeto de transporte de passageiros estão regularizadas?",
        "5. Histórico de manutenção preventiva e corretiva está atualizado, com OS encerradas e evidências?",
        "6. As recomendações do fabricante por quilometragem/tempo estão atendidas e rastreadas?",
        "7. Identificação do veículo, placas, faixas e sinalização foram conferidas quanto à integridade?",
        "8. Os calços são compatíveis com pneus, massa, solo e procedimento de imobilização?",
        "10. Pneus, sulcos, pressão, aros, fixações e reapertos foram avaliados conforme fabricante?",
        "11. Chassi, longarinas, suportes, fixações e soldas estão íntegros, sem reparos irregulares?",
        "12. Foram identificadas e tratadas fugas nos sistemas de combustível, lubrificação, ar e arrefecimento?",
        "13. Extintores e demais meios de emergência foram inspecionados, incluindo fixações e manutenção?",
        "14. Equipamentos de emergência, estepe e ferramentas estão completos e adequados, quando exigidos?",
        "15. Retrovisores, regulagens, fechaduras, vedações e vidros foram avaliados detalhadamente?",
        "16. Longarinas, piso, fixadores e pontos de ancoragem foram inspecionados?",
        "17. Escada, piso, guarda-corpo e sistema de proteção contra quedas foram examinados?",
        "18. Cintas, correntes, catracas e ancoragens têm identificação e capacidade compatíveis?",
        "19. Suspensão, molas, amortecedores, buchas e suportes apresentam integridade e folgas aceitáveis?",
        "20. Terminais de direção, barras e articulações foram avaliados quanto a desgaste e fixação?",
        "21. Linhas e reservatórios pneumáticos/hidráulicos de freio estão íntegros, com drenagem e ensaios previstos?",
        "22. Fixação de cabine ao chassi e respectivos suportes/coxins estão íntegros?",
        "23. Sistema de exaustão, suportes e proteção contra aquecimento indevido estão íntegros?",
        "24. Bateria, chicotes, terminais e proteções elétricas estão íntegros, sem improvisações?",
        "25. Bujões, reservatórios e tampas estão íntegros e identificados, sem vestígios de vazamento?",
        "26. Há evidência de torque/reaperto de fixadores críticos quando previsto em manutenção?",
        "27. Cinto, ancoragem, fecho e retrator foram inspecionados?",
        "28. Bancos, suportes, pedais, ergonomia e interferências nos comandos foram avaliados?",
        "29. Sistema de limpador, esguichos, braços e palhetas foram testados?",
        "30. Fixação e ancoragem dos cintos e bancos foram avaliadas e documentadas?",
        "31. Projeto/homologação, ancoragens, estrutura e fixações da cabine complementar foram verificados?",
        "32. Ancoragens, cintos, bancos e encostos de cabeça foram inspecionados?",
        "33. Sistema de intercomunicação, acionamento e indicadores foram testados?",
        "34. Saída de emergência, abertura e identificação foram avaliadas?",
        "35. Fechaduras, travas e vedações da cabine complementar foram inspecionadas?",
        "36. Documentos de transformação/homologação da cabine complementar foram revisados?",
        "37. Suportes estruturais e fixadores da cabine complementar foram inspecionados?",
        "38. Falhas, sensores, mensagens do painel e histórico diagnóstico foram verificados?",
        "9 (Elétrica). Circuitos, suportes, iluminação, relés e lanternas foram inspecionados?",
        "10 (Elétrica). Buzina e alarme de ré foram submetidos a teste funcional controlado?",
        "11 (Elétrica). Câmera, monitor, fiação, fixação e imagem foram inspecionados e testados?",
        "12 (Elétrica). O sensor de presencia foi testado em procedimento controlado e teve calibração/posicionamento conferidos?",
        "13 (Elétrica). Giroflex, fixações e alimentação elétrica foram avaliados?",
        "14 (Elétrica). Estrobo, fixações e alimentação elétrica foram avaliados?",
        "15 (Elétrica). Registros, aferição/regularidade do registrador de velocidade foram conferidos?",
        "16 (Elétrica). Dispositivos de advertência de marcha à ré tiveram resultado de ensaio controlado registrado?",
        "17 (Elétrica). Sistema de freios, componentes, indicadores e ensaios previstos foram conferidos?",
        "18 (Freios). Freio de estacionamento, acionamento e condição de retenção foram inspecionados?",
        "19 (Freios). Direção, articulações, transmissão e folgas foram avaliadas?",
        "19 (Extra). O veículo possui calços em condições e quantidade suficientes?"
    ]

else:  # Bobcat
    itens_checklist = [
        "1. Manuais, modificações autorizadas e plano de manutenção estão disponíveis e atualizados?",
        "3. Histórico de manutenção por horímetro, pendências e correções está atualizado?",
        "4. Periodicidade de inspeções técnicas indicada pelo fabricante está atendida?",
        "5. Identificação, faixas, avisos e símbolos estão completos e íntegros?",
        "6. Estrutura, suportes, soldas e fixações foram inspecionados quanto a trincas/deformações?",
        "7. ROPS/FOPS, ancoragens e ausência de alterações não autorizadas foram conferidos?",
        "8. Tubulações, retentores, conexões, reservatórios e eventuais vazamentos foram avaliados?",
        "9. Proteções, suportes e intertravamentos foram avaliados quanto à integridade?",
        "10. Extintor e/ou medidas de combate a incêndio foram verificados quanto à adequação?",
        "11. Tensão, roletes, pneus/esteiras, rodas e fixadores foram avaliados?",
        "12. Acoplador, pinos, travas, soldas, dentes e travamento foram inspecionados?",
        "13. Braços, articulações, buchas e suportes foram avaliados?",
        "14. Trava de sustentação e instruções de bloqueio estão íntegras e identificadas?",
        "15. Fixadores estruturais, soldas e pontos de apoio foram inspecionados quanto a deformações?",
        "16. Pontos de lubrificação, mancais, buchas e pinos foram avaliados quanto à lubrificação e folgas?",
        "17. Coifas, chapas e proteções de partes móveis foram avaliadas quanto à fixação e resistência?",
        "18. Instalação elétrica, bateria, proteção dos chicotes e conexões foram verificadas?",
        "19. Instrumentação, alertas e eventuais códigos de falha foram avaliados?",
        "20. Mangueiras hidráulicas foram avaliadas por abrasão, dobramento, idade/condição e retenções?",
        "21. Filtro de ar, refrigeração, correias e ventiladores foram verificados pelo plano do fabricante?",
        "22. Pontos de ancoragem ou suporte para manutenção do implemento estão íntegros?",
        "23. Engate rápido e retenção contra desprendimento foram auditados?",
        "24. Degraus, superfícies antiderrapantes, corrimãos, soldas e fixações foram inspecionados?",
        "25. Vidros, espelhos, suportes, ajustes e visibilidade foram conferidos?",
        "26. Ancoragem, retrator, fecho, costuras e regulagem do cinto foram examinados?",
        "27. Assento, mecanismos de regulagem, fixações, vedações e condições ergonômicas foram avaliados?",
        "28. Sistema de climatização e desembaçamento foi avaliado frente à NR-18 e à configuração?",
        "29. Sensores de ocupação, barra de retenção e lógica de intertravamento foram testados?",
        "30. Ancoragens do banco/cinto e elementos de cabine foram examinados quanto a folgas?",
        "20 (Segurança). Alarme de ré e buzina foram testados quanto ao funcionamento e audibilidade?",
        "21 (Segurança). Instalação e funcionamento dos sistemas de iluminação foram inspecionados?",
        "22 (Segurança). Câmera, monitor e cabeamento foram submetidos a teste funcional?",
        "23 (Segurança). Detecção, indicação e instalação do sensor foram testadas?",
        "24 (Segurança). Giroflex, fixação e alimentação elétrica foram avaliados?",
        "25 (Segurança). Estrobo, fixação e

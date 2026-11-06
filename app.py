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
    "Caminhão Carroceria - Cabine Complementar": [
        "1. CRLV-e, documentos de operação, inspeções e exigências aplicáveis foram conferidos?",
        "2. Manual, identificação do modelo, modificações e plano de manutenção estão atualizados?",
        "3. Lotação e condições do projeto de transporte de passageiros estão regularizadas?",
        "4. Histórico de manutenção preventiva e corretiva está atualizado, com OS encerradas e evidências?",
        "5. As recomendações do fabricante por quilometragem/tempo estão atendidas e rastreadas?",
        "6. Identificação do veículo, placas, faixas e sinalização foram conferidas quanto à integridade?",
        "7. Os calços são compatíveis com pneus, massa, solo e procedimento de imobilização?",
        "8. Circuitos, suportes, iluminação, relés e lanternas foram inspecionados?",
        "9. Buzina e alarme de ré foram submetidos a teste funcional controlado?",
        "10. Câmera, monitor, fiação, fixação e imagem foram inspecionados e testados?",
        "11. O sensor de presença foi testado em procedimento controlado e teve calibração/posicionamento conferidos?",
        "12. Giroflex, fixações e alimentação elétrica foram avaliados?",
        "13. Estrobo, fixações e alimentação elétrica foram avaliados?",
        "14. Registros, aferição/regularidade do registrador de velocidade foram conferidos?",
        "15. Dispositivos de advertência de marcha à ré tiveram resultado de ensaio controlado registrado?",
        "16. Sistema de freios, componentes, indicadores e ensaios previstos foram conferidos?",
        "17. Pneus, sulcos, pressão, aros, fixações e reapertos foram avaliados conforme fabricante?",
        "18. Chassi, longarinas, suportes, fixações e soldas estão íntegros, sem reparos irregulares?",
        "19. Foram identificadas e tratadas fugas nos sistemas de combustível, lubrificação, ar e arrefecimento?",
        "20. Extintores e demais meios de emergência foram inspecionados, incluindo fixações e manutenção?",
        "21. Equipamentos de emergência, estepe e ferramentas estão completos e adequados, quando exigidos?",
        "22. Retrovisores, regulagens, fechaduras, vedações e vidros foram avaliados detalhadamente?",
        "23. Longarinas, piso, fixadores e pontos de ancoragem foram inspecionados?",
        "24. Escada, piso, guarda-corpo e sistema de proteção contra quedas foram examinados?",
        "25. Cintas, correntes, catracas e ancoragens têm identificação e capacidade compatíveis?",
        "26. Suspensão, molas, amortecedores, buchas e suportes apresentam integridade e folgas aceitáveis?",
        "27. Terminais de direção, barras e articulações foram avaliados quanto a desgaste e fixação?",
        "28. Linhas e reservatórios pneumáticos/hidráulicos de freio estão íntegros, com drenagem e ensaios previstos?",
        "29. Fixação de cabine ao chassi e respectivos suportes/coxins estão íntegros?",
        "30. Sistema de exaustão, suportes e proteção contra aquecimento indevido estão íntegros?",
        "31. Bateria, chicotes, terminais e proteções elétricas estão íntegros, sem improvisações?",
        "32. Bujões, reservatórios e tampas estão íntegros e identificados, sem vestígios de vazamento?",
        "33. Há evidência de torque/reaperto de fixadores críticos quando previsto em manutenção?",
        "34. Cinto, ancoragem, fecho e retrator foram inspecionados?",
        "35. Bancos, suportes, pedais, ergonomia e interferências nos comandos foram avaliados?",
        "36. Sistema de limpador, esguichos, braços e palhetas foram testados?",
        "37. Fixação e ancoragem dos cintos e bancos foram avaliadas e documentadas?",
        "38. Projeto/homologação, ancoragens, estrutura e fixações da cabine complementar foram verificados?",
        "39. Ancoragens, cintos, bancos e encostos de cabeça foram inspecionados?",
        "40. Sistema de intercomunicação, acionamento e indicadores foram testados?",
        "41. Saída de emergência, abertura e identificação foram avaliadas?",
        "42. Fechaduras, travas e vedações da cabine complementar foram inspecionadas?",
        "43. Documentos de transformação/homologação da cabine complementar foram revisados?",
        "44. Suportes estruturais e fixadores da cabine complementar foram inspecionados?",
        "45. Falhas, sensores, mensagens do painel e histórico diagnóstico foram verificados?",
        "46. Freio de estacionamento, acionamento e condição de retenção foram inspecionados?",
        "47. Direção, articulações, transmissão e folgas foram avaliadas?",
        "48. O veículo possui calços em condições e quantidade suficientes?"
    ],
    "Bobcat": [
        "1. Manuais, modificações autorizadas e plano de manutenção estão disponíveis e atualizados?",
        "2. Histórico de manutenção por horímetro, pendências e correções está atualizado?",
        "3. Periodicidade de inspeções técnicas indicada pelo fabricante está atendida?",
        "4. Identificação, fa

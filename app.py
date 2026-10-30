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
        "4. Identificação, faixas, avisos e símbolos estão completos e íntegros?",
        "5. Estrutura, suportes, soldas e fixações foram inspecionados quanto a trincas/deformações?",
        "6. ROPS/FOPS, ancoragens e ausência de alterações não autorizadas foram conferidos?",
        "7. Tubulações, retentores, conexões, reservatórios e eventuais vazamentos foram avaliados?",
        "8. Proteções, suportes e intertravamentos foram avaliados quanto à integridade?",
        "9. Extintor e/ou medidas de combate a incêndio foram verificados quanto à adequação?",
        "10. Tensão, roletes, pneus/esteiras, rodas e fixadores foram avaliados?",
        "11. Acoplador, pinos, travas, soldas, dentes e travamento foram inspecionados?",
        "12. Braços, articulações, buchas e suportes foram avaliados?",
        "13. Trava de sustentação e instruções de bloqueio estão íntegras e identificadas?",
        "14. Fixadores estruturais, soldas e pontos de apoio foram inspecionados quanto a deformações?",
        "15. Pontos de lubrificação, mancais, buchas e pinos foram avaliados quanto à lubrificação e folgas?",
        "16. Coifas, chapas e proteções de partes móveis foram avaliadas quanto à fixação e resistência?",
        "17. Instalação elétrica, bateria, proteção dos chicotes e conexões foram verificadas?",
        "18. Instrumentação, alertas e eventuais códigos de falha foram avaliados?",
        "19. Mangueiras hidráulicas foram avaliadas por abrasão, dobramento, idade/condição e retenções?",
        "20. Filtro de ar, refrigeração, correias e ventiladores foram verificados pelo plano do fabricante?",
        "21. Pontos de ancoragem ou suporte para manutenção do implemento estão íntegros?",
        "22. Engate rápido e retenção contra desprendimento foram auditados?",
        "23. Degraus, superfícies antiderrapantes, corrimãos, soldas e fixações foram inspecionados?",
        "24. Vidros, espelhos, suportes, ajustes e visibilidade foram conferidos?",
        "25. Ancoragem, retrator, fecho, costuras e regulagem do cinto foram examinados?",
        "26. Assento, mecanismos de regulagem, fixações, vedações e condições ergonômicas foram avaliados?",
        "27. Sistema de climatização e desembaçamento foi avaliado frente à NR-18 e à configuração?",
        "28. Sensores de ocupação, barra de retenção e lógica de intertravamento foram testados?",
        "29. Ancoragens do banco/cinto e elementos de cabine foram examinados quanto a folgas?",
        "30. Alarme de ré e buzina foram testados quanto ao funcionamento e audibilidade?",
        "31. Instalação e funcionamento dos sistemas de iluminação foram inspecionados?",
        "32. Câmera, monitor e cabeamento foram submetidos a teste funcional?",
        "33. Detecção, indicação e instalação do sensor foram testadas?",
        "34. Giroflex, fixação e alimentação elétrica foram avaliados?",
        "35. Estrobo, fixação e alimentação elétrica foram avaliados?",
        "36. Motor, suportes, ruídos, vazamentos e sistema de arrefecimento foram examinados?",
        "37. Circuitos de segurança, partida e travamentos hidráulicos foram testados?",
        "38. Chaves gerais, sistemas de intertravamento e bloqueio elétrico estão identificados e íntegros?",
        "39. Foram registrados resultados de testes controlados de sensores/alertas e dos dispositivos corporativos aplicáveis?",
        "40. Foi ensaiada a lógica de segurança de barra de retenção/ocupação segundo instruções do fabricante?",
        "41. Sistemas de freio, retenção e acionamentos foram submetidos a testes controlados?",
        "42. Comandos, intertravamentos e sistemas de direção/transmissão foram inspecionados?",
        "43. Controle de elevação, retenção e resposta dos cilindros foram testados?",
        "44. Sistema de engate rápido foi testado conforme fabricante?",
        "45. A direção, freios, transmissão e comandos foram avaliados com registros de ensaio quando previstos?",
        "46. Sistema de estacionamento, desligamento e bloqueio de acionamento indevido foi inspecionado?"
    ]
}

itens_checklist = CHECKLISTS[equipamento_selecionado]
opcoes_status = ["ATENDE", "ATENDE PARCIAL", "NÃO ATENDE", "NÃO SE APLICA"]

st.subheader(f"📝 Itens de Inspeção: {equipamento_selecionado}")

# --- FORMULÁRIO INTERATIVO ---
with st.form("form_checklist"):
    respostas_temporarias = []
    
    for idx, item in enumerate(itens_checklist):
        st.markdown(f"**{item}**")
        col_opt, col_obs = st.columns([2, 3])
        
        with col_opt:
            status = st.radio(
                "Status",
                opcoes_status,
                key=f"status_{equipamento_selecionado}_{idx}",
                horizontal=True,
                label_visibility="collapsed"
            )
        
        with col_obs:
            obs = st.text_input(
                "Observações",
                key=f"obs_{equipamento_selecionado}_{idx}",
                placeholder="Observações adicionais..."
            )
        
        respostas_temporarias.append({
            "item_idx": idx,
            "descricao": item,
            "status_key": f"status_{equipamento_selecionado}_{idx}",
            "obs_key": f"obs_{equipamento_selecionado}_{idx}"
        })
        st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    st.subheader("📌 Recomendações e Observações Gerais")
    recomendacoes = st.text_area("Insira recomendações ou observações gerais:", key="rec_geral")
    
    st.subheader("✍️ Assinaturas e Responsáveis")
    col_resp1, col_resp2 = st.columns(2)
    with col_resp1:
        resp_inspecao = st.text_input("Responsável pela Inspeção (Nome):", key="resp_insp")
    with col_resp2:
        resp_equipamento = st.text_input("Responsável pelo Equipamento (Nome):", key="resp_eqp")

    # --- Bloco de Assinatura Digital (Canvas) ---
    st.markdown("#### 🖊️ Assinatura Digital do Inspetor")
    st.markdown("Utilize o campo abaixo para desenhar a sua assinatura:")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=500,
        drawing_mode="freedraw",
        return_image_data=True,
        key=f"canvas_assinatura_{equipamento_selecionado}",
    )

    submitted = st.form_submit_button("Gerar e Salvar Relatório Formatado")

# --- PROCESSAR E SALVAR OS DADOS EM FORMATO DE FORMULÁRIO ---
if submitted:
    if not resp_inspecao.strip() or not resp_equipamento.strip():
        st.warning("⚠️ Por favor, preencha os nomes dos responsáveis antes de gerar o relatório.")
    else:
        respostas_finais = []
        for item_info in respostas_temporarias:
            status_atual = st.session_state.get(item_info["status_key"], "ATENDE")
            obs_atual = st.session_state.get(item_info["obs_key"], "")
            
            respostas_finais.append({
                "Nº / Descrição do Item": item_info["descricao"],
                "Status": status_atual,
                "Observações": obs_atual
            })

        df_respostas = pd.DataFrame(respostas_finais)
        
        pasta_destino = "historico_geral"
        os.makedirs(pasta_destino, exist_ok=True)
        
        nome_equipamento_limpo = str(id_equipamento).replace(" ", "_").replace("/", "-")
        if not nome_equipamento_limpo:
            nome_equipamento_limpo = "geral"
            
        nome_base = f"checklist_{equipamento_selecionado.replace(' ', '_')}_{nome_equipamento_limpo}_{data_inspecao}"
        caminho_xlsx = os.path.join(pasta_destino, f"{nome_base}.xlsx")
        caminho_consolidado = os.path.join(pasta_destino, "Relatorio_Consolidado_Checklists.xlsx")
            
        try:
            # --- CONSTRUÇÃO DO FORMULÁRIO EXCEL FORMATADO ---
            wb = Workbook()
            ws = wb.active
            ws.title = "Relatório de Inspeção"
            
            # 1. Cabeçalho Principal
            ws['A1'] = "SISTEMA DE CHECK LIST MENSAL DE EQUIPAMENTOS"
            ws['A1'].font = openpyxl.styles.Font(size=14, bold=True)
            
            # 2. Informações Gerais (Metadados)
            ws['A3'] = "Local do Serviço:"; ws['B3'] = local_servico
            ws['A4'] = "Equipamento:"; ws['B4'] = equipamento_selecionado
            ws['A5'] = "ID / Prefixo:"; ws['B5'] = id_equipamento
            ws['A6'] = "Data da Inspeção:"; ws['B6'] = str(data_inspecao)
            ws['C3'] = "Periodicidade:"; ws['D3'] = periodicidade
            ws['C4'] = "Revisão:"; ws['D4'] = revisao
            ws['C5'] = "Cor de Liberação:"; ws['D5'] = cor_liberacao
            
            # 3. Tabela de Itens (Linha 8 em diante)
            ws['A8'] = "ITENS DE INSPEÇÃO"
            ws['A8'].font = openpyxl.styles.Font(bold=True)
            
            headers = ["Nº / Descrição do Item", "Status", "Observações"]
            for col_idx, header in enumerate(headers, start=1):
                cell = ws.cell(row=9, column=col_idx)
                cell.value = header
                cell.font = openpyxl.styles.Font(bold=True)
                cell.fill = openpyxl.styles.PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
            
            row_idx = 10
            for item in respostas_finais:
                ws.cell(row=row_idx, column=1, value=item["Nº / Descrição do Item"])
                ws.cell(row=row_idx, column=2, value=item["Status"])
                ws.cell(row=row_idx, column=3, value=item["Observações"])
                row_idx += 1
                
            # 4. Observações Gerais e Responsáveis
            row_idx += 1
            ws.cell(row=row_idx, column=1, value="Recomendações Gerais:").font = openpyxl.styles.Font(bold=True)
            ws.cell(row=row_idx+1, column=1, value=recomendacoes)
            
            row_idx += 4
            ws.cell(row=row_idx, column=1, value=f"Responsável Inspeção: {resp_inspecao}")
            ws.cell(row=row_idx, column=3, value=f"Responsável Equipamento: {resp_equipamento}")
            
            # 5. Inserção da Assinatura Digital no Excel
            if canvas_result.image_data is not None:
                img_pil = Image.fromarray(canvas_result.image_data.astype('uint8'))
                caminho_img_temp = os.path.join(pasta_destino, f"{nome_base}_assinatura.png")
                img_pil.save(caminho_img_temp)
                
                row_idx += 2
                ws.cell(row=row_idx, column=1, value="Assinatura Digital do Inspetor:")
                img_excel = OpenpyxlImage(caminho_img_temp)
                img_excel.width = 250
                img_excel.height = 70
                ws.add_image(img_excel, f"A{row_idx+1}")

            # Salva o arquivo individual formatado
            wb.save(caminho_xlsx)

            # --- ATUALIZA O ARQUIVO ACUMULATIVO CONSOLIDADO ---
            df_novo_registro = pd.DataFrame([{
                "Local": local_servico,
                "Equipamento": equipamento_selecionado,
                "ID/Prefixo": id_equipamento,
                "Data": str(data_inspecao),
                "Responsável Inspeção": resp_inspecao,
                "Responsável Equipamento": resp_equipamento,
                "Revisão": revisao
            }])
            
            if os.path.exists(caminho_consolidado):
                df_antigo = pd.read_excel(caminho_consolidado)
                df_final = pd.concat([df_antigo, df_novo_registro], ignore_index=True)
            else:
                df_final = df_novo_registro
            
            df_final.to_excel(caminho_consolidado, index=False)

            st.success("✅ Check List salvo no formato de formulário com sucesso!")
            st.info(f"O arquivo formatado foi salvo em: **{caminho_xlsx}**")

            st.subheader("📊 Visualização dos Itens Preenchidos")
            st.dataframe(df_respostas, use_container_width=True)
            
            # --- BOTÃO DE DOWNLOAD DO RELATÓRIO FORMATADO ---
            with open(caminho_xlsx, "rb") as f:
                excel_bytes = f.read()

            st.download_button(
                label="📥 Baixar Relatório em Excel (Formato Original)",
                data=excel_bytes,
                file_name=f"{nome_base}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except Exception as e:
            st.error(f"Erro ao tentar formatar e salvar o arquivo em Excel: {e}")

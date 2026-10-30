if submitted:
    if not resp_inspecao.strip() or not resp_equipamento.strip():
        st.warning("⚠️ Por favor, preencha os nomes dos responsáveis antes de gerar o relatório.")
    else:
        # Monta a lista oficial de respostas lendo diretamente dos estados dos widgets
        respostas_finais = []
        for item_info in respostas_temporarias:
            status_atual = st.session_state.get(item_info["status_key"], "ATENDE")
            obs_atual = st.session_state.get(item_info["obs_key"], "")
            
            respostas_finais.append({
                "Local": local_servico,
                "Equipamento": equipamento_selecionado,
                "ID/Prefixo": id_equipamento,
                "Nº / Descrição": item_info["descricao"],
                "Status": status_atual,
                "Observações": obs_atual,
                "Recomendações Gerais": recomendacoes,
                "Responsável Inspeção": resp_inspecao,
                "Responsável Equipamento": resp_equipamento,
                "Data da Inspeção": str(data_inspecao),
                "Revisão": revisao,
                "Periodicidade": periodicidade,
                "Cor Liberação": cor_liberacao
            })

        df_respostas = pd.DataFrame(respostas_finais)
        
        if diretorio_customizado.strip() == "":
            pasta_destino = "historico_checklists"
        else:
            pasta_destino = diretorio_customizado.strip()
            
        try:
            os.makedirs(pasta_destino, exist_ok=True)
            
            nome_equipamento_limpo = str(id_equipamento).replace(" ", "_").replace("/", "-")
            if not nome_equipamento_limpo:
                nome_equipamento_limpo = "geral"
                
            nome_base = f"checklist_{equipamento_selecionado.replace(' ', '_')}_{nome_equipamento_limpo}_{data_inspecao}"
            caminho_csv = os.path.join(pasta_destino, f"{nome_base}.csv")
            
            # Salva o arquivo CSV localmente
            df_respostas.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
            
            # Salva a assinatura digital como imagem PNG se o usuário desenhou algo
            caminho_img = None
            if canvas_result.image_data is not None:
                img = Image.fromarray(canvas_result.image_data.astype('uint8'))
                caminho_img = os.path.join(pasta_destino, f"{nome_base}_assinatura.png")
                img.save(caminho_img)

            st.success("✅ Check List preenchido e guardado com sucesso!")
            st.info(f"O relatório foi salvo em: **{caminho_csv}**")

            # --- ENVIO AUTOMÁTICO POR E-MAIL ---
            # ATENÇÃO: Para enviar via código Python, você precisa configurar um e-mail remetente e uma senha de aplicativo.
            EMAIL_REMETENTE = "seu_email@gmail.com"  # Substitua pelo seu e-mail do Gmail
            SENHA_APLICATIVO = "sua_senha_de_app"      # Substitua pela sua senha de aplicativo do Gmail
            EMAIL_DESTINO = "lekaolinascimento@gmail.com"

            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_REMETENTE
                msg['To'] = EMAIL_DESTINO
                msg['Subject'] = f"Check List Concluído - {equipamento_selecionado} ({id_equipamento})"

                 corpo = f"Olá,\n\nSegue em anexo o relatório do Check List Mensal referente ao equipamento {equipamento_selecionado} (ID: {id_equipamento}), realizado em {data_inspecao}.\n\nAtenciosamente,\nSistema de Check List"
                msg.attach(MIMEText(corpo, 'plain'))

                # Anexa o CSV
                with open(caminho_csv, "rb") as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(caminho_csv)}')
                msg.attach(part)

                # Anexa a Assinatura (se existir)
                if caminho_img and os.path.exists(caminho_img):
                    with open(caminho_img, "rb") as f:
                        part_img = MIMEBase('application', 'octet-stream')
                        part_img.set_payload(f.read())
                    encoders.encode_base64(part_img)
                    part_img.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(caminho_img)}')
                    msg.attach(part_img)

                # Conexão com o servidor SMTP do Gmail
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_REMETENTE, SENHA_APLICATIVO)
                server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
                server.quit()

                st.success(f"📧 E-mail com os arquivos enviado com sucesso para **{EMAIL_DESTINO}**!")

            except Exception as email_err:
                st.warning(f"⚠️ O checklist foi salvo localmente, mas houve um erro ao enviar o e-mail automático: {email_err}")

            st.subheader("📊 Resumo das Respostas")
            st.dataframe(df_respostas, use_container_width=True)
            
            csv_data = df_respostas.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Descarregar Cópia Extra (CSV)",
                data=csv_data,
                file_name=f"{nome_base}.csv",
                mime='text/csv'
            )
            
        except Exception as e:
            st.error(f"Erro ao tentar salvar o arquivo na pasta indicada: {e}")

import streamlit as st
import smtplib
from email.mime.text import MIMEText

def Formulario():
    def enviar_email(nome, email, empresa, descricao_servico):
        remetente = "seuemail@gmail.com"
        senha = "sua_senha"
        destinatario = "destinatariofixo@gmail.com"
        
        corpo_email = f"""
        Solicitação de Serviço de Desenvolvimento e Automação RPA
        ---------------------------------------------------------
        Nome: {nome}
        E-mail: {email}
        Empresa: {empresa}
        Descrição do Serviço: {descricao_servico}
        """
        
        msg = MIMEText(corpo_email)
        msg["Subject"] = "Nova Solicitação de Serviço"
        msg["From"] = remetente
        msg["To"] = destinatario
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(remetente, senha)
                server.sendmail(remetente, destinatario, msg.as_string())
            return True
        except Exception as e:
            return False
    
    st.title("Solicitação de Serviço de Desenvolvimento e Automação RPA")
    
    with st.form(key='solicitacao_servico'):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        empresa = st.selectbox('Selecione sua divisão:', ['Portifólio', 'Prospecção', 'Gerência', 'Outros'])
        descricao_servico = st.text_area("Descrição do Serviço")
        
        enviar = st.form_submit_button("Solicitar Serviço")
        
        if enviar:
            if enviar_email(nome, email, empresa, descricao_servico):
                st.success(f"Obrigado, {nome}! Sua solicitação foi enviada com sucesso.")
            else:
                st.error("Houve um erro ao enviar a solicitação. Tente novamente mais tarde.")

    st.warning("Em fase de Teste")
if __name__ == "__main__":
    Formulario()


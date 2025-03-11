import streamlit as st
from Pages.Analise_de_codigo.analise_de_codigo import analise_codigo
from Pages.LeitorDeContrato.LeitordeContrato import LeitordeContrato
from Pages.Formulario.formulario import Formulario



# Tenta importar a função consulta_cmed e captura possíveis erros
try:
    from Pages.Consulta_CMED.consultaCMED import consulta_cmed
    cmed_disponivel = True
except ImportError as e:
    st.sidebar.error("Erro ao carregar Consulta CMED. Verifique a instalação.")
    cmed_disponivel = False

# Criar menu lateral para navegar entre os projetos

image_url = "https://raw.githubusercontent.com/TojiFushiguro2000/Portal_Terceiros/main/Images/eurofarma-logo.png"
st.sidebar.image(image_url, use_column_width=True)


# Menu lateral
st.sidebar.title("Portal de Ferramentas CMO Terceiros")


# Exibir as opções de menu
pagina_selecionada = st.sidebar.radio("Escolha uma funcionalidade:", ["Home", "Análise de Código", "Consulta CMED", "Leitor de Contrato com IA", "Solicitar Serviço"])

if pagina_selecionada == "Home":
    st.title("Bem-vindo ao Portal de Ferramentas")
    st.write("Escolha uma funcionalidade no menu lateral.")

elif pagina_selecionada == "Análise de Código":
    with st.spinner("Carregando Análise de Código..."):
        analise_codigo()  

elif pagina_selecionada == "Consulta CMED":
    if cmed_disponivel:
        with st.spinner("Carregando Consulta CMED..."):
            consulta_cmed()  
    else:
        st.error("A funcionalidade Consulta CMED não pôde ser carregada.")

elif pagina_selecionada == "Leitor de Contrato com IA":
    if cmed_disponivel:
        with st.spinner("Leitor de Contrato com IA..."):
            LeitordeContrato()  
    else:
        st.error("A funcionalidade Leitor de Contrato com IA não pôde ser carregada.")

elif pagina_selecionada == "Solicitar Serviço":
    if cmed_disponivel:
        with st.spinner("Carregando Solicitação de Serviço..."):
            Formulario()
    else:
        st.error("A funcionalidade Solicitar Serviço não pôde ser carregada.")

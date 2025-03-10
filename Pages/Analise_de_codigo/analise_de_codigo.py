import pandas as pd
import xlsxwriter
import streamlit as st
import requests
from io import BytesIO

# URL do arquivo Excel no GitHub
URL_ARQUIVO = "https://github.com/TojiFushiguro2000/Portal_Terceiros/raw/main/Pages/Analise_de_codigo/data/MEGA-BL.xlsx"
def analise_codigo():
    # Função para carregar os dados da planilha
    @st.cache_data
    def carregar_dados():
        try:
            response = requests.get(URL_ARQUIVO)
            if response.status_code == 200:
                df = pd.read_excel(BytesIO(response.content), engine="openpyxl")
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove colunas Unnamed
                
                # Ajustes nas colunas
                if 'Produção' in df.columns:
                    df['Produção'] = df['Produção'].apply(lambda x: int(x) if pd.notnull(x) else x)
                if 'Código' in df.columns:
                    df['Código'] = df['Código'].astype(str).str.replace(',', '', regex=False)
    
                return df
            else:
                st.error(f"Erro ao baixar o arquivo do GitHub: Código {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
            return pd.DataFrame()
    
    # Função para realizar pesquisa com um único termo
    def pesquisar(dados, tipo, termo):
        colunas = ['BLOCO', 'Código', 'Descrição', 'Familia', 'Tipo', 'Sub-divisão', 'CÓDIGO BULK', 'Produção', 'Lote']
        if tipo.lower() == "cod" and 'Código' in dados.columns:
            return dados[dados['Código'].astype(str).str.contains(termo, case=False, na=False)][colunas]
        elif tipo.lower() == "desc" and 'Descrição' in dados.columns:
            return dados[dados['Descrição'].str.contains(termo, case=False, na=False)][colunas]
        elif tipo.lower() == "fam" and 'Familia' in dados.columns:
            return dados[dados['Familia'].str.contains(termo, case=False, na=False)][colunas]
        else:
            return pd.DataFrame()
    
    # Função para realizar múltiplas pesquisas
    def pesquisar_multiplos(dados, tipo, termos):
        resultados = pd.DataFrame()
        for termo in termos:
            termo = termo.strip()  # Remove espaços extras
            if termo:
                resultado = pesquisar(dados, tipo, termo)
                resultados = pd.concat([resultados, resultado], ignore_index=True)
        return resultados
    
    # Função para gerar o link de download no formato XLSX
    def gerar_link_download(df, nome_arquivo):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')
        st.download_button(
            label="Baixar resultados filtrados",
            data=output.getvalue(),
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Interface Streamlit
    st.title("Análise de Código EUROFARMA")
    st.markdown("""
    Esta aplicação permite realizar múltiplas pesquisas com base em uma lista de termos, e baixar os resultados no formato Excel.
    """)
    
    # Carregar os dados automaticamente
    df = carregar_dados()
    
    # Seleção do tipo de pesquisa
    tipo_de_pesquisa = st.selectbox(
        "Escolha o tipo de pesquisa:",
        options=["Código (COD)", "Descrição (DESC)", "Família (FAM)"],
        index=0
    )
    
    # Mapear os inputs para o tipo esperado pela função
    tipo_map = {"Código (COD)": "cod", "Descrição (DESC)": "desc", "Família (FAM)": "fam"}
    tipo = tipo_map[tipo_de_pesquisa]
    
    # Exemplo de entrada para o usuário
    st.markdown("""
    **Exemplo de entrada:**  
    - Para pesquisar por códigos: `1234, 5678, 91011`  
    - Para pesquisar por descrições: `Produto A, Produto B, Produto C`  
    - Para pesquisar por famílias: `Família X, Família Y, Família Z`  
    *Separe os termos por vírgulas.*
    """)
    
    # Campo para os termos de pesquisa
    termos_de_pesquisa = st.text_area("Digite os termos de pesquisa (separados por vírgulas):")
    
    # Botão de pesquisa
    if st.button("Pesquisar"):
        lista_termos = termos_de_pesquisa.split(',')  # Divide os termos por vírgulas
        resultados = pesquisar_multiplos(df, tipo, lista_termos)
    
        if not resultados.empty:
            # Formatar a coluna "Produção" com separador de milhar
            if 'Produção' in resultados.columns:
                resultados['Produção'] = resultados['Produção'].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notnull(x) else x)
    
            # Verificar se há "Subsidiária" na coluna 'Tipo'
            if 'Tipo' in resultados.columns:
                linhas_subsidiarias = resultados[resultados['Tipo'].str.strip().str.contains("subsidiária", case=False, na=False)]
                if not linhas_subsidiarias.empty:
                    st.warning(f"""
    Os resultados incluem {len(linhas_subsidiarias)} itens com o tipo 'Subsidiária'.  
    **Linhas identificadas:**  
    """)
                    st.dataframe(linhas_subsidiarias)
    
            st.success("Resultados encontrados:")
            st.dataframe(resultados)
            gerar_link_download(resultados, "resultados_pesquisa.xlsx")
        else:
            st.warning("Nenhum resultado encontrado.")

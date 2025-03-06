import streamlit as st
import pandas as pd

def plot_pmc(resultados):
    pmc_data = resultados[['LABORATÓRIO', 'PMC Sem Imposto']]
    pmc_data = pmc_data[pmc_data['PMC Sem Imposto'] > 0.00]
    pmc_data = pmc_data.sort_values(by='PMC Sem Imposto')

    st.subheader('Gráfico: PMC Sem Imposto')
    st.bar_chart(pmc_data.set_index('LABORATÓRIO').sort_values(by='PMC Sem Imposto', ascending=True), use_container_width=True)

def plot_pf(resultados):
    pf_data = resultados[['LABORATÓRIO', 'PF Sem Impostos']]
    pf_data = pf_data[pf_data['PF Sem Impostos'] > 0.00]
    pf_data = pf_data.sort_values(by='PF Sem Impostos')

    st.subheader('Gráfico: PF Sem Impostos')
    st.bar_chart(pf_data.set_index('LABORATÓRIO').sort_values(by='PF Sem Impostos', ascending=True), use_container_width=True)

def consulta_cmed():
    st.title('Consulta à Tabela CMED')

    # Carregar os dados do Excel
    caminho_arquivo = r'C:\\Users\\T-Gamer\Desktop\\Portal_Ferramentas\\Pages\\Consulta_CMED\\data\dados-CMED.xlsx'
    df = pd.read_excel(caminho_arquivo)

    coluna = st.selectbox('Selecione a coluna:', ['SUBSTÂNCIA/API', 'PRODUTO/MARCA'])
    pesquisa = st.text_input('Pesquisa:', '')

    if st.button('Consultar'):
        if pesquisa and coluna:
            resultados = df[df[coluna].str.contains(pesquisa, case=False, na=False)]

            if not resultados.empty:
                concorrentes = resultados['LABORATÓRIO'].dropna().unique()
                concorrentes = [conc for conc in concorrentes if "EUROFARMA LABORATÓRIOS S.A." not in conc]

                st.subheader('Concorrentes')
                for i, concorrente in enumerate(concorrentes, start=1):
                    st.write(f"{i}. {concorrente}")

                st.subheader('PMC mais em conta')
                pmc_data = resultados[['LABORATÓRIO', 'PMC Sem Imposto']]
                pmc_data = pmc_data[pmc_data['PMC Sem Imposto'] > 0.00]
                pmc_data = pmc_data.sort_values(by='PMC Sem Imposto')
                pmc_mais_em_conta = pmc_data.iloc[0]
                st.markdown(f"<font color='green'>{pmc_mais_em_conta['LABORATÓRIO']}: R$ {pmc_mais_em_conta['PMC Sem Imposto']:.2f}</font>", unsafe_allow_html=True)

                st.subheader('PF mais em conta')
                pf_data = resultados[['LABORATÓRIO', 'PF Sem Impostos']]
                pf_data = pf_data[pf_data['PF Sem Impostos'] > 0.00]
                pf_data = pf_data.sort_values(by='PF Sem Impostos')
                pf_mais_em_conta = pf_data.iloc[0]
                st.markdown(f"<font color='green'>{pf_mais_em_conta['LABORATÓRIO']}: R$ {pf_mais_em_conta['PF Sem Impostos']:.2f}</font>", unsafe_allow_html=True)

                st.subheader('Resultados da Pesquisa')
                st.write(resultados)

                # Gráficos
                st.subheader('Gráficos')
                plot_pmc(resultados)
                plot_pf(resultados)
            else:
                st.error("Produto/Substância não encontrado")

    if st.button('Limpar Pesquisa'):
        st.session_state.pesquisa = ''
        st.session_state.coluna = ''
        st.experimental_rerun()

    st.write("\n\n\nCriado e Desenvolvido por Lucas Lopes da Silva, Aprendiz Terceiros-CMO Globais 2024 EUROFARMA -- Versão(1.0)", unsafe_allow_html=True)

if __name__ == '__main__':
    consulta_cmed()

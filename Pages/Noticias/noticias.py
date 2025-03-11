# import requests
# from bs4 import BeautifulSoup
# import streamlit as st

# # Função para extrair as notícias do portal
# def obter_noticias():
#     url = 'https://panoramafarmaceutico.com.br/noticias/industriafarmaceutica/'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     noticias = []
#     for item in soup.find_all('div', class_='td-module-thumb'):
#         titulo = item.find('a')['title']
#         link = item.find('a')['href']
#         noticias.append({'titulo': titulo, 'link': link})

#     return noticias

# # Função principal do Streamlit
# def noticias():
#     st.title('Notícias da Indústria Farmacêutica')
#     noticias = obter_noticias()

#     for noticia in noticias:
#         st.subheader(noticia['titulo'])
#         st.markdown(f"[Leia mais]({noticia['link']})")

# if __name__ == '__main__':
#     noticias()

import streamlit as st

def def noticias(): 
    st.title("Em Desenvolvimento...")

if __name__ == "__main__":
    noticias()

import streamlit as st
from modules import build_model, tsne_plot, build_authenticator

if __name__ == "__main__":
    st.set_page_config(page_title="Dadosfera Case", page_icon=":bar_chart:", layout="wide")

    st.image("https://dadosfera.ai/webinar/wp-content/uploads/2022/08/Logo_Dadosfera_Branca-1024x426.png", width = 150)
    authenticator = build_authenticator()
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1946/1946429.png", width = 100)
        st.sidebar.title(f"Welcome {name}")
        selected_column = st.sidebar.selectbox("Select a column:", ["Title", "Text", "category", "material","features"])
        authenticator.logout('Logout', 'sidebar')

        st.title("Dashboard Product Search Scopus")
        st.header("Word Embedding Chart:")

        with st.spinner('Wait for it...'):
            tsne_plot(build_model(selected_column))

    elif authentication_status == False:
        st.error('Username or password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')



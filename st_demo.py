import asyncio


import streamlit as st





def main():
    st.set_page_config(layout="wide")
    col1,col2 = st.columns(2)
    with col1:
        st.header("Client")
        container1 = st.empty()
        container2 = st.empty()
    with col2:
        st.header("Server")
    asyncio.run(run_server(container1,container2))

async def run_server(container1,container2):
    pass



if __name__ == '__main__':
    main()

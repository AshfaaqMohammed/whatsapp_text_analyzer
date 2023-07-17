import streamlit as st
from llama_index import download_loader
from llama_index import GPTVectorStoreIndex
import pandas as pd

# @st.cache(hash_funcs={'builtins.CoreBPE': lambda _: None}, show_spinner=False, allow_output_mutation=True)
# @st.cache_data
def start_query():
    st.session_state['query_started'] = True


# @st.cache(hash_funcs={'builtins.CoreBPE': lambda _: None}, show_spinner=False, allow_output_mutation=True)
# @st.cache_data
def get_response(question):
    PandasCSVReader = download_loader('PandasCSVReader')
    loader = PandasCSVReader()
    documents = loader.load_data('small.csv')
    index = GPTVectorStoreIndex(documents)
    query_engine = index.as_query_engine()
    inputs = question
    response = query_engine.query(inputs)
    return response


def small_df(df):
    llm = pd.DataFrame(df[['Message', 'User', 'Only date']].iloc[-100:])
    # if 'small.csv' not in os.listdir('.'):
    llm.to_csv('small.csv', index=False)

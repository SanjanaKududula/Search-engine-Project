import streamlit as st
import chromadb

client = chromadb.PersistentClient(path="/path/to/save/to")
client.heartbeat()
collection = client.get_collection(name="subtitle_sem")


st.set_page_config(
    page_title="ShowFinder 🔍",
    page_icon=":tv:",
    layout="wide"
)


def set_style():
    st.markdown("""
    <style>
    .title {
        font-size: 36px !important;
        text-align: center !important;
        margin-bottom: 30px !important;
    }
    .subtitle {
        font-size: 24px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    .text {
        font-size: 18px !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

set_style()


st.title('ShowFinder 🔍')
st.subheader('Say goodbye to endless scrolling and decision fatigue 😫')


query_text = st.text_input('Enter your query:')
if st.button('Generate'):
    def similar_title(query_text):
        result = collection.query(
            query_texts=[query_text],
            include=["metadatas", "distances"],
            n_results=10
        )
        ids = result['ids'][0]
        distances = result['distances'][0]
        metadatas = result['metadatas'][0]
        sorted_data = sorted(zip(metadatas, ids, distances), key=lambda x: x[2], reverse=True)
        return sorted_data

    result_data = similar_title(query_text)
    

    st.success('Here are the most relevant subtitle names:')
    for metadata, ids, distance in result_data:
        subtitle_name = metadata['subtitle_name']
        subtitle_id = metadata['subtitle_id']
        subtitle_link = f"https://www.opensubtitles.org/en/subtitles/{subtitle_id}"
        st.markdown(f"[{subtitle_name}]({subtitle_link})")


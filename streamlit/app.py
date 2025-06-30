import os

import pandas as pd

import streamlit as st
import requests

# Backend endpoint
API_URL = os.getenv("API_URL")  # Change to your backend URL

st.set_page_config(page_title="Intelligent Document Search", layout="centered")
st.title("📄 Intelligent Document Understanding")

st.markdown("Upload a document (PDF, PNG, JPG) and search for relevant content.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "png", "jpg", "jpeg"])

# Selector for number of results to retrieve

# Search query input
with st.form(key="search_form"):
    query = st.text_input("🔍 Enter your search query:")
    k = st.number_input("🔢 Number of results to return", min_value=1, max_value=50, value=5, step=1)
    submitted = st.form_submit_button("Search")

if submitted and query:
    params = {
        "k": k,
        "query": query
    }

    try:
        response = requests.get(API_URL + "/api/extract_entities", params=params)
#        response = requests.get(API_URL + "/api/extract_entities", json={"query": "red book", "k": 3}})
        response.raise_for_status()
        results = response.json()

        for idx, chunk in enumerate(results):
            st.markdown(f"**Chunk {idx + 1}:**")
            for key, value in chunk.items():
                match key:
                    case "document_type" | "document_name" | "document_content":
                        st.write(f"**{key}:** {value}")
                    case "entities":
                        # Assumes value["entities"] is a list of dicts
                        df = pd.DataFrame([
                            {f"entity": k, "value": v}
                            for k, v in value.items()
                        ])
                        st.dataframe(df, use_container_width=True)

            st.markdown(f"**Score:** {chunk['score']:.2f}")
            st.markdown(f"**Explain Score:** {chunk['explain_score']}")
            st.divider()

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")



if uploaded_file and not submitted:
    with st.spinner("Analyzing document..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

        try:
            response = requests.post(API_URL + "/api/documents", files=files)
            response.raise_for_status()
            results = response.json()
            st.success("Document uploaded and processed successfully!")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


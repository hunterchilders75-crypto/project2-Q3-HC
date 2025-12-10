import streamlit as st
from langchain_ollama import ChatOllama

# Initialize LLaMA via Ollama
llm = ChatOllama(model="llama3.2:latest", temperature=0.2)

st.title("Input to AI")

# Question input
question = st.text_input("Enter your question")

# File uploader
file_input = st.file_uploader("Upload a TXT, PDF, DOCX, or HTML file", type=["txt", "pdf", "docx", "html"])

if st.button("Submit"):
    st.subheader("AI Response:")

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        context_text = ""
        if file_input is not None:
            suffix = file_input.name.split(".")[-1].lower()
            try:
                if suffix == "txt":
                    # Flat file: open/read
                    context_text = file_input.read().decode("utf-8", errors="ignore")

                elif suffix == "pdf":
                    # PDF: PyPDF2 (basic text extraction)
                    import PyPDF2
                    reader = PyPDF2.PdfReader(file_input)
                    context_text = " ".join([page.extract_text() or "" for page in reader.pages])

                elif suffix == "docx":
                    # DOCX: docx2txt
                    import docx2txt
                    context_text = docx2txt.process(file_input)

                elif suffix in ["html", "htm"]:
                    # HTML: BeautifulSoup
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(file_input.read(), "html.parser")
                    context_text = soup.get_text(separator=" ")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        # Build prompt with context if available
        if context_text:
            prompt = f"Use the following document context to answer the question.\n\nContext:\n{context_text}\n\nQuestion: {question}"
        else:
            prompt = question

        response = llm.invoke(prompt)
        st.write(response.content)


import streamlit as st

from agents.orchestrator import ask

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Healthcare Multi-Agent Assistant",
    page_icon="🏥",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🏥 Healthcare Assistant")

    st.success("✅ SQL Agent")
    st.success("✅ RAG Agent")

    st.divider()

    st.subheader("Project Features")

    st.write("• SQLite Database")
    st.write("• FAISS Vector Database")
    st.write("• HuggingFace Embeddings")
    st.write("• Groq LLM")
    st.write("• Multi-Agent Routing")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# TITLE
# =====================================================

st.title("🏥 RAG-Based Healthcare Query Assistant")

st.write(
    "Ask questions about patient records or hospital policies."
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================================
# USER INPUT
# =====================================================

question = st.chat_input(
    "Ask your healthcare question..."
)

if question:

    # ============================
    # USER MESSAGE
    # ============================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # ============================
    # ASSISTANT
    # ============================

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = ask(question)

                agent = result["agent"]

                answer = result["answer"]

                # ============================
                # SQL AGENT
                # ============================

                if agent == "SQL":

                    st.success("🗄 SQL Agent Selected")

                    if "sql" in result:

                        with st.expander("Generated SQL"):

                            st.code(
                                result["sql"],
                                language="sql"
                            )

                # ============================
                # RAG AGENT
                # ============================

                else:

                    st.info("📚 RAG Agent Selected")

                # ============================
                # ANSWER
                # ============================

                st.markdown(answer)

                # ============================
                # SOURCE DOCUMENTS
                # ============================

                if (
                    agent == "RAG"
                    and result.get("sources")
                ):

                    st.divider()

                    st.subheader("📄 Source Documents")

                    for source in result["sources"]:

                        st.write(f"• {source}")

                assistant_message = answer

            except Exception as e:

                assistant_message = f"❌ Error\n\n{str(e)}"

                st.error(assistant_message)

    # ============================
    # SAVE CHAT
    # ============================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Healthcare Multi-Agent Assistant | Groq + SQLite + FAISS + Streamlit"
)
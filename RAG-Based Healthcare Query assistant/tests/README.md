# 🏥 RAG-Based Healthcare Query Assistant

## 📌 Project Overview

The **RAG-Based Healthcare Query Assistant** is an AI-powered multi-agent system that enables hospital staff to retrieve information from both structured patient records and unstructured hospital policy documents using natural language.

The system intelligently routes user queries through an **Orchestrator Agent** to either:

- **SQL Agent** – Queries structured patient data stored in SQLite.
- **RAG Agent** – Retrieves and answers questions from hospital policy documents using Retrieval-Augmented Generation (RAG).

This project was developed as part of an **Intern Mini Project** to demonstrate practical applications of Generative AI, NLP, Vector Databases, and Multi-Agent Systems.

---

# 🎯 Objectives

- Convert natural language into SQL queries.
- Query patient records stored in SQLite.
- Retrieve hospital policies using RAG.
- Build an intelligent multi-agent routing system.
- Provide a conversational interface using Streamlit.

---

# 🏗 Project Architecture

```
                    User
                      │
                      ▼
             Streamlit Web Interface
                      │
                      ▼
             Orchestrator Agent
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
     SQL Agent               RAG Agent
          │                       │
          ▼                       ▼
     SQLite Database        FAISS Vector DB
                                  │
                                  ▼
                    HuggingFace Embeddings
                                  │
                                  ▼
                           Groq Llama 3.3
                                  │
                                  ▼
                           Final Response
```

---

# 🚀 Features

- ✅ Natural Language to SQL
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Intelligent Query Routing
- ✅ SQLite Database
- ✅ FAISS Vector Database
- ✅ HuggingFace Embeddings
- ✅ Groq Llama 3.3 Integration
- ✅ Hospital Policy Question Answering
- ✅ SQL Validation
- ✅ Conversational Chat Interface
- ✅ Response Formatting
- ✅ Error Handling

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | User Interface |
| SQLite | Patient Database |
| LangChain | RAG Pipeline |
| FAISS | Vector Database |
| HuggingFace | Text Embeddings |
| Groq API | Large Language Model |
| Llama 3.3 70B | AI Model |
| Pandas | Data Processing |
| SQL | Database Querying |

---

# 📂 Project Structure

```
project/

│
├── agents/
│   ├── generative_client.py
│   ├── orchestrator.py
│   ├── rag_agent.py
│   └── sql_agent.py
│
├── database/
│   ├── db_utils.py
│   └── hospital.db
│
├── docs/
│
├── prompts/
│   └── sql_prompt.txt
│
├── tests/
│   ├── test_sql.py
│   ├── test_rag.py
│   ├── test_routing.py
│   └── test_latency.py
│
├── vector_db/
│
├── data/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── .env
```

---

# 📊 Dataset

The project uses a **synthetic healthcare dataset** containing approximately **10,000 patient records**.

### Patient Information

- Name
- Age
- Gender
- Blood Type

### Clinical Data

- Medical Condition
- Medication
- Test Results

### Hospital Details

- Hospital
- Doctor
- Room Number

### Admission Details

- Admission Type
- Admission Date
- Discharge Date

### Financial Information

- Insurance Provider
- Billing Amount

---

# 🤖 Multi-Agent System

## 1️⃣ SQL Agent

Responsible for:

- Natural Language to SQL Conversion
- SQL Validation
- Query Execution
- Database Response Formatting

Example:

**Question**

```
How many patients are there?
```

Generated SQL

```sql
SELECT COUNT(*) FROM patients;
```

---

## 2️⃣ RAG Agent

Responsible for:

- Document Retrieval
- Similarity Search
- Context Generation
- Grounded Answer Generation

Example:

**Question**

```
What is the discharge policy?
```

The agent retrieves the most relevant hospital policy chunks and generates an answer using Groq.

---

## 3️⃣ Orchestrator Agent

The Orchestrator detects the user's intent and routes the query to the appropriate agent.

Example:

| Query | Agent |
|--------|------|
| How many patients are there? | SQL Agent |
| What is the discharge policy? | RAG Agent |

---

# 💻 Installation

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙ Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶ Run Application

```bash
streamlit run app.py
```

---

# 🧪 Testing

Run SQL tests

```bash
python tests/test_sql.py
```

Run RAG tests

```bash
python tests/test_rag.py
```

Run Routing tests

```bash
python tests/test_routing.py
```

Run Latency tests

```bash
python tests/test_latency.py
```

---

# 💬 Sample SQL Questions

```
How many patients are there?
```

```
Show all diabetic patients.
```

```
Show average billing amount by insurance provider.
```

```
Which patients have abnormal test results?
```

---

# 📚 Sample Policy Questions

```
What is admission policy?
```

```
What is discharge policy?
```

```
What is insurance policy?
```

```
Is prior insurance approval required?
```

---

# 📈 Project Workflow

1. User enters a question.
2. Streamlit sends the query to the Orchestrator.
3. Orchestrator detects the intent.
4. SQL Agent or RAG Agent processes the request.
5. Groq Llama generates the final response.
6. Response is displayed to the user.

---

# 📋 Testing & Evaluation

The system was evaluated on:

- SQL Accuracy
- Retrieval Relevance
- Agent Routing
- Response Time
- Error Handling

---

# 🔮 Future Improvements

- Voice Assistant
- Authentication
- Medical Image Support
- PostgreSQL Support
- Multi-language Support
- Dashboard Analytics
- Conversation Memory
- Hybrid Search
- Docker Deployment

---

# 📷 Demo

The application provides:

- Interactive Chat Interface
- SQL Query Generation
- RAG-based Policy Answers
- Source Document Display
- Multi-Agent Routing

---

# 👨‍💻 Author

**Intern Mini Project**

**RAG-Based Healthcare Query Assistant**

Developed using:

- Python
- Streamlit
- SQLite
- FAISS
- LangChain
- Groq Llama 3.3

---

# ⭐ Thank You

Thank you for reviewing this project.

This project demonstrates the integration of **Generative AI**, **RAG**, **Vector Search**, **SQL**, and **Multi-Agent Systems** to build an intelligent healthcare assistant.
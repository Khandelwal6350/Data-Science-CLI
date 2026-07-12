from pathlib import Path
from dotenv import load_dotenv
import os

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

# =====================================================
# PROJECT PATHS
# =====================================================

DATA_PATH = BASE_DIR / "data"

DATABASE_PATH = BASE_DIR / "database" / "hospital.db"

DOCS_PATH = BASE_DIR / "docs"

VECTOR_DB_PATH = BASE_DIR / "vector_db" / "faiss_index"

PROMPTS_PATH = BASE_DIR / "prompts"

SQL_PROMPT_FILE = PROMPTS_PATH / "sql_prompt.txt"

# =====================================================
# GROQ API
# =====================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file."
    )

# =====================================================
# GROQ MODEL
# =====================================================

MODEL_NAME = "llama-3.3-70b-versatile"

# Fallback Models
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

# =====================================================
# GENERATION SETTINGS
# =====================================================

TEMPERATURE = 0.2

MAX_TOKENS = 1024

TOP_K = 3

MAX_RETRIES = 3

RETRY_DELAY = 3
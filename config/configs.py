import os
from dotenv import load_dotenv

load_dotenv()
# ---------------------------------------------
# |                                           |
# |             Config Variables              |
# |                                           |
# ---------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

NEO4J_API_KEY = os.getenv("NEO4J_API_KEY", "")
NEO4J_CONNECTION_URL = os.getenv("NEO4J_CONNECTION_URL", "")
NEO4J_USER = os.getenv("NEO4J_USER", "")

# DB_HOST = os.getenv("DB_HOST", "")
# DB_PORT = os.getenv("DB_PORT", "")
# DB_NAME = os.getenv("DB_NAME", "")
# DB_USER = os.getenv("DB_USER", "")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")

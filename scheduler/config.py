import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI = os.environ.get("MONGO_URI")

# OpenAI
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
#OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
#OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
#OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE")
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
OPENAI_DEPLOYMENT_NAME = os.environ.get("OPENAI_DEPLOYMENT_NAME")

# Alpaca
#ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
#ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.environ.get("ALPACA_SECRET_KEY")

# News API
#NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#NEWS_API_SECRET = os.getenv("NEWS_API_SECRET")
#NEWS_API_ENDPOINT = os.getenv("NEWS_API_ENDPOINT")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_SECRET = os.environ.get("NEWS_API_SECRET")
NEWS_API_ENDPOINT = os.environ.get("NEWS_API_ENDPOINT")



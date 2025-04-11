import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

# Gemini API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASS = 'your_db_password'
DB_HOST = 'localhost'
SECRET_KEY = 'your-secret-key'
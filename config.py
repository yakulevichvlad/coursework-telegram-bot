"""
Configuration settings for the Telegram Bot application.
"""

import os
from pathlib import Path

# ============================================================================
# API Keys and Tokens
# ============================================================================

# Telegram Bot Token
# Get this from BotFather on Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'your_telegram_token_here')

# OpenAI API Key
# Get this from https://platform.openai.com/account/api-keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')

# ============================================================================
# Database Configuration
# ============================================================================

# Base directory for the application
BASE_DIR = Path(__file__).resolve().parent

# Database file path
DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'data' / 'bot.db'))

# Enable database logging (for debugging)
DATABASE_LOGGING = os.getenv('DATABASE_LOGGING', 'False').lower() == 'true'

# ============================================================================
# Application Settings
# ============================================================================

# Application name
APP_NAME = 'Telegram Bot'

# Application version
APP_VERSION = '1.0.0'

# Debug mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Logging level
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Logging file path
LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'logs' / 'bot.log'))

# ============================================================================
# Bot Behavior Settings
# ============================================================================

# Request timeout (in seconds)
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))

# Maximum retries for failed requests
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# Retry delay (in seconds)
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))

# ============================================================================
# OpenAI Settings
# ============================================================================

# OpenAI Model to use
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

# Maximum tokens for OpenAI responses
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2000'))

# Temperature for OpenAI responses (0.0 - 2.0)
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

# ============================================================================
# User and Rate Limiting
# ============================================================================

# Rate limit: messages per minute per user
RATE_LIMIT_MESSAGES = int(os.getenv('RATE_LIMIT_MESSAGES', '10'))

# Rate limit window (in seconds)
RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))

# ============================================================================
# Feature Flags
# ============================================================================

# Enable user statistics tracking
ENABLE_STATISTICS = os.getenv('ENABLE_STATISTICS', 'True').lower() == 'true'

# Enable message history persistence
ENABLE_MESSAGE_HISTORY = os.getenv('ENABLE_MESSAGE_HISTORY', 'True').lower() == 'true'

# Enable user feedback collection
ENABLE_FEEDBACK = os.getenv('ENABLE_FEEDBACK', 'True').lower() == 'true'

# ============================================================================
# Validation and Initialization
# ============================================================================

def validate_config():
    """
    Validate that all required configuration values are set.
    
    Raises:
        ValueError: If any required configuration value is missing or invalid.
    """
    required_keys = ['TELEGRAM_TOKEN', 'OPENAI_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        value = globals().get(key)
        if not value or value.startswith('your_'):
            missing_keys.append(key)
    
    if missing_keys:
        raise ValueError(
            f"Missing or invalid configuration values: {', '.join(missing_keys)}. "
            f"Please set these environment variables or update config.py"
        )


def create_directories():
    """Create necessary directories for the application."""
    directories = [
        Path(DATABASE_PATH).parent,
        Path(LOG_FILE).parent,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Initialize directories on import
try:
    create_directories()
except Exception as e:
    print(f"Warning: Could not create directories: {e}")

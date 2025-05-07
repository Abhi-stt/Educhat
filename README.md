## 🚀 **VS Code Quick Start**

## 1. **Clone Repo & Open in VS Code**
##   ```bash
## git clone https://github.com/yourusername/Edu_chatbot.git
## code Edu_chatbot
## Setup Python Environment

## Open VS Code terminal (Ctrl+`` `` )

## Create virtual env:

## bash
## python -m venv .venv
## .\.venv\Scripts\activate  # Windows
## source .venv/bin/activate # Mac/Linux
## Install Dependencies

## bash
## pip install -r requirements.txt
## Configure Environment

## Create .env file (copy from .env.sample)

## Add your API key:

## inialize
## GEMINI_API_KEY=your_actual_key_here
## Run & Debug

## Press F5 (with Flask debug configuration)

## Or manually:

## bash
## python main.py

🌟 Features
## Feature	Description
📚 Multi-Subject	Physics, Chemistry, Philosophy
🤖 AI-Powered	Gemini/OpenAI API integration
🔒 Secure	API keys in .env
💡 Lightweight	Single-file Flask app
📂 VS Code Project Structure
## bash
Edu_chatbot/
├── .vscode/            # VS Code configs
│   ├── launch.json     # Flask debug profile
│   └── settings.json
├── main.py             # Main application
├── static/
│   └── style.css       # Custom styles
├── templates/
│   └── index.html      # Chat interface
└── requirements.txt    # Dependencies

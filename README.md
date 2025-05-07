# 🎓 EduChat - AI-Powered Study Assistant

## 🛠️ **Setup Guide (VS Code Optimized)**

### **Prerequisites**
- Python 3.9+
- VS Code with [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- API Key from [Google AI Studio](https://ai.google.dev/) or [OpenAI](https://platform.openai.com/)

---

### **Step 1: Project Setup in VS Code**
1. Clone repository:
   ```bash
   git clone 

Open in VS Code:
bash
code Edu_chatbot

Step 2: Configure Environment
Create virtual environment:

bash
python -m venv .venv
Activate it:

Windows:

bash
.\.venv\Scripts\activate

Mac/Linux:
bash
source .venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt

Step 3: API Configuration
Create .env file:

## Write the API Key
# For Gemini
GEMINI_API_KEY="your_api_key_here"

# OR for OpenAI
OPENAI_API_KEY="your_api_key_here"

⚠️ Add .env to .gitignore

Step 4: Launch the Application
Start Flask development server:

bash
python main.py
Access in browser:

http://localhost:5000
